from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OCRViewSet

router = DefaultRouter()
router.register(r'', OCRViewSet, basename='ocr')

urlpatterns = router.urls
