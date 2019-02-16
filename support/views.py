from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import DetailView, View

from profiles.models import UserProfile
from support.forms import TicketCreateForm, TicketCommentCreateForm, TicketStatusChangeForm, ListFilterForm
from support.models import Ticket, TicketComment


class MyTicketListView(View):
    model = Ticket
    form = ListFilterForm

    def get(self, request):
        form = self.form
        ticket_list = Ticket.objects.filter(creator=request.user, status__lte=2)
        return render(request, 'tickets/' + request.tenant + '/ticket_mylist.html',
                      {'form': form, 'ticket_list': ticket_list})

    def post(self, request):
        form = self.form(request.POST)
        ticket_list = Ticket.objects.filter(creator=request.user, status__lte=2)
        if request.POST.get('showClosed'):
            ticket_list = Ticket.objects.filter(creator=request.user)
        if request.POST.get('searchQuery'):
            query = request.POST.get('searchQuery')
            try:
                ticket_list = Ticket.objects.filter(pk=query)
            except ValueError:
                ticket_list = Ticket.objects.filter(text__contains=query)
        return render(request, 'tickets/' + request.tenant + '/ticket_mylist.html',
                      {'form': form, 'ticket_list': ticket_list})


class MyTicketDetailView(DetailView):
    model = Ticket
    form1 = TicketCommentCreateForm()
    form1_class = TicketCommentCreateForm
    form2 = TicketStatusChangeForm()
    form2_class = TicketStatusChangeForm

    def get(self, request, **kwargs):
        form1 = self.form1_class(None)
        form2 = self.form2_class(None)

        pk = self.kwargs['pk']
        ticket = get_object_or_404(Ticket, pk=pk)
        creator = UserProfile.objects.get(user=ticket.creator)
        comments = TicketComment.objects.filter(ticket=pk)
        return render(request, 'tickets/' + request.tenant + '/ticket_mydetail.html', {'form': form1, 'x': pk,
                                                                                       "ticket": ticket,
                                                                                       "comments": comments,
                                                                                       'creator': creator})

    def get_context_date(self, **kwargs):
        context = super(MyTicketDetailView, self).get_context_data(**kwargs)
        context['form'] = self.form1
        return context

    def post(self, request, *args, **kwargs):
        if 'post_comment' in request.POST:
            self.form1 = TicketCommentCreateForm(request.POST)
            if self.form1.is_valid():
                self.form1_valid(self.form1)
                return redirect(reverse('support:detail', args=[self.kwargs['pk']]))
            return super(MyTicketDetailView, self).get(request, *args, **kwargs)

        if 'change_status' in request.POST:
            self.form2 = TicketStatusChangeForm(request.POST, instance=Ticket.objects.get(pk=self.kwargs['pk']))
            self.status_form_valid(self.form2)
            return redirect(reverse('support:detail', args=[self.kwargs['pk']]))

    def form1_valid(self, form):
        comment = form.instance
        comment.author = self.request.user
        comment.ticket = Ticket.objects.get(id=self.kwargs['pk'])
        comment.save()
        messages.success(self.request, 'Your response has been successfully added to the ticket.')

    def status_form_valid(self, form2):
        ticket = form2.instance
        ticket.status = 3
        ticket.save()
        messages.success(self.request, 'Ticket successfully closed.')

    def get_queryset(self):
        return Ticket.objects.filter(creator=self.request.user)


class TicketCreateView(View):
    form_class = TicketCreateForm

    def get(self, request):
        form = self.form_class()
        return render(request, 'tickets/' + request.tenant + '/ticket_create.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            ticket = form.instance
            ticket.creator = self.request.user
            ticket.text = form.cleaned_data['text']
            ticket.category = form.cleaned_data['category']
            ticket.save()
            messages.success(self.request, 'Your ticket has been successfully created')
            return redirect('support:detail', pk=ticket.id)
