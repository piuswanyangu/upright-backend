from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from cases.models import Case
from django.core.mail import send_mail
from django.conf import settings
from professionals.models import ProfessionalProfile

@receiver(post_save, sender=Case)
def notify_admin_new_case(sender, instance, created, **kwargs):
    if created:
        print(f"DEBUG EMAIL: New case submitted! Case ID: {instance.case_id}")

@receiver(m2m_changed, sender=Case.assigned_professionals.through)
def notify_professional_assigned(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        professionals = ProfessionalProfile.objects.filter(pk__in=pk_set)
        for prof in professionals:
            email = prof.user.email
            print(f"DEBUG EMAIL: Assigned to case! To: {email}, Case ID: {instance.case_id}")
