from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Case, CaseTimeline
from .serializers import CaseSerializer, CaseTimelineSerializer

class CaseViewSet(viewsets.ModelViewSet):
    queryset = Case.objects.all().order_by('-created_at')
    serializer_class = CaseSerializer

    def get_permissions(self):
        if self.action in ['create', 'access']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        case = serializer.save()
        CaseTimeline.objects.create(
            case=case,
            event_type=CaseTimeline.EventType.CASE_CREATED,
            description="Case was submitted to the platform."
        )

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def access(self, request):
        case_id = request.data.get('case_id')
        access_code = request.data.get('access_code')
        try:
            case = Case.objects.get(case_id=case_id, access_code=access_code)
            serializer = self.get_serializer(case)
            return Response(serializer.data)
        except Case.DoesNotExist:
            return Response({'error': 'Invalid case ID or access code'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def timeline(self, request, pk=None):
        case = self.get_object()
        timeline_events = case.timeline.all().order_by('-created_at')
        serializer = CaseTimelineSerializer(timeline_events, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def assign(self, request, pk=None):
        # Only Admins can assign professionals
        if getattr(request.user, 'role', '') != 'ADMIN':
            return Response({'error': 'Only administrators can assign cases'}, status=status.HTTP_403_FORBIDDEN)
            
        case = self.get_object()
        professional_id = request.data.get('professional_id')
        
        if not professional_id:
            return Response({'error': 'professional_id is required'}, status=status.HTTP_400_BAD_REQUEST)
            
        from professionals.models import ProfessionalProfile
        try:
            professional = ProfessionalProfile.objects.get(id=professional_id)
        except ProfessionalProfile.DoesNotExist:
            return Response({'error': 'Professional not found'}, status=status.HTTP_404_NOT_FOUND)
            
        case.assigned_professionals.add(professional)
        if case.status == case.Status.OPEN:
            case.status = case.Status.IN_PROGRESS
            case.save()
            
        CaseTimeline.objects.create(
            case=case,
            event_type=CaseTimeline.EventType.PROFESSIONAL_ASSIGNED,
            description=f"Case assigned to {professional.get_role_display()} {professional.user.get_full_name() or professional.user.username}"
        )
        
        serializer = self.get_serializer(case)
        return Response(serializer.data)
