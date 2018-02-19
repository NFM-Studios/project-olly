from django.http import HttpResponse
from django.shortcuts import render, redirect, HttpResponseRedirect, resolve_url
from django.contrib.auth import login as auth_login, REDIRECT_FIELD_NAME
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import View
from .forms import CreateUserForm, EditProfileForm
from .models import UserProfile
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode, is_safe_url
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib import messages
import requests
from django.conf import settings
from django.template.response import TemplateResponse
from django.db.models import Q


def login(request, template_name='profiles/login_form.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm,
          current_app=None, extra_context=None):
    """
    Displays the login form and handles the login action.
    """
    redirect_to = request.POST.get(redirect_field_name,
                                   request.GET.get(redirect_field_name, ''))

    if request.method == "POST":
        form = authentication_form(request, data=request.POST)
        if form.is_valid():
            ''' reCAPTCHA validation '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }

            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            ''' End reCAPTCHA validation'''
            if result['success']:
                if not request.POST.get('remember me', None):
                    request.session.set_expiry(0)
                # Ensure the user-originating redirection url is safe.
                if not is_safe_url(url=redirect_to, host=request.get_host()):
                    redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

                # Okay, security check complete. Log the user in.
                auth_login(request, form.get_user())

                return HttpResponseRedirect(redirect_to)
            else:
                messages.error(request, 'Invalid or missing reCAPTCHA. Please try again.')
    else:
        form = authentication_form(request)

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)


def profile(request, urlusername):
    template_name = 'profiles/profile.html'
    userprofile = UserProfile.objects.get(user__username=urlusername)
    return render(request, template_name, {'userprofile': userprofile, 'requestuser': request.user})


def profile_no_username(request):
    if not request.user.is_anonymous:
        userprofile = UserProfile.objects.get(user__username=request.user)
        return render(request, 'profiles/profile.html', {'userprofile': userprofile, 'requestuser': request.user})
    else:
        return redirect('login')


def users(request):
    return render(request, 'profiles/users.html')


def searchusers(request):
    query = request.GET.get('q')
    if query:
        return render(request, 'profiles/users.html',
                      {'userprofiles': UserProfile.objects.filter
                       (Q(user__username__icontains=query) | Q(user__email__icontains=query))})
    else:
        return redirect('profiles:users')


def edit_profile(request):
    if request.method == 'POST':
        userprofileobj = UserProfile.objects.get(user__username=request.user.username)
        form = EditProfileForm(request.POST, instance=userprofileobj)
        if form.is_valid():
            form.save()
            return redirect('profiles:profile_no_username')
    else:
        userprofileobj = UserProfile.objects.get(user__username=request.user.username)
        form = EditProfileForm(instance=userprofileobj)
        return render(request, 'profiles/edit_profile.html', {'form': form})


class CreateUserFormView(View):
    form_class = CreateUserForm
    template_name = 'profiles/registration_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            ''' reCAPTCHA validation '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }

            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            ''' End reCAPTCHA validation'''
            if result['success']:
                user = form.save(commit=False)

                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user.set_password(password)
                user.is_active = False
                user.save()

                current_site = get_current_site(request)

                mail_subject = 'Activate your "Project Olly" account.'
                message = render_to_string('profiles/activate_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(
                        mail_subject, message, to=[to_email]
                    )
                email.send()

                messages.success(request, "Please confirm your email")
                return redirect('login')
            elif not result['success']:
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')

        return render(request, self.template_name, {'form': form})


def activate(request, uidb64, token):
    try:
        a = uidb64.split("'")[1]
        uid = urlsafe_base64_decode(a).decode()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
        print("Exception")
        print(e)
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, 'Thank you for your email confirmation. You are now logged in.')
        return redirect('profiles:profile_no_username')
    else:
        return render(request, 'profiles/activation_invalid.html')
