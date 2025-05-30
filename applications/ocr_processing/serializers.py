from rest_framework import serializers
from .models import OCRResult


class ResizeSerializer(serializers.Serializer):
    width = serializers.IntegerField(min_value=1)
    height = serializers.IntegerField(min_value=1)


class CropSerializer(serializers.Serializer):
    x = serializers.IntegerField(min_value=0)
    y = serializers.IntegerField(min_value=0)
    width = serializers.IntegerField(min_value=1)
    height = serializers.IntegerField(min_value=1)


class ThresholdSerializer(serializers.Serializer):
    value = serializers.IntegerField(min_value=0, max_value=255, default=127)
    max_value = serializers.IntegerField(
        min_value=1, max_value=255, default=255)
    type = serializers.ChoiceField(
        choices=[
            'THRESH_BINARY', 'THRESH_BINARY_INV', 'THRESH_TRUNC', 'THRESH_TOZERO', 'THRESH_TOZERO_INV'
        ],
        default='THRESH_BINARY'
    )


class PreprocessingSerializer(serializers.Serializer):
    grayscale = serializers.BooleanField(required=False, default=False)
    enhance_contrast = serializers.BooleanField(required=False, default=False)
    rotate = serializers.IntegerField(required=False)  # grados, ej 90, 180
    resize = ResizeSerializer(required=False)
    crop = CropSerializer(required=False)
    binarization = serializers.BooleanField(required=False, default=False)
    noise_reduction = serializers.BooleanField(required=False, default=False)
    threshold = ThresholdSerializer(required=False)


ENGINE_CHOICES = [('easyocr', 'EasyOCR'), ('paddleocr', 'PaddleOCR')]
LANGUAGE_CHOICES = [('es', 'Español'), ('en', 'Inglés')]


class OCRProcessInputSerializer(serializers.Serializer):
    image = serializers.ImageField()
    engine = serializers.ChoiceField(
        choices=ENGINE_CHOICES, default='easyocr')
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='en')
    preprocessing = PreprocessingSerializer(required=False)


class OCRResultOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = OCRResult
        fields = [
            'id', 'image', 'engine', 'language', 'extracted_text',
            'average_confidence', 'processing_time', 'confidence_scores'
        ]
