import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import User
from professionals.models import ProfessionalProfile
from cases.models import Case

def run():
    print("Seeding database...")
    # Admin
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'adminpass', role=User.Role.ADMIN)
        print("Created admin user (admin / adminpass)")

    # Lawyer
    if not User.objects.filter(username='lawyer1').exists():
        prof_user = User.objects.create_user('lawyer1', 'lawyer1@example.com', 'lawyerpass', role=User.Role.PROFESSIONAL)
        prof_profile = ProfessionalProfile.objects.create(
            user=prof_user,
            role=ProfessionalProfile.ProfessionRole.LAWYER,
            verified=True,
            active=True
        )
        print("Created lawyer user (lawyer1 / lawyerpass)")

    # Psychologist / Counselor
    if not User.objects.filter(username='psychologist1').exists():
        prof_user = User.objects.create_user('psychologist1', 'psychologist1@example.com', 'psychpass', role=User.Role.PROFESSIONAL)
        prof_profile = ProfessionalProfile.objects.create(
            user=prof_user,
            role=ProfessionalProfile.ProfessionRole.COUNSELOR,
            verified=True,
            active=True
        )
        print("Created psychologist user (psychologist1 / psychpass)")

    # Case
    if not Case.objects.exists():
        case = Case.objects.create(
            description="Sample case description for vulnerable individual needing legal advice.",
            status=Case.Status.OPEN
        )
        lawyer_profile = ProfessionalProfile.objects.filter(user__username='lawyer1').first()
        if lawyer_profile:
            case.assigned_professionals.add(lawyer_profile)
        print(f"Created sample case: {case.case_id} (Access Code: {case.access_code})")

    print("Seeding complete.")

if __name__ == '__main__':
    run()
