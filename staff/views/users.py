from staff.auth import staff_required

import ipaddress

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from profiles.tokens import account_activation_token
from profiles.models import BannedUser
from staff.forms import *
from wagers.models import *
from . import tools


@staff_required
def users(request):
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
               'verification': settings.USER_VERIFICATION, 'request': request}
    return render(request, 'staff/profiles/users.html', context)


@staff_required
def searchusers(request):
    query = request.GET.get('q')
    if query:
        return render(request, 'staff/profiles/users.html',
                      {'userprofiles': UserProfile.objects.filter
                      (Q(user__username__icontains=query) | Q(user__email__icontains=query)),
                       'bannedusers': list(BannedUser.objects.all())})
    else:
        return redirect('staff:users')


@staff_required
def banuser(request, urlusername):
    buser = User.objects.get(username=urlusername)
    buserprofile = UserProfile.objects.get(user__username=urlusername)
    try:
        banned_ip = str(ipaddress.ip_address(buserprofile.ip))
    except ValueError:
        messages.error(request, 'User ' + urlusername + ' has a non-bannable IP')
        return redirect('staff:users')
    b = BannedUser(user=buser, ip=banned_ip)
    b.save()
    messages.success(request, 'User ' + urlusername + ' has been banned')
    return redirect('staff:users')


@staff_required
def unbanuser(request, urlusername):
    buser = User.objects.get(username=urlusername)
    b = BannedUser.objects.get(user=buser)
    b.delete()
    messages.success(request, 'User ' + urlusername + ' has been unbanned')
    return redirect('staff:users')


@staff_required
def banip(request, urlusername):
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


@staff_required
def unbanip(request, urlusername):
    buserprofile = UserProfile.objects.get(user__username=urlusername)
    b = BannedUser.objects.get(ip=buserprofile.ip)
    b.delete()
    messages.success(request, 'User ' + urlusername + ' has been banned')
    return redirect('staff:users')


@staff_required
def getrank(request):
    allusers = UserProfile.objects.all()
    tools.calculaterank()
    messages.success(request, "Calculated rank for %s users" % allusers.count())
    return redirect('staff:users')


@staff_required
def reset_xp(request):
    allusers = UserProfile.objects.all()
    for i in allusers:
        i.xp = 0
        i.save()
    messages.success(request, "Reset XP for %s users" % allusers.count())
    return redirect('staff:users')


@staff_required
def modifyuser(request, urlusername):
    if request.method == 'GET':
        userprofileobj = UserProfile.objects.get(user__username=urlusername)
        form = ModifyUserForm(instance=userprofileobj)
        return render(request, 'staff/profiles/user_edit.html', {'form': form})
    else:
        userprofileobj = UserProfile.objects.get(user__username=urlusername)
        form = ModifyUserForm(request.POST, instance=userprofileobj)
        if form.is_valid():
            form.save()
            messages.success(request, 'User has been updated')
            return redirect('staff:users')
        else:
            return render(request, 'staff/profiles/user_edit.html', {'form': form})


@staff_required
def userdetail(request, urlusername):
    if request.method == 'POST':
        userprofile = UserProfile.objects.get(user__username=urlusername)
        userprofile.profile_picture = ''
        userprofile.save()
        messages.success(request, "Removed profile picture")
        return redirect('staff:userdetail', urlusername=urlusername)

    else:
        userprofile = UserProfile.objects.get(user__username=urlusername)
        return render(request, 'staff/profiles/user_detail.html', {'userprofile': userprofile})


@staff_required
def resend_verify_email(request, urlusername):
    # should be a get request
    user = User.objects.get(username=urlusername)
    current_site = get_current_site(request)
    mail_subject = 'Activate your ' + settings.SITE_NAME + ' account.'
    message = render_to_string('profiles/activate_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    to_email = user.email
    email = EmailMessage(
        mail_subject, message, from_email=settings.FROM_EMAIL, to=[to_email]
    )
    email.send()
    messages.success(request, "Resent verification email")
    return redirect('staff:users')


@staff_required
def verify(request, urlusername):
    userprofile = UserProfile.objects.get(user__username=urlusername)
    userprofile.user_verified = not userprofile.user_verified
    userprofile.save()
    return redirect('staff:users')
