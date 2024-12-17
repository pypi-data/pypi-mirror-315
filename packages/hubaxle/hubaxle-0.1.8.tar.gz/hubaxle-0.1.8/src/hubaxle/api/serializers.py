from rest_framework import serializers
from .models import Secret, CameraConfig

class BaseSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    id = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        abstract = True

class SecretSerializer(BaseSerializer):
    class Meta:
        model = Secret
        fields = '__all__'

class CameraConfigSerializer(BaseSerializer):
    rtsp_url = serializers.CharField(max_length=200)

    class Meta:
        model = CameraConfig
        fields = '__all__'
        read_only_fields = ('name', 'created_at', 'updated_at')