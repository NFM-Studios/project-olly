from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'staff'

urlpatterns = [
    url(r'^$', login_required(views.staffindex), name='index'),

    url(r'^users/$', login_required(views.users), name='users'),

    url(r'^tickets/$', login_required(views.tickets), name='tickets'),
    url(r'^ticketdetail/(?P<pk>\d+)/$', login_required(views.TicketDetail.as_view()), name='ticket_detail'),
    url(r'^ticketcomment/(?P<pk>\d+)/$', login_required(views.TicketCommentCreate.as_view()), name='ticket_comment_create'),
    url(r'^pages/$', login_required(views.pages), name='pages'),

    url(r'^users/getrank/$', login_required(views.getrank)),
    url(r'^users/ban/(?P<urlusername>[A-Za-z0-9_@+.-]+)/$', login_required(views.banuser)),
    url(r'^users/unban/(?P<urlusername>[A-Za-z0-9_@+.-]+)/$', login_required(views.unbanuser)),
    url(r'^users/banip/(?P<urlusername>[A-Za-z0-9_@+.-]+)/$', login_required(views.banip)),
    url(r'^users/unbanip/(?P<urlusername>[A-Za-z0-9_@+.-]+)/$', login_required(views.unbanip)),
    url(r'^users/search/$', login_required(views.searchusers), name='searchusers'),
    url(r'^users/edit/(?P<urlusername>[A-Za-z0-9_@+.-]+)/$', login_required(views.edituser)),
    url(r'^users/(?P<urlusername>[A-Za-z0-9_@+.-]+)/$', login_required(views.userdetail)),
    url(r'^users/verify/(?P<urlusername>[A-Za-z0-9_@+.-]+)/$', login_required(views.verify)),
    url(r'^users/modify/(?P<urlusername>\[A-Za-z0-9_@+.-]+)/$', login_required(views.modifyuser)),


    url(r'^tournaments/$', login_required(views.tournaments), name='tournamentlist'),
    url(r'^tournaments/rulesets/$', login_required(views.ruleset_list), name='tournamentrulesetlist'),
    url(r'^tournaments/rulesets/(?P<pk>\d+)/$', login_required(views.ruleset_detail), name='tournamentrulesetdetail'),
    url(r'^tournaments/rulesets/create$', login_required(views.ruleset_create), name='tournamentrulesetcreate'),
    url(r'^tournaments/(?P<pk>\d+)/$', login_required(views.tournament_detail), name='tournament_detail'),
    url(r'^tournaments/edit/(?P<pk>\d+)/$', login_required(views.edit_tournament), name='edit_tournament'),
    url(r'^tournaments/create/$', login_required(views.create_tournament), name='create_tournament'),
    url(r'^tournaments/delete/(?P<pk>\d+)/$', login_required(views.delete_tournament), name='delete_tournament'),
    url(r'^tournaments/generatebracket/(?P<pk>\d+)$', login_required(views.generate_bracket), name='generate_bracket'),
    url(r'^tournaments/advance/(?P<pk>\d+)$', login_required(views.advance), name='advance'),
    url(r'^tournaments/winner/(?P<pk>\d+)$', login_required(views.DeclareTournamentWinner.as_view()), name='winner'),

    url(r'^matches/$', login_required(views.matches_index), name='matches_index'),
    url(r'^match/(?P<pk>\d+)$', login_required(views.match_detail), name='match_detail'),
    url(r'^match/(?P<pk>\d+)/declare$', login_required(views.MatchDeclareWinner.as_view()), name='match_declare_winner'),
    url(r'^match/(?P<pk>\d+)/delete', login_required(views.match_delete_winner), name='match_delete_winner'),
    url(r'^match/(?P<pk>\d+)/edit', login_required(views.match_edit), name='match_edit'),
    url(r'^round/(?P<pk>\d+)/edit', login_required(views.edit_round), name='edit_round'),
    url(r'^round/(?P<pk>\d+)/', login_required(views.round_detail), name='round_detail'),
    url(r'^dispute/(?P<pk>\d+)/', login_required(views.dispute_detail), name='dispute_detail'),

    url(r'^news/$', login_required(views.news_index), name='news_index'),
    url(r'^news/list/$', login_required(views.news_list), name='news_list'),
    url(r'^news/create/$', login_required(views.create_article), name='create_article'),
    url(r'^news/(?P<pk>\d+)/$', login_required(views.detail_article), name='detail_article'),
    url(r'^news/(?P<pk>\d+)/edit', login_required(views.edit_post), name='edit_article'),
    url(r'^news/remove', login_required(views.remove_article), name='remove_article'),

    url(r'^store/$', login_required(views.store_index), name='store'),
    url(r'^store/transactions/list', login_required(views.TransactionView.as_view()), name='transaction_list'),
    url(r'^store/transfers/list', login_required(views.TransferView.as_view()), name='transfer_list'),
    url(r'^store/products/$', login_required(views.products), name='product_list'),
    url(r'^store/products/create/$', login_required(views.create_product), name='create_product'),
    url(r'^store/products/delete/$', login_required(views.delete_product), name='delete_product'),
    url(r'^store/products/(?P<pk>\d+)/$', login_required(views.product_detail), name='product_detail'),
    url(r'^store/products/(?P<pk>\d+)/edit/$', login_required(views.edit_product), name='product_edit'),

    url(r'^teams/$', login_required(views.teams_index), name='teamindex'),
    url(r'^teams/(?P<pk>\d+)/$', login_required(views.teams_detail), name='team_detail'),
    url(r'^teams/(?P<pk>\d+)/remove/$', login_required(views.remove_user), name='remove_user'),
    url(r'^teams/getrank/$', login_required(views.getteamrank), name='getteamrank'),

    url(r'^partners/$', login_required(views.partnerlist), name='partner_list'),
    url(r'^partners/create/$', login_required(views.createpartner), name='partner_create'),
    url(r'^partners/(?P<pk>\d+)/$', login_required(views.partner_detail), name='partner_detail')

]
