from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, View
from support.forms import TicketCreateForm, TicketCommentCreateForm, TicketStatusChangeForm, ListFilterForm
from support.models import Ticket, TicketComment
from django.shortcuts import render, redirect


class MyTicketListView(View):
    model = Ticket
    template_name = 'tickets/ticket_mylist.html'
    form = ListFilterForm

    def get(self, request):
        form = self.form
        ticket_list = Ticket.objects.filter(creator=request.user, status__lte=2)
        return render(request, self.template_name, {'form': form, 'ticket_list': ticket_list})

    def post(self, request):
        form = self.form(request.POST)
        ticket_list = Ticket.objects.filter(creator=request.user, status__lte=2)
        try:
            if form.data['showClosed']:
                ticket_list = Ticket.objects.filter(creator=request.user)
        except:
            pass
        return render(request, self.template_name, {'form': form, 'ticket_list': ticket_list})


class MyTicketDetailView(DetailView):
    model = Ticket
    template_name = 'tickets/ticket_mydetail.html'
    form1 = TicketCommentCreateForm()
    form1_class = TicketCommentCreateForm
    form2 = TicketStatusChangeForm()
    form2_class = TicketStatusChangeForm

    def get(self, request, **kwargs):
        form1 = self.form1_class(None)
        form2 = self.form2_class(None)
        pk = self.kwargs['pk']
        ticket = Ticket.objects.get(id=pk)
        comments = TicketComment.objects.filter(ticket=pk)
        return render(request, self.template_name, {'form': form1, 'x': pk,
                                                    "ticket": ticket, "comments": comments})

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


class TicketCreateView(CreateView):
    form_class = TicketCreateForm
    template_name = 'tickets/ticket_create.html'

    def form_valid(self, form):
        ticket = form.instance
        ticket.creator = self.request.user
        ticket.save()
        self.success_url = reverse('support:detail', args=[ticket.id])
        messages.success(self.request, 'Your ticket has been successfully created')
        return super(TicketCreateView, self).form_valid(form)
