from django.db import models
from applications.ocr_processing.models import OCRResult
import uuid


class ExportedFile(models.Model):
    EXPORT_TYPES = [
        ('pdf', 'PDF'),
        ('docx', 'DOCX'),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    ocr_result = models.ForeignKey(
        OCRResult,
        on_delete=models.PROTECT)
    file_type = models.CharField(
        max_length=10,
        choices=EXPORT_TYPES)
    file = models.FileField(upload_to='exports/')
    created_at = models.DateTimeField(auto_now_add=True)
