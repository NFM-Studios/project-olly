from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View, DetailView

from staff.forms import *
from support.models import Ticket, TicketComment


def tickets(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        if request.method == 'GET':
            form = TicketSearchForm
            ticket_list = Ticket.objects.filter(status__lte=2).order_by('-id')
            return render(request, 'staff/support/ticket_list.html', {'form': form, 'ticket_list': ticket_list})

        elif request.method == 'POST':
            form = TicketSearchForm(request.POST)
            ticket_list = Ticket.objects.filter(status__lte=2).order_by('-id')
            if request.POST.get('showClosed'):
                ticket_list = Ticket.objects.all().order_by('-id')
            if request.POST.get('searchQuery'):
                query = request.POST.get('searchQuery')
                try:
                    ticket_list = Ticket.objects.filter(pk=query).order_by('-id')
                except ValueError:
                    ticket_list = Ticket.objects.filter(Q(text__contains=query) |
                                                        Q(creator__username__contains=query)).order_by('-id')
            return render(request, 'staff/support/ticket_list.html', {'form': form, 'ticket_list': ticket_list})


def ticket_category_list(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        cats = TicketCategory.objects.all()
        return render(request, 'staff/support/ticket_category_list.html', {'cats': cats})


class TicketCategoryCreate(View):
    form_class = TicketCategoryCreateForm
    template_name = 'staff/support/ticket_category_create.html'

    def get(self, request):
        user = UserProfile.objects.get(user__username=request.user.username)
        allowed = ['superadmin', 'admin']
        if user.user_type not in allowed:
            return render(request, 'staff/permissiondenied.html')
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        user = UserProfile.objects.get(user__username=request.user.username)
        allowed = ['superadmin', 'admin']
        if user.user_type not in allowed:
            return render(request, 'staff/permissiondenied.html')
        form = self.form_class(request.POST)

        if form.is_valid():
            cat = form.instance
            cat.name = form.cleaned_data['name']
            cat.priority = form.cleaned_data['priority']
            cat.save()
            messages.success(self.request, 'Ticket Category successfully added')
            return redirect('staff:ticket_categories')
        else:
            messages.error(self.request, 'An error occurred')
            return render(request, self.template_name, {'form': form})


def ticket_cat_delete(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        cat = TicketCategory.objects.get(pk=pk)
        # cat = get_object_or_404(TicketCategory, pk=pk)
        cat.delete()
        # cat.save()
        messages.success(request, 'Successfully deleted ticket category')
        return redirect('staff:ticket_categories')


class TicketDetail(DetailView):
    model = Ticket
    template_name = 'staff/support/ticket_detail.html'
    form1 = TicketCommentCreateForm()
    form1_class = TicketCommentCreateForm
    form2 = TicketStatusChangeForm()
    form2_class = TicketStatusChangeForm

    def get(self, request, **kwargs):
        user = UserProfile.objects.get(user__username=request.user.username)
        allowed = ['superadmin', 'admin']
        if user.user_type not in allowed:
            return render(request, 'staff/permissiondenied.html')
        form1 = self.form1_class(None)
        form2 = self.form2_class(None)
        pk = self.kwargs['pk']
        ticket = Ticket.objects.get(id=pk)
        comments = TicketComment.objects.filter(ticket=pk).order_by('id')
        return render(request, self.template_name, {'form': form1, 'form2': form2, 'x': pk,
                                                    "ticket": ticket, "comments": comments})

    def get_context_date(self, **kwargs):
        context = super(TicketDetail, self).get_context_data(**kwargs)
        context['form'] = self.form
        return context

    def post(self, request, *args, **kwargs):
        user = UserProfile.objects.get(user__username=request.user.username)
        allowed = ['superadmin', 'admin']
        if user.user_type not in allowed:
            return render(request, 'staff/permissiondenied.html')
        if 'post_comment' in request.POST:
            self.form1 = TicketCommentCreateForm(request.POST)
            if self.form1.is_valid():
                self.form1_valid(self.form1)
                return redirect(reverse('staff:ticket_detail', args=[self.kwargs['pk']]))
            return super(TicketDetail, self).get(request, *args, **kwargs)

        if 'change_status' in request.POST:
            self.form2 = TicketStatusChangeForm(request.POST, instance=Ticket.objects.get(pk=self.kwargs['pk']))
            if self.form2.is_valid():
                self.status_form_valid(self.form2)
                return redirect(reverse('staff:ticket_detail', args=[self.kwargs['pk']]))
            return super(TicketDetail, self).get(request, *args, **kwargs)

    def form1_valid(self, form1):
        comment = form1.instance
        comment.author = self.request.user
        comment.ticket = Ticket.objects.get(id=self.kwargs['pk'])
        comment.save()
        messages.success(self.request, 'Your response has been successfully added to the ticket.')

    def status_form_valid(self, form2):
        ticket = form2.instance
        ticket.save()
        messages.success(self.request, 'Ticket successfully updated.')

    def get_queryset(self):
        return Ticket.objects.filter(creator=self.request.user)


class TicketCommentCreate(View):
    form_class = TicketCommentCreateForm
    template_name = 'staff/ticket_comment_create.html'

    def get(self, request, pk):
        user = UserProfile.objects.get(user__username=request.user.username)
        allowed = ['superadmin', 'admin']
        if user.user_type not in allowed:
            return render(request, 'staff/permissiondenied.html')
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        user = UserProfile.objects.get(user__username=request.user.username)
        allowed = ['superadmin', 'admin']
        if user.user_type not in allowed:
            return render(request, 'staff/permissiondenied.html')
        form = self.form_class(request.POST)

        if form.is_valid():
            comment = form.instance
            comment.ticket = Ticket.objects.get(pk=pk)
            comment.author = self.request.user
            comment.comment = form.cleaned_data['comment']
            comment.save()
            messages.success(self.request, 'Comment successfully added')
            return redirect('staff:tickets')
        else:
            messages.error(self.request, 'An error occurred')
            return render(request, self.template_name, {'form': form})
