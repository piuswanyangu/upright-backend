from django.urls import path
from .views import ProfessionalDashboardView, AdminDashboardView

urlpatterns = [
    path('professional/', ProfessionalDashboardView.as_view(), name='professional-dashboard'),
    path('admin/', AdminDashboardView.as_view(), name='admin-dashboard'),
]
