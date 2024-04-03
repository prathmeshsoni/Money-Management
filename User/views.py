import uuid
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.views import PasswordChangeForm, PasswordResetConfirmView
from django.http import JsonResponse
from django.shortcuts import redirect, render

from management.views import get_user_obj, custom_login_required, custom_login_required_not
from .mail import send_mail
from .models import *


# Home Page
def home(request):
    return render(request, 'user/home.html')


# Register User
def register_attempt(request):
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        if not email.endswith('@gmail.com'):
            msg = 'Please Enter Valid Email Address.....!'
            a = {'status': True, 'exists': 'email_error', 'msg': msg}
            return JsonResponse(a)

        if User.objects.filter(username=username).first():
            msg = 'Username Already Exists.....!'
            a = {'status': True, 'exists': 'existuser', 'msg': msg}
            return JsonResponse(a)

        if User.objects.filter(email=email).first():
            msg = 'Email Already Exists.....!'
            a = {'status': True, 'exists': 'existemail', 'msg': msg}
            return JsonResponse(a)

        auth_token = str(uuid.uuid4())
        try:
            create_user(username, email, password, auth_token, 'register')
        except:
            pass

        msg = f'Account Was Created For {username} And Activation Link Was Sent To {email}.....!'
        a = {'status': True, 'exists': 'usercreate', 'u_name': 'username', 'msg': msg}
        return JsonResponse(a)

    else:
        if 'userid' in request.session:
            return redirect('/')
        else:
            return render(request, 'user/register.html', )


# Send Email Verification For Registration
def create_user(username, email, password, auth_token, check):
    sub_domain = 'money-manager'
    site_url = f'http://127.0.0.1:8000/verify/{auth_token}'

    if check == 'register':
        user_obj = User(username=username, email=email)
        user_obj.set_password(password)
        user_obj.save()

        profile_obj = Profile.objects.create(
            user=user_obj,
            auth_token=auth_token,
            is_verified=False
        )
        profile_obj.save()

    send_mail(email, username, username, site_url, password, check, sub_domain)


# Send Email Verification Page
def token_send(request):
    return render(request, 'user/token_send.html')


# Check Email verification
def verify(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()
        user_obj = User.objects.filter(username=profile_obj.user.username).first()

        if profile_obj:
            if not profile_obj.is_verified:
                profile_obj.is_verified = True
                profile_obj.save()
                user_obj.save()

            request.session['private_admin'] = profile_obj.user.username
            request.session['private_id'] = profile_obj.user.id
            request.session['login_time'] = datetime.now().timestamp()

            messages.success(request, 'Account Logged In Successfully ✔')
            return redirect('/view/')
        else:
            return redirect('/register/')
    except:
        return redirect('/')


# Change User Password
@custom_login_required
def change_password(request):
    user_obj = get_user_obj(request)
    if request.method == 'POST':
        form = PasswordChangeForm(user=user_obj, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password Changed Successfully ✔')
            return redirect('/change-password/')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'user/change-password.html', {
        'search': 'search',
        'form': form,
        'password_master': 'master',
        'password_active': 'password_master',
    })


# Reset User Password
@custom_login_required_not
def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email').lower()

        if not email.endswith('@gmail.com'):
            messages.success(request, 'Please Enter Valid Email Address.....!')
            return redirect('/password-reset/')

        if not User.objects.filter(email=email).first():
            messages.success(request, 'Email Not Exists.....!')
            return redirect('/password-reset/')

        obj = User.objects.filter(email=email).first()
        obj_profile = Profile.objects.filter(user=obj).first()

        password = obj.password
        username = obj.username
        auth_token = obj_profile.auth_token
        try:
            create_user(username, email, password, auth_token, 'forgot')
        except:
            pass

        messages.success(request, f'Password Reset Link Was Sent To {email}.....!')
        return redirect('/password-reset/')

    else:
        if 'userid' in request.session:
            return redirect('/')
        else:
            return render(
                request,
                'user/password-forget.html',
                {'cartc': '2'}
            )


# Rest User Password Confirm Message
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request,
                         "Your password has been reset Successfully ✔. You can now log in with your new password. ")
        return response
