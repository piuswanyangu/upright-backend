import uuid
import random
import string
from django.db import models

class Case(models.Model):
    class Status(models.TextChoices):
        OPEN = 'OPEN', 'Open'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        CLOSED = 'CLOSED', 'Closed'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    case_id = models.CharField(max_length=20, unique=True, blank=True)
    access_code = models.CharField(max_length=20, blank=True)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    created_at = models.DateTimeField(auto_now_add=True)
    assigned_professionals = models.ManyToManyField('professionals.ProfessionalProfile', related_name='assigned_cases', blank=True)

    def save(self, *args, **kwargs):
        if not self.case_id:
            self.case_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        if not self.access_code:
            self.access_code = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.case_id


class CaseTimeline(models.Model):
    class EventType(models.TextChoices):
        CASE_CREATED = 'CASE_CREATED', 'Case Created'
        EVIDENCE_ADDED = 'EVIDENCE_ADDED', 'Evidence Added'
        PROFESSIONAL_ASSIGNED = 'PROFESSIONAL_ASSIGNED', 'Professional Assigned'
        STATUS_CHANGED = 'STATUS_CHANGED', 'Status Changed'
    
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='timeline')
    event_type = models.CharField(max_length=50, choices=EventType.choices)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.case.case_id} - {self.get_event_type_display()}"
