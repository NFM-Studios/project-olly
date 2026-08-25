import requests
from django import forms
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import (
    LoginView as DjangoLoginView,
    LogoutView as DjangoLogoutView,
    PasswordResetView as DjangoPasswordResetView,
    PasswordResetDoneView as DjangoPasswordResetDoneView,
    PasswordResetConfirmView as DjangoPasswordResetConfirmView,
    PasswordResetCompleteView as DjangoPasswordResetCompleteView,
)
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import View
from teams.models import TeamInvite
from .forms import CreateUserForm, EditProfileForm, SortForm
from .models import UserProfile, Notification
from .tokens import account_activation_token


class LoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False)


class LoginView(DjangoLoginView):
    template_name = 'profiles/login_form.html'
    authentication_form = LoginForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_key'] = settings.GOOGLE_RECAPTCHA_SITE_KEY
        return context

    def form_valid(self, form):
        ''' reCAPTCHA validation '''
        recaptcha_response = self.request.POST.get('g-recaptcha-response')
        data = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }

        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()

        ''' End reCAPTCHA validation'''
        if not result['success']:
            messages.error(self.request, 'Invalid or missing reCAPTCHA. Please try again.')
            return self.form_invalid(form)

        # If the "remember me" checkbox is not checked, the session cookie
        # expires when the browser closes instead of after SESSION_COOKIE_AGE.
        if not form.cleaned_data.get('remember_me'):
            self.request.session.set_expiry(0)

        return super().form_valid(form)


class LogoutView(DjangoLogoutView):
    # Django 4.2's LogoutView only accepts POST, but the site templates link
    # to /logout/ with a plain GET anchor, so accept both.
    http_method_names = ["get", "post", "options"]

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class PasswordResetView(DjangoPasswordResetView):
    template_name = 'profiles/reset_form.html'
    email_template_name = 'profiles/reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    from_email = settings.FROM_EMAIL


class PasswordResetDoneView(DjangoPasswordResetDoneView):
    template_name = 'profiles/reset_done.html'


class PasswordResetConfirmView(DjangoPasswordResetConfirmView):
    template_name = 'profiles/reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')


class PasswordResetCompleteView(DjangoPasswordResetCompleteView):
    template_name = 'profiles/reset_complete.html'


def profile(request, urlusername):
    userprofile = get_object_or_404(UserProfile, user__username=urlusername)
    # following line is not stock olly
    return render(request, 'profiles/profile.html',
                  {'userprofile': userprofile, 'requestuser': request.user})


def profile_no_username(request):
    if not request.user.is_anonymous:
        userprofile = UserProfile.objects.get(user__username=request.user)
        team_list = TeamInvite.objects.filter(accepted=True, user=request.user)
        return render(request, 'profiles/profile.html',
                      {'userprofile': userprofile, 'requestuser': request.user, "team_list": team_list})
    else:
        return redirect('login')


def users(request):
    return render(request, 'profiles/users.html')


def searchusers(request):
    query = request.GET.get('q')
    if query:
        return render(request, 'profiles/users.html',
                      {'userprofiles': UserProfile.objects.filter
                      (Q(user__username__icontains=query) | Q(user__email__icontains=query) |
                       Q(psn__icontains=query) | Q(xbl__icontains=query))})
    else:
        return redirect('profiles:users')


def edit_profile(request):
    if request.method == 'POST':
        userprofileobj = UserProfile.objects.get(user__username=request.user.username)
        form = EditProfileForm(request.POST, request.FILES, instance=userprofileobj)
        if form.is_valid():
            user = request.user
            if form.cleaned_data['first_name'] != '':
                user.first_name = form.cleaned_data['first_name']
            if form.cleaned_data['last_name'] != '':
                user.last_name = form.cleaned_data['last_name']
            user.save()
            form.save()
            messages.success(request, "Profile updated successfully")
            return redirect('profiles:profile_no_username')
        else:
            return render(request, 'profiles/edit_profile.html', {'form': form, 'userprofile': userprofileobj})
    else:
        userprofileobj = UserProfile.objects.get(user__username=request.user.username)
        form = EditProfileForm(instance=userprofileobj)
        return render(request, 'profiles/edit_profile.html', {'form': form, 'userprofile': userprofileobj})


