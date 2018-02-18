from django.contrib import messages
from django.shortcuts import render, redirect
from pages.models import StaticInfo
from staff.forms import StaticInfoForm, EditUserForm
from profiles.models import UserProfile, BannedUser
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from support.models import Ticket

def staffindex(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        return render(request, 'staff/staffindex.html')

def users(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:

        object_list = UserProfile.objects.get_queryset().order_by('id')
        paginator = Paginator(object_list, 20)
        page = request.GET.get('page')
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            # if it aint no integer deliver the first page
            users = paginator.page(1)
        except EmptyPage:
            # if the page is out of range deliver last page of results
            users = paginator.page(paginator.num_pages)
        context = {'page': page, 'userprofiles': users,\
                   'bannedusernames': BannedUser.objects.values_list('user', flat=True),\
                   'bannedips': BannedUser.objects.values_list('ip', flat=True)}
        return render(request, 'staff/users.html', context)

def searchusers(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        query = request.GET.get('q')
        if query:
            return render(request, 'staff/users.html',{'userprofiles': UserProfile.objects.filter(Q(user__username__icontains=query) | Q(user__email__icontains=query)), 'bannedusers': list(BannedUser.objects.all())})
        else:
            return redirect('/staff/users')

def edituser(request, urlusername):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        if request.method == 'POST':
            userprofileobj = UserProfile.objects.get(user__username=urlusername)
            form = EditUserForm(request.POST, instance=userprofileobj)
            if form.is_valid():
                form.save()
                messages.success(request, 'User type has been updated')
                return redirect('/staff/users/')
            else:
                print('form is not valid')
        else:
            userprofileobj = UserProfile.objects.get(user__username=urlusername)
            form = EditUserForm(instance=userprofileobj)
            return render(request, 'staff/edituser.html', {'form': form})

def banuser(request, urlusername):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        buser = User.objects.get(username=urlusername)
        b = BannedUser(user=buser, ip='999.999.999.999')
        b.save()
        messages.success(request, 'User ' + urlusername + ' has been banned')
        return redirect('/staff/users')

def unbanuser(request, urlusername):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        buser = User.objects.get(username=urlusername)
        b = BannedUser.objects.get(user=buser)
        b.delete()
        messages.success(request, 'User ' + urlusername + ' has been unbanned')
        return redirect('/staff/users')

def banip(request, urlusername):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        buser = User.objects.get(username=urlusername)
        buserprofile = UserProfile.objects.get(user__username=urlusername)
        b = BannedUser(user=buser, ip=buserprofile.ip)
        b.save()
        messages.success(request, 'User ' + urlusername + ' has been banned')
        return redirect('/staff/users')

def unbanip(request, urlusername):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        buserprofile = UserProfile.objects.get(user__username=urlusername)
        b = BannedUser.objects.get(ip=buserprofile.ip)
        b.delete()
        messages.success(request, 'User ' + urlusername + ' has been banned')
        return redirect('/staff/users')

def tickets(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        tickets = Ticket.objects.all()
        return render(request, 'staff/tickets.html', {'ticket_list': tickets})
    
def staticinfo(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        if request.method == 'POST':
            staticinfoobj = StaticInfo.objects.get(pk=1)
            form = StaticInfoForm(request.POST, instance=staticinfoobj)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your information has been updated')
                return redirect('/staff/staticinfo/')
        else:
            staticinfoobj = StaticInfo.objects.get(pk=1)
            form = StaticInfoForm(instance=staticinfoobj)
            return render(request, 'staff/staticinfo.html', {'form': form})