from.models import Scrapping,History
from rest_framework import serializers


class ScrappingSerializers(serializers.ModelSerializer):
    class Meta:
        model=Scrapping
        fields='__all__'


class HistorySerializers(serializers.ModelSerializer):
    class Meta:
        model=History
        fields='__all__'