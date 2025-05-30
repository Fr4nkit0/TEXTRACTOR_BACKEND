from django.db import models
import uuid
# Create your models here.


class OCRResult (models.Model):
    OCR_ENGINES = [
        ('easyocr', 'EasyOCR'),
        ('paddleocr', 'PaddleOCR'),
    ]

    LANGUAGES = [
        ('es', 'Español'),
        ('en', 'Inglés'),
    ]
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    image = models.ImageField(upload_to='images/')
    engine = models.CharField(
        max_length=20,
        choices=OCR_ENGINES)
    language = models.CharField(
        max_length=10,
        choices=LANGUAGES)
    extracted_text = models.TextField()
    confidence_scores = models.JSONField(default=dict)
    average_confidence = models.FloatField(
        help_text="Porcentaje de confianza entre 0 y 100")
    processing_time = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
