from django.contrib import admin

from support.models import Ticket, TicketComment


class TicketCommentInline(admin.TabularInline):
    model = TicketComment
    extra = 1
    raw_id_fields = ['author']
    readonly_fields = ['date']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'author':
            kwargs['initial'] = request.user.id
        return super(TicketCommentInline, self).formfield_for_foreignkey(db_field, request, **kwargs)


class TicketAdmin(admin.ModelAdmin):
    list_display = ['date', 'status', 'creator', 'assignee', 'latest_activity', 'is_answered']
    list_filter = ['status', 'date']
    search_fields = ['text', 'creator__username', 'creator__email']
    raw_id_fields = ['creator', 'assignee']
    inlines = [TicketCommentInline, ]

    def latest_activity(self, obj):
        # list_display = obj.get_latest_comment()
        # return "%s %s - %s" % (_date(latest.date), _time(latest.date), latest.author)
        pass

    latest_activity.short_description = 'Latest Activity'


admin.site.register(Ticket, TicketAdmin)
