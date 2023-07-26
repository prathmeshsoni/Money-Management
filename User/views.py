from User.models import Profile
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
import uuid
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.http import JsonResponse


def custom_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.session.get('private_admin'):
            return redirect('/')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper


# Registration Page for User
@custom_login_required
def register_attempt(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            if User.objects.filter(username=username).first():
                a = {'status': True, 'exists': 'existuser'}
                return JsonResponse(a)

            if User.objects.filter(email=email).first():
                a = {'status': True, 'exists': 'existemail'}
                return JsonResponse(a)

            auth_token = str(uuid.uuid4())
            send_mail_after_registration(email, username, auth_token)
            user_obj = User(username=username, email=email)
            user_obj.set_password(password)
            user_obj.save()

            profile_obj = Profile.objects.create(user=user_obj, auth_token=auth_token)
            profile_obj.save()

            a = {'status': True, 'create': 'usercreate', 'u_name': username}
            return JsonResponse(a)

        except:
            a = {'status': False}
            return JsonResponse(a)

    return render(request, 'user/register.html')


# Account Activation Mail Send
def send_mail_after_registration(email, username, token):
    email_template_name = 'user/verifymail.html'
    parameters = {
        'domain': 'money-manager.monarksoni.com/user/verify',
        'token': f'{token}',
        'protocol': 'https',
        'username': f'{username}',

    }
    html_template = render_to_string(email_template_name, parameters)
    subject = 'Registration Complete'

    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]

    message = EmailMessage(subject, html_template, email_from, recipient_list)
    message.content_subtype = 'html'
    message.send()


# After Mail Send Page
@custom_login_required
def token_send(request):
    return render(request, 'user/token_send.html')


# check Email verification
def verify(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()
        user_obj = User.objects.filter(username=profile_obj.user.username).first()

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('/view/')
            profile_obj.is_verified = True
            profile_obj.save()
            user_obj.is_superuser = True
            user_obj.is_staff = True
            user_obj.is_active = True
            user_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('/view/')
    except:
        return redirect('/view/')
