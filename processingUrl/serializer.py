from rest_framework import serializers

from processingUrl.models import Urls


class BaseUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Urls
        fields = '__all__'
