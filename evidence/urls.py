from django.urls import path
from .views import EvidenceUploadView

urlpatterns = [
    path('upload/', EvidenceUploadView.as_view(), name='evidence-upload'),
]
