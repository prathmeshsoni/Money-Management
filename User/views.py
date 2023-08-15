import uuid

from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetConfirmView
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from management.views import custom_login_required_not, sent_massages
from wallet.config import *
from .models import *


# Registration Page for User
@custom_login_required_not
def register_attempt(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # try:
        if User.objects.filter(username=username).first():
            a = {'status': True, 'exists': 'existuser'}
            return JsonResponse(a)

        if User.objects.filter(email=email).first():
            a = {'status': True, 'exists': 'existemail'}
            return JsonResponse(a)

        auth_token = str(uuid.uuid4())
        user_obj = User(username=username, email=email)
        user_obj.set_password(password)
        user_obj.save()

        profile_obj = Profile.objects.create(user=user_obj, auth_token=auth_token)
        profile_obj.save()
        request.session['test_user'] = username
        a = {'status': True, 'create': 'usercreate', 'u_name': username}
        return JsonResponse(a)

    return render(request, 'user/register-1.html')


@custom_login_required_not
def send_email_(request):
    if request.method == 'POST':
        check = request.session.get('test_user')
        if check:
            del request.session['test_user']
            username = check
            profile_obj = Profile.objects.get(user__username=username)
            if not profile_obj.is_verified:
                token = profile_obj.auth_token
                receiver_email = profile_obj.user.email
                subject = 'Registration Complete'
                email_template_name = 'user/verifymail.html'
                parameters = {
                    'domain': 'money-manager.monarksoni.com/verify',
                    'token': f'{token}',
                    'protocol': 'https',
                    'username': f'{username}',

                }
                html_template = render_to_string(email_template_name, parameters)

                try:
                    sent_massages(f'Registration ::\n\n https://money-manager.monarksoni.com/verify/{token}')
                    # send_mail(
                    #     subject=subject,
                    #     message='',  # Since you're using an HTML template, message can be empty
                    #     from_email=sender_email,
                    #     recipient_list=[receiver_email],
                    #     fail_silently=False,
                    #     html_message=html_template,
                    #     auth_user=sender_email,
                    #     auth_password=sender_password,
                    # )
                except:
                    pass

        a = {'status': True}
        return JsonResponse(a)
    else:
        return redirect('/register/')


# After Mail Send Page
@custom_login_required_not
def token_send(request):
    return render(request, 'user/password_reset_done.html')


# check Email verification
def verify(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()
        user_obj = User.objects.filter(username=profile_obj.user.username).first()

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified ✔.')
                return redirect('/')
            profile_obj.is_verified = True
            profile_obj.save()
            user_obj.is_superuser = True
            user_obj.is_staff = True
            user_obj.is_active = True
            user_obj.save()
            messages.success(request, 'Your account has been verified ✔.')
            return redirect('/')
    except:
        return redirect('/')


@custom_login_required_not
# Forgot Password Page
def forget_password(request):
    if request.method == 'POST':
        password_form = PasswordResetForm(request.POST)
        if password_form.is_valid():
            data = password_form.cleaned_data['email']
            user_obj = User.objects.filter(email=data)
            if user_obj.exists():
                user_obj = user_obj.first()
                subject = "Password Request"
                email_template_name = 'password_reset_email.html'
                parameters = {
                    'email': user_obj.email,
                    'username': user_obj.username,
                    'domain': 'money-manager.monarksoni.com',
                    'uid': urlsafe_base64_encode(force_bytes(user_obj.pk)),
                    'token': default_token_generator.make_token(user_obj),
                    'protocol': 'https',
                }
                html_template = render_to_string(email_template_name, parameters)
                receiver_email = data

                try:
                    sent_massages(
                        f'Forget Password ::\n\n https://money-manager.monarksoni.com/password-reset-confirm/{parameters["uid"]}/{parameters["token"]}/')

                    send_mail(
                        subject=subject,
                        message='',  # Since you're using an HTML template, message can be empty
                        from_email=sender_email,
                        recipient_list=[receiver_email],
                        fail_silently=False,
                        html_message=html_template,
                        auth_user=sender_email,
                        auth_password=sender_password,
                    )
                except:
                    pass

                return render(request, 'password_reset_done.html')
            else:
                messages.success(request, "Email Address Not Found.")
                return redirect('/password-reset/')
    else:
        password_form = PasswordResetForm()
        context = {
            'password_form': password_form,
        }
    return render(request, 'password_reset_form.html', context)


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy('login')  # Replace with your desired success URL

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request,
                         "Your password has been reset Successfully ✔. You can now log in with your new password. ")
        return response
