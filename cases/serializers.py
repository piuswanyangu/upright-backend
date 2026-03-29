from rest_framework import serializers
from .models import Case, CaseTimeline
from professionals.models import ProfessionalProfile
from accounts.models import User

class ProfessionalProfileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.get_full_name', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = ProfessionalProfile
        fields = ['id', 'name', 'username', 'role', 'verified', 'active']

class CaseSerializer(serializers.ModelSerializer):
    assigned_professionals = ProfessionalProfileSerializer(many=True, read_only=True)

    class Meta:
        model = Case
        fields = ['id', 'case_id', 'access_code', 'description', 'status', 'created_at', 'assigned_professionals']
        read_only_fields = ['id', 'case_id', 'access_code', 'status', 'created_at']

class CaseTimelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseTimeline
        fields = ['id', 'event_type', 'description', 'created_at']
