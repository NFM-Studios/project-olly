from django.db import models
from django.contrib.auth.models import User
# import the choices that are defined in the settings.py file
from support.settings import STATUS_CHOICES, CLOSED_STATUSES, CATEGORY_CHOICES

# Create your models here.


class Ticket(models.Model):
    creator = models.ForeignKey(User, verbose_name='Creator', related_name='ticket_create', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True, auto_now_add=False)
    # subject = models.CharField(max_length=255)
    category = models.SmallIntegerField(choices=CATEGORY_CHOICES, default=0)
    text = models.TextField(default='A detailed description of your issue')
    assignee = models.ForeignKey(User, related_name='assigned_tickets', verbose_name='assignee', blank=True,
                                 null=True, on_delete=models.CASCADE)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=0)

    class Meta:
        verbose_name = 'ticket'
        verbose_name_plural = 'tickets'
        ordering = ['date']

    def get_comments_count(self):
        return self.comments.count()

    def get_latest_comment(self):
        return self.comments.latest('date')

    def __unicode__(self):
        return "%s# %s" % (self.id, self.subject)

    def is_closed(self):
        return self.status in CLOSED_STATUSES

    def is_answered(self):
        try:
            latest = self.get_latest_comment()
        except TicketComment.DoesNotExist:
            return False
        return latest.author != self.creator
    is_answered.boolean = True
    is_answered.short_description = 'Is answered'


class TicketComment(models.Model):
    ticket = models.ForeignKey(Ticket, verbose_name='Ticket', related_name='comments', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, verbose_name='Date')
    author = models.ForeignKey(User, verbose_name='Author', on_delete=models.CASCADE)
    comment = models.TextField()
    # if the message is sent by staff set this to true. Then in the template display something unique
    staff = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Ticket comment'
        verbose_name_plural = 'Ticket comments'
        ordering = ['date']

    # Not sure if this is needed
    # def __unicode__(self):
        # return "Comment on " + unicode(self.ticket)
