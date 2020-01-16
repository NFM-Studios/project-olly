from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect

from profiles.models import BannedUser
from staff.forms import *
from wagers.models import *
from . import tools


def users(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        object_list = UserProfile.objects.get_queryset().order_by('id')
        paginator = Paginator(object_list, 20)
        numusers = len(UserProfile.objects.all())
        page = request.GET.get('page')
        try:
            list_users = paginator.page(page)
        except PageNotAnInteger:
            # if it aint no integer deliver the first page
            list_users = paginator.page(1)
        except EmptyPage:
            # if the page is out of range deliver last page of results
            list_users = paginator.page(paginator.num_pages)
        context = {'page': page, 'userprofiles': list_users,
                   'bannedusernames': BannedUser.objects.values_list('user', flat=True),
                   'bannedips': BannedUser.objects.values_list('ip', flat=True), 'numusers': numusers,
                   'request': request}
        return render(request, 'staff/profiles/users.html', context)


def searchusers(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        query = request.GET.get('q')
        if query:
            return render(request, 'staff/profiles/users.html',
                          {'userprofiles': UserProfile.objects.filter
                          (Q(user__username__icontains=query) | Q(user__email__icontains=query)),
                           'bannedusers': list(BannedUser.objects.all())})
        else:
            return redirect('staff:users')


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
        return redirect('staff:users')


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
        return redirect('staff:users')


def banip(request, urlusername):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        buser = User.objects.get(username=urlusername)
        buserprofile = UserProfile.objects.get(user__username=urlusername)
        if (buserprofile.ip == '127.0.0.1') or (buserprofile.ip == '0.0.0.0') or (buserprofile.ip == '999.999.999.999'):
            messages.error(request, 'User has non-bannable IP')
            return redirect('staff:users')
        else:
            b = BannedUser(user=buser, ip=buserprofile.ip)
            b.save()
            messages.success(request, 'User ' + urlusername + ' has been banned')
            return redirect('staff:users')


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
        return redirect('staff:users')


def getrank(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        allusers = UserProfile.objects.all()
        tools.calculaterank()
        messages.success(request, "Calculated rank for %s users" % allusers.count())
        return redirect('staff:users')


def reset_xp(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        allusers = UserProfile.objects.all()
        for i in allusers:
            i.xp = 0
            i.save()
        messages.success(request, "Reset XP for %s users" % allusers.count())
        return redirect('staff:users')


def modifyuser(request, urlusername):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        if request.method == 'GET':
            userprofileobj = UserProfile.objects.get(user__username=urlusername)
            form = ModifyUserForm(instance=userprofileobj)
            return render(request, 'staff/profiles/modifyuser.html', {'form': form})
        else:
            userprofileobj = UserProfile.objects.get(user__username=urlusername)
            form = ModifyUserForm(request.POST, instance=userprofileobj)
            if form.is_valid():
                form.save()
                messages.success(request, 'User has been updated')
                return redirect('staff:users')


def userdetail(request, urlusername):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        if request.method == 'POST':
            userprofile = UserProfile.objects.get(user__username=urlusername)
            userprofile.profile_picture = ''
            userprofile.save()
            messages.success(request, "Removed profile picture")
            return redirect('staff:userdetail', urlusername=urlusername)

        else:
            userprofile = UserProfile.objects.get(user__username=urlusername)
            return render(request, 'staff/profiles/profile_detail.html', {'userprofile': userprofile})


def verify(request, urlusername):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        userprofile = UserProfile.objects.get(user__username=urlusername)
        userprofile.user_verified = not userprofile.user_verified
        userprofile.save()
        return redirect('staff:users')
