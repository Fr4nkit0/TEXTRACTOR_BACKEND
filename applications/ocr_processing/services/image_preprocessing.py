import cv2
import numpy as np
from PIL import Image, ImageEnhance

# Mejorar esta Clase


class ImagePreprocessor:
    @staticmethod
    def preprocess_image(image, config=None):
        """
        Preprocesa la imagen según la configuración especificada
        """
        if config is None:
            config = {}

        # Convertir PIL Image a numpy array
        if isinstance(image, Image.Image):
            img_array = np.array(image)
        else:
            img_array = image

        # Convertir a RGB si es necesario
        if len(img_array.shape) == 3:
            img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

        # Grayscale (si se requiere)
        if config.get('grayscale', False):
            img_array = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
            # Convertir a BGR de nuevo para mantener consistencia
            img_array = cv2.cvtColor(img_array, cv2.COLOR_GRAY2BGR)

        # Rotar imagen
        if 'rotate' in config:
            angle = config['rotate']
            (h, w) = img_array.shape[:2]
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            img_array = cv2.warpAffine(img_array, M, (w, h))

        # Crop (recortar)
        if 'crop' in config:
            c = config['crop']
            x, y = c['x'], c['y']
            w, h = c['width'], c['height']
            img_array = img_array[y:y+h, x:x+w]

        # Aplicar preprocesamiento
        if config.get('resize'):
            img_array = ImagePreprocessor._resize(img_array, config['resize'])

        if config.get('enhance_contrast', False):
            img_array = ImagePreprocessor._enhance_contrast(img_array)

        if config.get('binarization', False):
            img_array = ImagePreprocessor._binarize(img_array)

        if config.get('noise_reduction', False):
            img_array = ImagePreprocessor._reduce_noise(img_array)

        if config.get('threshold'):
            img_array = ImagePreprocessor._apply_threshold(
                img_array, config['threshold'])

        return img_array

    @staticmethod
    def _resize(image, size_config):
        """Redimensionar imagen"""
        if isinstance(size_config, dict):
            width = size_config.get('width')
            height = size_config.get('height')
            if width and height:
                return cv2.resize(image, (width, height))
        return image

    @staticmethod
    def _enhance_contrast(image):
        """Mejorar contraste"""
        # Convertir a PIL para mejorar contraste
        pil_img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        enhancer = ImageEnhance.Contrast(pil_img)
        enhanced = enhancer.enhance(1.5)
        return cv2.cvtColor(np.array(enhanced), cv2.COLOR_RGB2BGR)

    @staticmethod
    def _binarize(image):
        """Binarización de imagen"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(
            gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)

    @staticmethod
    def _reduce_noise(image):
        """Reducir ruido"""
        return cv2.bilateralFilter(image, 9, 75, 75)

    @staticmethod
    def _apply_threshold(image, threshold_config):
        """Aplicar threshold personalizado"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thresh_value = threshold_config.get('value', 127)
        max_value = threshold_config.get('max_value', 255)
        thresh_type = getattr(
            cv2, threshold_config.get('type', 'THRESH_BINARY'))

        _, threshed = cv2.threshold(gray, thresh_value, max_value, thresh_type)
        return cv2.cvtColor(threshed, cv2.COLOR_GRAY2BGR)
