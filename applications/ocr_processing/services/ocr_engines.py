import easyocr
import paddleocr
import hashlib
import json
from django.core.cache import cache
from django.conf import settings
import time
from abc import ABC, abstractmethod


class OCREngineFactory:
    _engines = {}

    @classmethod
    def get_engine(cls, engine_type, language='en'):
        """Factory method para obtener instancias de motores OCR"""
        engine_key = f"{engine_type}_{language}"

        if engine_key not in cls._engines:
            if engine_type == 'easyocr':
                cls._engines[engine_key] = EasyOCREngine(language)
            elif engine_type == 'paddleocr':
                cls._engines[engine_key] = PaddleOCREngine(language)
            else:
                raise ValueError(f"Motor OCR no soportado: {engine_type}")

        return cls._engines[engine_key]

# Implementar un tecnica de cache para mas adelante para mejor el tiempo de respuesta


class BaseOCREngine(ABC):
    def __init__(self, language):
        self.language = language
        self.engine = None

    # def _get_cache_key(self, image_data, config):
    #     """Generar clave de caché basada en imagen y configuración"""
    #     config_str = json.dumps(config, sort_keys=True)
    #     combined = f"{image_data}_{config_str}_{self.__class__.__name__}_{self.language}"
    #     return hashlib.md5(combined.encode()).hexdigest()

    def extract_text(self, image, config=None):
        # """Extraer texto con caché"""
        if config is None:
            config = {}

        #  # Generar hash de la imagen para caché
        # image_hash = hashlib.md5(image.tobytes()).hexdigest()
        # cache_key = self._get_cache_key(image_hash, config)

        # # Verificar caché
        # cached_result = cache.get(cache_key)
        # if cached_result:
        #     return cached_result

        # Procesar imagen
        start_time = time.time()
        result = self._process_image(image)
        processing_time = time.time() - start_time

        # Formatear resultado
        formatted_result = {
            'text': result['text'],
            'average_confidence': result['average_confidence'],
            'confidence_scores': result['confidence_scores'],
            'processing_time': processing_time
        }

        # # Guardar en caché
        # cache.set(cache_key, formatted_result,
        #           timeout=settings.OCR_CACHE_TIMEOUT)

        return formatted_result

    @abstractmethod
    def _process_image(self, image):
        """Debe ser implementado por subclases"""
        pass


class EasyOCREngine(BaseOCREngine):
    def __init__(self, language):
        super().__init__(language)
        lang_codes = language.split(',') if ',' in language else [language]
        self.engine = easyocr.Reader(lang_codes, gpu=False)

    def _process_image(self, image):
        try:
            results = self.engine.readtext(image)

            text_parts = []
            confidence_scores = []

            for (bbox, text, confidence) in results:
                text_parts.append(text)
                confidence_scores.append(confidence)

            average_confidence = (
                (sum(confidence_scores) / len(confidence_scores)) * 100
                if confidence_scores else 0.0
            )

            return {
                'text': '\n'.join(text_parts),
                'average_confidence': round(average_confidence, 4),
                'confidence_scores': confidence_scores
            }
        except Exception as e:
            print(f"Error al procesar la imagen con EasyOCR: {e}")
            return {
                'text': '',
                'average_confidence': 0.0,
                'confidence_scores': []
            }

# AREGLA LA IMPLEMENTACION DE ESTA CLASE NO FUNCIONA AUN


class PaddleOCREngine(BaseOCREngine):
    def __init__(self, language):
        super().__init__(language)
        self.engine = paddleocr.PaddleOCR(
            use_angle_cls=True,
            lang=language,
            show_log=False
        )

    def _process_image(self, image):
        results = self.engine.ocr(image, cls=True)

        text_parts = []
        confidence_scores = []

        if results and results[0]:
            for line in results[0]:
                if line:
                    text = line[1][0]
                    confidence = line[1][1]
                    text_parts.append(text)
                    confidence_scores.append(confidence)
        average_confidence = (
            (sum(confidence_scores) / len(confidence_scores)) * 100
            if confidence_scores else 0.0
        )

        return {
            'text': '\n'.join(text_parts),
            'average_confidence': round(average_confidence, 4),
            'confidence_scores': confidence_scores
        }
