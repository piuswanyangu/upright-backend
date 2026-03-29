from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import ProfessionalProfile
from cases.models import Case, CaseTimeline
from cases.serializers import CaseSerializer, CaseTimelineSerializer
from evidence.models import EvidenceItem

class ProfessionalDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile = request.user.professional_profile
        except ProfessionalProfile.DoesNotExist:
            return Response({'error': 'Professional profile not found'}, status=403)
        
        assigned_cases = profile.assigned_cases.all().order_by('-created_at')
        active_cases = assigned_cases.filter(status__in=[Case.Status.OPEN, Case.Status.IN_PROGRESS])
        closed_cases = assigned_cases.filter(status=Case.Status.CLOSED)
        
        recent_activity = CaseTimeline.objects.filter(case__in=assigned_cases).order_by('-created_at')[:10]

        return Response({
            'assigned_cases': CaseSerializer(assigned_cases, many=True).data,
            'active_cases_count': active_cases.count(),
            'closed_cases_count': closed_cases.count(),
            'recent_activity': CaseTimelineSerializer(recent_activity, many=True).data
        })

class AdminDashboardView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        total_cases = Case.objects.count()
        active_professionals_qs = ProfessionalProfile.objects.filter(active=True)
        active_professionals = active_professionals_qs.count()
        evidence_uploads = EvidenceItem.objects.count()
        
        open_cases = Case.objects.filter(status=Case.Status.OPEN).count()
        in_progress_cases = Case.objects.filter(status=Case.Status.IN_PROGRESS).count()
        closed_cases = Case.objects.filter(status=Case.Status.CLOSED).count()

        from cases.serializers import CaseSerializer, ProfessionalProfileSerializer

        all_cases = Case.objects.all().order_by('-created_at')
        all_cases_data = CaseSerializer(all_cases, many=True).data
        professionals_data = ProfessionalProfileSerializer(active_professionals_qs, many=True).data

        return Response({
            'total_cases': total_cases,
            'active_professionals': active_professionals,
            'evidence_uploads': evidence_uploads,
            'case_status_statistics': {
                'OPEN': open_cases,
                'IN_PROGRESS': in_progress_cases,
                'CLOSED': closed_cases
            },
            'all_cases': all_cases_data,
            'professionals': professionals_data
        })
