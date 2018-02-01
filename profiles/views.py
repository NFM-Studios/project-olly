from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.views import generic
from django.views.generic import View
from .forms import CreateUserForm, EditProfileForm
from .models import UserProfile
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied
from django.contrib import messages
import requests
from django.conf import settings

from ipware.ip import get_real_ip

#def get_ip(request):
   # ip = get_real_ip(request)
    #if ip is not None:
     #   if user is not None:
      #      user = User.objects.get(username=request.user.username)
       #     user.ip = ip  # change field
        #    user.save() # this will update only


def profile(request, urlusername):
    template_name = 'profiles/profile.html'
    userprofile = UserProfile.objects.get(user__username=urlusername)
    return render(request, template_name, {'userprofile': userprofile, 'requestuser': request.user})

def profile_no_username(request):
    if not (request.user.is_anonymous):
        return redirect('/profile/user/' + str(request.user))
    else:
        return redirect('/login')

def edit_profile(request):
    if request.method == 'POST':
        userprofileobj = UserProfile.objects.get(user__username=request.user.username)
        form = EditProfileForm(request.POST, instance=userprofileobj)
        if form.is_valid():
            form.save()
            return redirect('/profile/user/' + str(request.user))
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
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':account_activation_token.make_token(user),
                })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(
                        mail_subject, message, to=[to_email]
                    )
                email.send()

                messages.success(request, "Please confirm your email")
                return redirect('/login/')

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('profiles:index')

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
        return redirect('/profile')
    else:
        return HttpResponse('Activation link is invalid!')
