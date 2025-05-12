from django.db import models
from django.utils import timezone
from datetime import timedelta
import random

def generate_verification_code():
    return str(random.randint(100000, 999999))  # 6 xonali raqamli kod

class VerificationCode(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=6, default=generate_verification_code)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=lambda: timezone.now() + timedelta(minutes=10))

    def __str__(self):
        return f"{self.email} - {self.code}"

    def is_expired(self):
        return timezone.now() > self.expires_at

# Create your models here.
