from rest_framework import serializers

from .models import ConfigEntry


class ConfigEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfigEntry
        fields = "__all__"
        read_only_fields = ("name", "created_at", "updated_at")
