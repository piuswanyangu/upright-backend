from rest_framework import serializers
from .models import EvidenceItem

class EvidenceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvidenceItem
        fields = ['id', 'case', 'file', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']
