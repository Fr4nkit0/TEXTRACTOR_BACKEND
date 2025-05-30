import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from docx import Document
from django.conf import settings
from django.core.files.base import ContentFile
import io


class ExportService:
    @staticmethod
    def export_to_pdf(text, filename=None):
        """Exportar texto a PDF"""
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        # Configuración de texto
        p.setFont("Helvetica", 12)
        margin = 50
        y_position = height - margin
        line_height = 15

        # Dividir texto en líneas
        lines = text.split('\n')

        for line in lines:
            # Verificar si necesitamos una nueva página
            if y_position < margin:
                p.showPage()
                p.setFont("Helvetica", 12)
                y_position = height - margin

            # Manejar líneas largas
            if len(line) > 80:
                words = line.split(' ')
                current_line = ''

                for word in words:
                    if len(current_line + ' ' + word) < 80:
                        current_line += ' ' + word if current_line else word
                    else:
                        p.drawString(margin, y_position, current_line)
                        y_position -= line_height
                        current_line = word

                        if y_position < margin:
                            p.showPage()
                            p.setFont("Helvetica", 12)
                            y_position = height - margin

                if current_line:
                    p.drawString(margin, y_position, current_line)
                    y_position -= line_height
            else:
                p.drawString(margin, y_position, line)
                y_position -= line_height

        p.save()
        buffer.seek(0)
        return ContentFile(buffer.getvalue(), name=filename or 'export.pdf')

    @staticmethod
    def export_to_docx(text, filename=None):
        """Exportar texto a DOCX"""
        doc = Document()

        # Agregar texto por párrafos
        paragraphs = text.split('\n')
        for paragraph in paragraphs:
            if paragraph.strip():
                doc.add_paragraph(paragraph)

        # Guardar en buffer
        buffer = io.BytesIO()
        doc.save(buffer)
        buffer.seek(0)

        return ContentFile(buffer.getvalue(), name=filename or 'export.docx')
