from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import FileResponse
from django.shortcuts import get_object_or_404

from .models import ExportedFile
from .serializers import ExportInputSerializer, ExportedOutputFileSerializer
from .services.export_service import ExportService
from applications.ocr_processing.models import OCRResult


class ExportViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ExportedFile.objects.all()
    serializer_class = ExportInputSerializer

    @action(detail=True, methods=['post'], url_path='export')
    def export_result(self, request, pk=None):
        """Exportar resultado a PDF o DOCX"""
        ocr_result = get_object_or_404(OCRResult, pk=pk)
        serializer = ExportInputSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        export_format = serializer.validated_data['format']

        try:
            # Exportar según formato
            if export_format == 'pdf':
                file_content = ExportService.export_to_pdf(
                    ocr_result.extracted_text,
                    f'ocr_result_{pk}.pdf'
                )
            else:
                file_content = ExportService.export_to_docx(
                    ocr_result.extracted_text,
                    f'ocr_result_{pk}.docx'
                )

            # Crear registro de archivo exportado
            exported_file = ExportedFile.objects.create(
                ocr_result=ocr_result,
                file_type=export_format,
                file=file_content
            )

            return Response(
                ExportedOutputFileSerializer(exported_file, context={
                    'request': request}).data,
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['get'], url_path='download')
    def download_file(self, request, pk=None):
        """Descargar archivo exportado"""
        exported_file = get_object_or_404(ExportedFile, pk=pk)

        if not exported_file.file:
            return Response(
                {'error': 'Archivo no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )

        response = FileResponse(
            exported_file.file.open(),
            as_attachment=True,
            filename=f'ocr_export.{exported_file.file_type}'
        )
        return response