class CreateUserFormView(View):
    form_class = CreateUserForm

    def get(self, request):
        if request.user.is_anonymous:
            form = self.form_class(None)
            return render(request, 'profiles/registration_form.html',
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
                    message = render_to_string('profiles/activate_email.html', {
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
                    messages.success(request, "Signup success! Please confirm your email to activate your account!")
                    return redirect('login')
                elif not result['success']:
                    messages.error(request, 'Invalid reCAPTCHA. Please try again.')

            if User.objects.filter(username=form.data['username']).exists():
                messages.error(request, 'That username already exists')
                return redirect('register')
            return render(request, 'profiles/registration_form.html', {'form': form})
        else:
            messages.error(request, "You cannot register while logged in")
            return redirect('index')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        # a = uidb64.split("'")[1]
        # uid = urlsafe_base64_decode(a).decode()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
        print("Exception")
        print(e)
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth_login(request, user)
        messages.success(request, 'Thank you for your email confirmation. Your account is now activated and you are now logged in.')
        return redirect('profiles:profile_no_username')
    else:
        return render(request, 'profiles/activate_invalid.html')


class LeaderboardView(View):
    form_class = SortForm

    def get(self, request, **kwargs):
        user_list = UserProfile.objects.order_by('rank')  # sort by rank default
        form = self.form_class(None)
        return render(request, 'teams/leaderboard.html', {'user_list': user_list, 'form': form})

    def post(self, request, **kwargs):
        form = self.form_class(request.POST)
        if not form.is_valid():
            user_list = UserProfile.objects.order_by('-xp')
            messages.error(request, 'No sort option selected, sorting by descending xp')
            return render(request, 'teams/leaderboard.html',
                          {'user_list': user_list, 'form': self.form_class(None)})
        if form.cleaned_data['sort_xp_asc']:
            user_list = UserProfile.objects.order_by('xp')
            messages.success(request, "Sorted by ascending XP")
            return render(request, 'teams/leaderboard.html',
                          {'user_list': user_list, 'form': self.form_class(None)})
        elif form.cleaned_data['sort_xp_desc']:
            user_list = UserProfile.objects.order_by('-xp')
            messages.success(request, "Sorted by descending XP")
            return render(request, 'teams/leaderboard.html',
                          {'user_list': user_list, 'form': self.form_class(None)})
        elif form.cleaned_data['sort_trophies_asc']:
            user_list = UserProfile.objects.order_by('num_trophies')
            messages.success(request, "Sorted by ascending number of trophies")
            return render(request, 'teams/leaderboard.html',
                          {'user_list': user_list, 'form': self.form_class(None)})
        elif form.cleaned_data['sort_trophies_desc']:
            user_list = UserProfile.objects.order_by('-num_trophies')
            messages.success(request, "Sorted by descending number of trophies")
            return render(request, 'teams/leaderboard.html',
                          {'user_list': user_list, 'form': self.form_class(None)})
        elif form.cleaned_data['sort_rank_asc']:
            user_list = UserProfile.objects.order_by('rank')
            messages.success(request, "Sorted by ascending rank")
            return render(request, 'teams/leaderboard.html',
                          {'user_list': user_list, 'form': self.form_class(None)})
        elif form.cleaned_data['sort_rank_desc']:
            user_list = UserProfile.objects.order_by('-rank')
            messages.success(request, "Sorted by descending rank")
            return render(request, 'teams/leaderboard.html',
                          {'user_list': user_list, 'form': self.form_class(None)})
        else:
            user_list = UserProfile.objects.order_by('-xp')
            messages.error(request, 'No sort option selected, sorting by descending xp')
            return render(request, 'teams/leaderboard.html',
                          {'user_list': user_list, 'form': self.form_class(None)})


def notifications_list(request):
    if request.user.is_anonymous:
        messages.error(request, 'You must be signed in to view your notifications')
        return redirect('index')
    else:
        profile = UserProfile.objects.get(user=request.user)
        notifications = profile.notifications.all().filter(read=False)
        read = profile.notifications.all().filter(read=True)
        for x in profile.notifications.all():
            x.seen = True
            x.save()
        return render(request, 'profiles/notifications_list.html',
                      {'profile': profile, 'notifications': notifications, 'read': read})


def notification_read(request, pk):
    try:
        notif = Notification.objects.get(pk=pk)
        notif.read = True
        notif.save()
    except ObjectDoesNotExist:
        messages.error(request, 'Error marking notification as read')
    return redirect('profiles:notifications')


def notification_unread(request, pk):
    try:
        notif = Notification.objects.get(pk=pk)
        notif.read = False
        notif.save()
    except ObjectDoesNotExist:
        messages.error(request, 'Error marking notification as unread')
    return redirect('profiles:notifications')
