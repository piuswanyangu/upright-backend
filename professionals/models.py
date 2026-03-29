from django.db import models
from accounts.models import User

class ProfessionalProfile(models.Model):
    class ProfessionRole(models.TextChoices):
        LAWYER = 'LAWYER', 'Lawyer'
        COUNSELOR = 'COUNSELOR', 'Counselor'
        MEDIATOR = 'MEDIATOR', 'Mediator'
        FINANCIAL_ADVISOR = 'FINANCIAL_ADVISOR', 'Financial Advisor'
        
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='professional_profile')
    role = models.CharField(max_length=50, choices=ProfessionRole.choices)
    verified = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"
