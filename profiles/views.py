from django.http import HttpResponse
from django.shortcuts import render, redirect, HttpResponseRedirect, resolve_url, get_object_or_404
from django.contrib.auth import login as auth_login, REDIRECT_FIELD_NAME, logout as auth_logout, get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, PasswordChangeForm, SetPasswordForm
from django.views.generic import View
from django.contrib.auth.tokens import default_token_generator
from .forms import CreateUserForm, EditProfileForm, SortForm
from .models import UserProfile
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode, is_safe_url
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib import messages
import requests
from django.conf import settings
from django.template.response import TemplateResponse
from django.db.models import Q
from teams.models import Team, TeamInvite
from django.urls import reverse


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
            messages.error(request, message='Error trying to log you in')

    else:
        form = authentication_form(request)

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
        'site_key': settings.GOOGLE_RECAPTCHA_SITE_KEY
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, 'profiles/' + request.tenant + '/login_form.html', context)


def logout(request, next_page=None,
           redirect_field_name=REDIRECT_FIELD_NAME,
           current_app=None, extra_context=None):
    """
    Logs out the user and displays 'You are logged out' message.
    """
    auth_logout(request)

    if next_page is not None:
        next_page = resolve_url(next_page)

    if (redirect_field_name in request.POST or
            redirect_field_name in request.GET):
        next_page = request.POST.get(redirect_field_name,
                                     request.GET.get(redirect_field_name))
        # Security check -- don't allow redirection to a different host.
        if not is_safe_url(url=next_page, host=request.get_host()):
            next_page = request.path

    if next_page:
        # Redirect to this page until the session has been cleared.
        return HttpResponseRedirect(next_page)

    current_site = get_current_site(request)
    context = {
        'site': current_site,
        'site_name': current_site.name,
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return redirect('index')


def password_reset(request, is_admin_site=False,
                   subject_template_name='registration/password_reset_subject.txt',
                   password_reset_form=PasswordResetForm,
                   token_generator=default_token_generator,
                   post_reset_redirect=None,
                   from_email=None,
                   current_app=None,
                   extra_context=None,
                   html_email_template_name=None):
    if post_reset_redirect is None:
        post_reset_redirect = reverse('password_reset_done')
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)
    if request.method == "POST":
        form = password_reset_form(request.POST)
        if form.is_valid():
            opts = {
                'use_https': request.is_secure(),
                'token_generator': token_generator,
                'from_email': from_email,
                'email_template_name': 'profiles/' + request.tenant + '/reset_email.html',
                'subject_template_name': subject_template_name,
                'request': request,
                'html_email_template_name': html_email_template_name,
            }
            if is_admin_site:
                opts = dict(opts, domain_override=request.get_host())
            form.save(**opts)
            return HttpResponseRedirect(post_reset_redirect)
    else:
        form = password_reset_form()
    context = {
        'form': form,
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, 'profiles/' + request.tenant + '/reset_form.html', context)


def password_reset_done(request, current_app=None, extra_context=None):
    context = {

    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, 'profiles/' + request.tenant + '/reset_done.html', context)


def password_reset_confirm(request, uidb64=None, token=None,
                           token_generator=default_token_generator,
                           set_password_form=SetPasswordForm,
                           post_reset_redirect=None,
                           current_app=None, extra_context=None):
    """
    View that checks the hash in a password reset link and presents a
    form for entering a new password.
    """
    UserModel = get_user_model()
    assert uidb64 is not None and token is not None  # checked by URLconf
    if post_reset_redirect is None:
        post_reset_redirect = reverse('password_reset_complete')
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)
    try:
        # urlsafe_base64_decode() decodes to bytestring on Python 3
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserModel._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        validlink = True
        if request.method == 'POST':
            form = set_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(post_reset_redirect)
        else:
            form = set_password_form(user)
    else:
        validlink = False
        form = None
    context = {
        'form': form,
        'validlink': validlink,
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, 'profiles/' + request.tenant + '/reset_confirm.html', context)


def password_reset_complete(request, current_app=None, extra_context=None):
    context = {
        'login_url': resolve_url(settings.LOGIN_URL),
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, 'profiles/' + request.tenant + '/reset_complete.html', context)


def profile(request, urlusername):
    userprofile = get_object_or_404(UserProfile, user__username=urlusername)
    # following line is not stock olly
    team_list = TeamInvite.objects.filter(accepted=True, user=userprofile.user)
    return render(request, 'profiles/' + request.tenant + '/profile.html', {'userprofile': userprofile, 'requestuser': request.user, "team_list": team_list})


def profile_no_username(request):
    if not request.user.is_anonymous:
        userprofile = UserProfile.objects.get(user__username=request.user)
        team_list = TeamInvite.objects.filter(accepted=True, user = request.user)
        return render(request, 'profiles/' + request.tenant + '/profile.html', {'userprofile': userprofile, 'requestuser': request.user, "team_list": team_list})
    else:
        return redirect('login')


def users(request):
    return render(request, 'profiles/' + request.tenant + '/users.html')


