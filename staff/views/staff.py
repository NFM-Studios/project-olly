from staff.auth import staff_required
from django.http import HttpResponseNotAllowed

from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from staff.forms import *
from support.models import Ticket
from pages.models import FrontPageSlide, OllySetting, StaticPage
from wagers.models import *


@staff_required
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


@staff_required
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
    elif request.method == 'GET':
        staticinfoobj = StaticInfo.objects.get(pk=1)
        socialinfoobj = SocialInfo.objects.get(pk=1)
        static = StaticInfoForm(instance=staticinfoobj)
        social = SocialInfoForm(instance=socialinfoobj)
        return render(request, 'staff/pages/staticinfo.html', {'static': static, 'social': social})


@staff_required
def partnerlist(request):
    partner_list = Partner.objects.all().order_by('id')
    return render(request, 'staff/pages/partner_list.html', {'partner_list': partner_list})


@staff_required
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


@staff_required
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
    elif request.method == 'GET':
        partner = Partner.objects.get(pk=pk)
        form = PartnerForm(instance=partner)
        return render(request, 'staff/pages/partner_create.html', {'form': form})


@staff_required
def slide_list(request):
    slides = FrontPageSlide.objects.all()
    return render(request, 'staff/pages/slide_list.html', {'slides': slides})


@staff_required
def slide_create(request):
    if request.method == 'POST':
        form = CreateSlide(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your slide has been created')
            return redirect('staff:slide_list')
        else:
            return render(request, 'staff/pages/slide_create.html', {'form': form})
    elif request.method == 'GET':
        form = CreateSlide(None)
        return render(request, 'staff/pages/slide_create.html', {'form': form})


@staff_required
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
    elif request.method == 'GET':
        slide_obj = FrontPageSlide.objects.get(pk=pk)
        form = CreateSlide(instance=slide_obj)
        return render(request, 'staff/pages/slide_detail.html', {'form': form, 'pk': pk})


@staff_required
def slide_delete(request, pk):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    slide = FrontPageSlide.objects.get(pk=pk)
    slide.delete()
    messages.success(request, 'slide has been deleted')
    return redirect('staff:slide_list')


@staff_required
def create_settings(request):
    if OllySetting.objects.exists():
        messages.warning(request, 'Settings already exist, redirecting to modify current settings.')
        return redirect('staff:edit_settings')
    else:
        if request.method == 'POST':
            form = CreateOllySetting(request.POST)
            if form.is_valid():
                temp = form.instance
                temp.save()
                messages.success(request, "Settings created")
                return redirect('staff:edit_settings')
        elif request.method == 'GET':
            form = CreateOllySetting()
            return render(request, 'staff/pages/create_olly_settings.html', {'form': form})


@staff_required
def edit_settings(request):
    settings = OllySetting.objects.get(pk=1)
    if request.method == 'POST':
        form = CreateOllySetting(request.POST)
        if form.is_valid():
            settings.freeze_team_invites = form.cleaned_data['freeze_team_invites']
            settings.disable_team_creation = form.cleaned_data['disable_team_creation']
            settings.whats_new = form.cleaned_data['whats_new']
            settings.save()
            messages.success(request, 'Settings updated')
        else:
            messages.success(request, 'Failed to save changes')
        return redirect('staff:index')
    elif request.method == 'GET':
        form = CreateOllySetting(instance=settings)
        return render(request, 'staff/pages/edit_olly_settings.html', {'form': form})


@staff_required
def create_static_page(request):
    form = StaticPageForm()
    if request.method == 'POST':
        form = StaticPageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Static Page successfully created")
            return redirect('staff:list_static_page')
        else:
            messages.error(request, "ERROR: Static Page not created")
            return redirect('staff:list_static_page')
    elif request.method == 'GET':
        return render(request, 'staff/pages/create_static_page.html', {'form': form})


@staff_required
def edit_static_page(request, slug):
    page = StaticPage.objects.get(slug=slug)
    if request.method == 'POST':
        form = StaticPageForm(request.POST, instance=page)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully updated static page")
            return redirect('staff:list_static_page')
    elif request.method == 'GET':
        form = StaticPageForm(instance=page)
        return render(request, 'staff/pages/create_static_page.html', {'form': form})


@staff_required
def list_static_page(request):
    pages = StaticPage.objects.all()
    return render(request, 'staff/pages/list_static_page.html', {'pages': pages})


@staff_required
def delete_static_page(request, slug):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    page = StaticPage.objects.get(slug=slug)
    page.delete()
    return redirect('staff:list_static_page')


