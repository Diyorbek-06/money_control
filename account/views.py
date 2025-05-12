from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages
from .models import VerificationCode
from django.utils import timezone
from datetime import timedelta
import random


def generate_verification_code():
    return str(random.randint(100000, 999999))


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already in use.')
            return redirect('signup')

        # Foydalanuvchini yaratamiz, ammo hali login qildirmaymiz
        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_active = False  # email tasdiqlanmaguncha aktiv emas
        user.save()

        # VerificationCode yozamiz
        code = generate_verification_code()
        expires = timezone.now() + timedelta(minutes=10)

        VerificationCode.objects.create(email=email, code=code, expires_at=expires)

        # Email yuborish
        subject = 'Email Verification Code'
        message = f'Your verification code is: {code}'
        send_mail(subject, message, 'youremail@gmail.com', [email])

        messages.success(request, 'Verification code sent to your email.')
        return redirect('verify_email')  # bu view quyida yoziladi

    return render(request, 'signup.html')


def verify_email(request):
    if request.method == 'POST':
        email = request.POST['email']
        code = request.POST['code']

        try:
            verification = VerificationCode.objects.get(email=email, code=code)

            if verification.is_expired():
                messages.error(request, 'Verification code has expired.')
                return redirect('verify_email')

            user = User.objects.get(email=email)
            user.is_active = True
            user.save()

            messages.success(request, 'Email successfully verified. You can now log in.')
            return redirect('login')

        except VerificationCode.DoesNotExist:
            messages.error(request, 'Invalid code or email.')
            return redirect('verify_email')

    return render(request, 'verify_email.html')

# Create your views here.
