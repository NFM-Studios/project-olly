from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect

from staff.forms import *
from support.models import Ticket
from pages.models import FrontPageSlide
from wagers.models import *


@staff_member_required
def staffindex(request):
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

@permission_required('pages.change_staticinfo', raise_exception=True)
def pages(request):
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


@permission_required('pages.view_partner', raise_exception=True)
def partnerlist(request):
    partner_list = Partner.objects.all().order_by('id')
    return render(request, 'staff/pages/partner_list.html', {'partner_list': partner_list})


@permission_required('pages.add_partner', raise_exception=True)
def createpartner(request):
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


@permission_required('pages.change_partner', raise_exception=True)
def partner_detail(request, pk):
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


@permission_required('pages.view_frontpageslide', raise_exception=True)
def slide_list(request):
    slides = FrontPageSlide.objects.all()
    return render(request, 'staff/pages/slide_list.html', {'slides': slides})


@permission_required('pages.add_frontpageslide', raise_exception=True)
def slide_create(request):
    if request.method == 'POST':
        form = CreateSlide(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your slide has been created')
            return redirect('staff:slide_list')
        else:
            return render(request, 'staff/pages/slide_create.html', {'form': form})
    else:
        form = CreateSlide(None)
        return render(request, 'staff/pages/slide_create.html', {'form': form})


@permission_required('pages.change_frontpageslide', raise_exception=True)
def slide_detail(request, pk):
    if request.method == 'POST':
        slide_obj = FrontPageSlide.objects.get(pk=pk)
        form = CreateSlide(request.POST, request.FILES, instance=slide_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your changes have been saved')
            return redirect('staff:slide_list')
        else:
            return render(request, 'staff/pages/slide_detail.html', {'form': form, 'pk': pk})
    else:
        slide_obj =  FrontPageSlide.objects.get(pk=pk)
        form = CreateSlide(instance=slide_obj)
        return render(request, 'staff/pages/slide_detail.html', {'form': form, 'pk': pk})


@permission_required('pages.delete_frontpageslide', raise_exception=True)
def slide_delete(request, pk):
    slide = FrontPageSlide.objects.get(pk=pk)
    slide.delete()
    messages.success(request, 'slide has been deleted')
    return redirect('staff:slide_list')

# end static info section
