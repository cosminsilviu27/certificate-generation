from rest_framework import serializers
from .models import ConversionRecord

class ConversionRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversionRecord
        fields = ['user', 'pdf_file', 'timestamp', 'status']  
