from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from .models import EvidenceItem
from .serializers import EvidenceItemSerializer
from cases.models import CaseTimeline

class EvidenceUploadView(generics.CreateAPIView):
    queryset = EvidenceItem.objects.all()
    serializer_class = EvidenceItemSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        evidence = serializer.save()
        CaseTimeline.objects.create(
            case=evidence.case,
            event_type=CaseTimeline.EventType.EVIDENCE_ADDED,
            description=f"New evidence uploaded: {evidence.file.name.split('/')[-1]}"
        )