def searchusers(request):
    query = request.GET.get('q')
    if query:
        return render(request, 'profiles/' + request.tenant + '/users.html',
                      {'userprofiles': UserProfile.objects.filter
                       (Q(user__username__icontains=query) | Q(user__email__icontains=query))})
    else:
        return redirect('profiles:users')


def edit_profile(request):
    if request.method == 'POST':
        userprofileobj = UserProfile.objects.get(user__username=request.user.username)
        form = EditProfileForm(request.POST, request.FILES, instance=userprofileobj)
        if form.is_valid():
            if form.cleaned_data['xbl'] != "No Xbox Live Linked":
                userprofileobj.xbl_verified = True
                userprofileobj.save()
            if form.cleaned_data['psn'] != "No PSN Linked":
                userprofileobj.psn_verified = True
                userprofileobj.save()
            form.save()
            return redirect('profiles:profile_no_username')
    else:
        userprofileobj = UserProfile.objects.get(user__username=request.user.username)
        form = EditProfileForm(instance=userprofileobj)
        return render(request, 'profiles/' + request.tenant + '/edit_profile.html', {'form': form})


class CreateUserFormView(View):
    form_class = CreateUserForm

    def get(self, request):
        if request.user.is_anonymous:
            form = self.form_class(None)
            return render(request, 'profiles/' + request.tenant + '/registration_form.html',
                          {'form': form, 'site_key': settings.GOOGLE_RECAPTCHA_SITE_KEY})
        else:
            messages.error(request, "You cannot register while logged in")
            return redirect('index')

    def post(self, request):
        if request.user.is_anonymous:
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
                    email_address = form.cleaned_data['email']
                    if User.objects.filter(email=email_address).exists():
                        messages.error(request, 'That email address already exists')
                        return redirect('register')
                    password = form.cleaned_data['password']
                    password_confirm = form.cleaned_data['password_confirm']
                    if password != password_confirm:
                        messages.error(request, 'Passwords must match')
                        return redirect('register')
                    user.set_password(password)
                    user.is_active = False
                    user.save()

                    current_site = get_current_site(request)

                    mail_subject = 'Activate your ' + settings.SITE_NAME + ' account.'
                    message = render_to_string('profiles/' + request.tenant + '/activate_email.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': account_activation_token.make_token(user),
                    })
                    to_email = email_address
                    email = EmailMessage(
                            mail_subject, message, from_email=settings.FROM_EMAIL, to=[to_email]
                        )
                    email.send()
                    messages.success(request, "Please confirm your email")
                    return redirect('login')
                elif not result['success']:
                    messages.error(request, 'Invalid reCAPTCHA. Please try again.')

            if User.objects.filter(username=form.data['username']).exists():
                messages.error(request, 'That username already exists')
                return redirect('register')
            return render(request, 'profiles/' + request.tenant + '/registration_form.html', {'form': form})
        else:
            messages.error(request, "You cannot register while logged in")
            return redirect('index')


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
        auth_login(request, user)
        messages.success(request, 'Thank you for your email confirmation. You are now logged in.')
        return redirect('profiles:profile_no_username')
    else:
        return render(request, 'profiles/' + request.tenant + '/activation_invalid.html')


class LeaderboardView(View):
    form_class = SortForm

    def get(self, request, **kwargs):
        user_list = UserProfile.objects.order_by('user__username')  # sort by username default
        form = self.form_class(None)
        return render(request, 'teams/' + request.tenant + '/leaderboard.html', {'user_list': user_list, 'form': form})

    def post(self, request, **kwargs):
        form = self.form_class(request.POST)
        form.is_valid()
        if form.cleaned_data['sort_xp_asc']:
            user_list = UserProfile.objects.order_by('xp')
            messages.success(request, "Sorted by ascending XP")
            return render(request, 'teams/' + request.tenant + '/leaderboard.html', {'user_list': user_list, 'form': self.form_class(None)})
        elif form.cleaned_data['sort_xp_desc']:
            user_list = UserProfile.objects.order_by('-xp')
            messages.success(request, "Sorted by descending XP")
            return render(request, 'teams/' + request.tenant + '/leaderboard.html', {'user_list': user_list, 'form': self.form_class(None)})
        elif form.cleaned_data['sort_trophies_asc']:
            user_list = UserProfile.objects.order_by('num_trophies')
            messages.success(request, "Sorted by ascending number of trophies")
            return render(request, 'teams/' + request.tenant + '/leaderboard.html', {'user_list': user_list, 'form': self.form_class(None)})
        elif form.cleaned_data['sort_trophies_desc']:
            user_list = UserProfile.objects.order_by('-num_trophies')
            messages.success(request, "Sorted by descending number of trophies")
            return render(request, 'teams/' + request.tenant + '/leaderboard.html', {'user_list': user_list, 'form': self.form_class(None)})
        else:
            user_list = UserProfile.objects.order_by('user__username')
            messages.error(request, 'No sort option selected, sorting by username')
            return render(request, 'teams/' + request.tenant + '/leaderboard.html', {'user_list': user_list, 'form': self.form_class(None)})
