from django.contrib import messages
from django.shortcuts import render, redirect

from staff.forms import *
from support.models import Ticket
from wagers.models import *


def staffindex(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        ticket = Ticket.objects.filter(Q(status=0) | Q(status=1) | Q(status=2))
        numtickets = len(ticket)
        news = Post.objects.all()
        teams = Team.objects.all()
        numusers = len(UserProfile.objects.all())
        tournaments = SingleEliminationTournament.objects.all()
        numdisputes = len(Match.objects.filter(disputed=True))
        return render(request, 'staff/staffindex.html', {'ticket': ticket, 'news': news, 'teams': teams,
                                                         'tournaments': tournaments, 'numusers': numusers,
                                                         'numtickets': numtickets, 'numdisputes': numdisputes})


# start static info section


def pages(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        if request.method == 'POST':
            staticinfoobj = StaticInfo.objects.get(pk=1)
            socialinfoobj = SocialInfo.objects.get(pk=1)
            static = StaticInfoForm(request.POST, request.FILES, instance=staticinfoobj)
            social = SocialInfoForm(request.POST, instance=socialinfoobj)
            if static.is_valid() and social.is_valid():
                static.save()
                social.save()
                messages.success(request, 'Your information has been updated')
                return redirect('staff:pages')
            else:
                messages.error(request, "Something went horribly wrong (this shouldn't be seen)")
                return redirect('staff:pages')
        else:
            staticinfoobj = StaticInfo.objects.get(pk=1)
            socialinfoobj = SocialInfo.objects.get(pk=1)
            static = StaticInfoForm(instance=staticinfoobj)
            social = SocialInfoForm(instance=socialinfoobj)
            return render(request, 'staff/pages/staticinfo.html', {'static': static, 'social': social})


def partnerlist(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        partner_list = Partner.objects.all().order_by('id')
        return render(request, 'staff/pages/partner_list.html', {'partner_list': partner_list})


def createpartner(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        if request.method == 'POST':
            form = PartnerForm(request.POST, request.FILES)
            if form.is_valid():
                # partner = form.instance
                # partner.author = User.objects.get(username=request.user.username)
                # partner.save()
                form.save()
                messages.success(request, 'Your partner has been created')
                return redirect('staff:partner_list')
            else:
                return render(request, 'staff/pages/partner_create.html', {'form': form})
        else:
            form = PartnerForm(None)
            return render(request, 'staff/pages/partner_create.html', {'form': form})


def partner_detail(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        if request.method == 'POST':
            partner = Partner.objects.get(pk=pk)
            form = PartnerForm(request.POST, request.FILES, instance=partner)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your information has been updated')
                return redirect('staff:partner_list')
            else:
                return render(request, 'staff/pages/partner_create.html', {'form': form})
        else:
            partner = Partner.objects.get(pk=pk)
            form = PartnerForm(instance=partner)
            return render(request, 'staff/pages/partner_create.html', {'form': form})

# end static info section
