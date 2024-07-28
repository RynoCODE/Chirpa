from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from groq import Groq
import re
from . models import Question
from django.contrib import messages
from .email_validator import is_valid_email



def verify_otp(request):
    if request.method == "POST":
        otp = request.POST['otp']
        user_id = request.session.get('user_id')
        saved_otp = request.session.get('otp')

        if otp == saved_otp:
            myuser = User.objects.get(id=user_id)
            myuser.is_active = True
            myuser.save()
            messages.success(request, "Your email has been verified successfully.")
            return redirect('signin')
        else:
            messages.error(request, "Invalid OTP, please try again.")
            return redirect('verify_otp')

    return render(request, 'verify_otp.html')


def signin(request):
    return render(request, 'signin.html')



def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if not is_valid_email(email):
            messages.error(request, "Invalid email address.")
            return redirect('/signup')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists!')
            return redirect('/signup')
        
        
        
        
        
        def password_validator(password):
            if len(password) < 8:
                messages.error(request, "Password must be at least 8 characters long.")
                return False
            if not any(char.isupper() for char in password):
                messages.error(request, "Password must contain at least one uppercase letter.")
                return False
            if not any(char.islower() for char in password):
                messages.error(request, "Password must contain at least one lowercase letter.")
                return False
            if not any(char.isdigit() for char in password):
                messages.error(request, "Password must contain at least one digit.")
                return False
            special_characters = r"[!@#$%^&*(),.?\":{}|<>]"
            if not re.search(special_characters, password):
                messages.error(request, "Password must contain at least one special character.")
                return False
            return True
        
        if not password_validator(password):
            return redirect('/signup')
        
        
        myuser = User.objects.create_user( email, password)
        myuser.is_active = False
        myuser.save()    
        messages.success(request, "Your account has been successfully created")  
        totp = pyotp.TOTP(pyotp.random_base32())
        otp = totp.now()
        request.session['otp'] = otp
        request.session['user_id'] = myuser.id  
        subject = 'Your OTP for account verification'
        message = f"Hello we are from chirpa,\nYour OTP for account verification is {otp}.\nThank you for registering.\n "
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        return redirect('verify_otp')

    return render(request, 'signup.html')
