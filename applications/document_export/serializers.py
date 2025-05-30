from rest_framework import serializers
from .models import ExportedFile


class ExportInputSerializer(serializers.Serializer):
    format = serializers.ChoiceField(choices=['pdf', 'docx'])


class ExportedOutputFileSerializer(serializers.ModelSerializer):
    download_url = serializers.SerializerMethodField()

    class Meta:
        model = ExportedFile
        fields = ['id', 'file_type', 'download_url', 'created_at']

    def get_download_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(f'/api/v1/file/{obj.pk}/download/')
        return None
