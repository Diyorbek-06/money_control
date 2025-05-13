from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.contrib import messages
from .models import VerificationCode
from django.utils import timezone
from datetime import timedelta
import random
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

User = get_user_model()

def generate_verification_code():
    return str(random.randint(100000, 999999))

@login_required(login_url='account:login')
def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        phone_number = request.POST.get('phone_number', '')

        if password != password2:
            messages.error(request, 'Parollar mos kelmadi.')
            return redirect('account:signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('account:signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already in use.')
            return redirect('account:signup')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_active = False
        user.phone_number = phone_number
        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']
        user.save()

        code = generate_verification_code()
        expires = timezone.now() + timedelta(minutes=5)
        VerificationCode.objects.create(email=email, code=code, expires_at=expires)

        subject = 'Email Verification Code'
        message = f'Your verification code is: {code}'
        send_mail(subject, message, 'diyorbekt146@gmail.com', [email])

        messages.success(request, 'Verification code sent to your email.')
        return redirect('account:verify_email')

    return render(request, 'account/signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Muvaffaqiyatli tizimga kirdingiz.')
            return redirect('transactions:main_page')
        else:
            messages.error(request, 'Login yoki parol noto‘g‘ri.')

    return render(request, 'account/login.html')

def logout_view(request):
    logout(request)
    return redirect('account:login')

def verify_email(request):
    if request.method == 'POST':
        email = request.POST['email']
        code = request.POST['code']

        try:
            verification = VerificationCode.objects.get(email=email, code=code)

            if verification.is_expired():
                messages.error(request, 'Verification code has expired.')
                return redirect('account:verify_email')

            user = User.objects.get(email=email)
            user.is_active = True
            user.save()

            messages.success(request, 'Email successfully verified. You can now log in.')
            return redirect('account:login')

        except VerificationCode.DoesNotExist:
            messages.error(request, 'Invalid code or email.')
            return redirect('account:verify_email')

    return render(request, 'account/verify_email.html')






















# from django.shortcuts import render, redirect
# from django.contrib.auth import get_user_model
# from django.core.mail import send_mail
# from django.contrib import messages
# from .models import VerificationCode
# from django.utils import timezone
# from datetime import timedelta
# import random
# from django.contrib.auth import authenticate, login
# from django.contrib.auth import logout
# from django.contrib.auth.decorators import login_required
#
#
#
# User = get_user_model()
#
# def generate_verification_code():
#     return str(random.randint(100000, 999999))
#
# @login_required(login_url='login')  # Agar foydalanuvchi login qilmagan bo'lsa, login sahifasiga yo'naltiriladi
# def home(request):
#     return render(request, 'home.html')
#
#
# def signup(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         email = request.POST['email']
#         password = request.POST['password']
#         password2 = request.POST['password2']
#
#         if password != password2:
#             messages.error(request, 'Parollar mos kelmadi.')
#             return redirect('signup')
#
#         if User.objects.filter(username=username).exists():
#             messages.error(request, 'Username already exists.')
#             return redirect('signup')
#
#         if User.objects.filter(email=email).exists():
#             messages.error(request, 'Email already in use.')
#             return redirect('signup')
#
#         # Foydalanuvchini yaratamiz, ammo hali login qildirmaymiz
#         user = User.objects.create_user(username=username, email=email, password=password)
#         user.is_active = False  # email tasdiqlanmaguncha aktiv emas
#         user.save()
#
#         # VerificationCode yozamiz
#         code = generate_verification_code()
#         expires = timezone.now() + timedelta(minutes=5)
#
#         VerificationCode.objects.create(email=email, code=code, expires_at=expires)
#
#         # Email yuborish
#         subject = 'Email Verification Code'
#         message = f'Your verification code is: {code}'
#         send_mail(subject, message, 'youremail@gmail.com', [email])
#
#         messages.success(request, 'Verification code sent to your email.')
#         return redirect('verify_email')  # bu view quyida yoziladi
#
#     return render(request, 'signup.html')
#
#
# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             messages.success(request, 'Muvaffaqiyatli tizimga kirdingiz.')
#             return redirect('home')  # o'z sahifangiz nomiga moslang
#         else:
#             messages.error(request, 'Login yoki parol noto‘g‘ri.')
#
#     return render(request, 'account/login.html')
#
# def logout_view(request):
#     logout(request)
#     return redirect('home')
#
# def verify_email(request):
#     if request.method == 'POST':
#         email = request.POST['email']
#         code = request.POST['code']
#
#         try:
#             verification = VerificationCode.objects.get(email=email, code=code)
#
#             if verification.is_expired():
#                 messages.error(request, 'Verification code has expired.')
#                 return redirect('verify_email')
#
#             user = User.objects.get(email=email)
#             user.is_active = True
#             user.save()
#
#             messages.success(request, 'Email successfully verified. You can now log in.')
#             return redirect('login')
#
#         except VerificationCode.DoesNotExist:
#             messages.error(request, 'Invalid code or email.')
#             return redirect('verify_email')
#
#     return render(request, 'verify_email.html')
#


# Create your views here.
