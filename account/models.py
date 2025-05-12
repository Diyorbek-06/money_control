from django.db import models
from django.utils import timezone
from datetime import timedelta
import random
from django.contrib.auth.models import AbstractUser



class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)  # Avatar maydoni qo'shildi

    def __str__(self):
        return self.username


def generate_verification_code():
    return str(random.randint(100000, 999999))  # 6 xonali raqamli kod

def get_expiry_time():
    return timezone.now() + timedelta(minutes=10)  # 10 daqiqalik tugash vaqti

class VerificationCode(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=6, default=generate_verification_code)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=get_expiry_time)  # lambda o'rniga funksiya ishlatilmoqda

    def __str__(self):
        return f"{self.email} - {self.code}"

    def is_expired(self):
        return timezone.now() > self.expires_at
