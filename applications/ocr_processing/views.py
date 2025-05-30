from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from PIL import Image

from .models import OCRResult
from .serializers import (
    OCRProcessInputSerializer, OCRResultOutputSerializer,
)
from .services.image_preprocessing import ImagePreprocessor
from .services.ocr_engines import OCREngineFactory


class OCRViewSet(viewsets.ModelViewSet):
    queryset = OCRResult.objects.all()
    serializer_class = OCRProcessInputSerializer
    parser_classes = [MultiPartParser, FormParser]

    @action(detail=False, methods=['post'], url_path='process')
    def process_image(self, request):
        """Procesar imagen con OCR"""
        serializer = OCRProcessInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Obtener datos
            image_file = serializer.validated_data['image']
            engine_type = serializer.validated_data['engine']
            language = serializer.validated_data['language']
            preprocessing_config = serializer.validated_data.get(
                'preprocessing', {})

            # Abrir imagen
            image = Image.open(image_file).convert("RGB")

            # Preprocesar imagen
            preprocessed_image = ImagePreprocessor.preprocess_image(
                image, preprocessing_config
            )

            # Obtener motor OCR
            ocr_engine = OCREngineFactory.get_engine(engine_type, language)

            # Extraer texto
            result = ocr_engine.extract_text(preprocessed_image)

            # Guardar resultado
            ocr_result = OCRResult.objects.create(
                image=image_file,
                engine=engine_type,
                language=language,
                extracted_text=result['text'],
                average_confidence=result['average_confidence'],
                confidence_scores=result['confidence_scores'],
                processing_time=result['processing_time']
            )

            return Response(
                OCRResultOutputSerializer(ocr_result).data,
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'], url_path='languages')
    def supported_languages(self, request):
        """Obtener idiomas soportados"""
        languages = {
            'easyocr': [
                'en', 'es'
            ],
            'paddleocr': [
                'en', 'es'
            ]
        }
        return Response(languages)
