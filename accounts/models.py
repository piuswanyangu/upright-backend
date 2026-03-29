from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        PROFESSIONAL = 'PROFESSIONAL', 'Professional'
        
    role = models.CharField(max_length=50, choices=Role.choices, default=Role.ADMIN)

    # Optional: we can add related_name arguments to avoid clashes if need be, 
    # but since this is AUTH_USER_MODEL, Django handles it fine.

    def __str__(self):
        return self.username
