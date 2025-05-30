from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/ocr/', include('applications.ocr_processing.urls')),
    path('api/v1/file/', include('applications.document_export.urls')),

]
