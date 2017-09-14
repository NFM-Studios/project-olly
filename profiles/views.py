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

from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied

# Won't be needed after pages app is in place
def index(request):
    return HttpResponse('<h1>PROFILES INDEX</h1>')

def profile(request, urlusername):
    template_name = 'profiles/profile.html'
    userprofile = UserProfile.objects.get(user__username=urlusername)
    return render(request, template_name, {'userprofile': userprofile, 'requestuser': request.user})

def profile_no_username(request):
    return redirect('/profile/user/' + str(request.user))

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
            user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('profiles:index')

        return render(request, self.template_name, {'form': form})
