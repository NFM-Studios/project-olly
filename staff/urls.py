from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'staff'

urlpatterns = [
    path('', login_required(views.staffindex), name='index'),

    path('tickets', login_required(views.tickets), name='tickets'),
    path('ticketdetail/<int:pk>/', login_required(views.TicketDetail.as_view()), name='ticket_detail'),
    path('pages', login_required(views.pages), name='pages'),

    path('users', login_required(views.users), name='users'),
    path('users/getrank/', login_required(views.getrank)),
    path('users/ban/<urlusername>/', login_required(views.banuser)),
    path('users/unban/<urlusername>/', login_required(views.unbanuser)),
    path('users/banip/<urlusername>/', login_required(views.banip)),
    path('users/unbanip/<urlusername>/', login_required(views.unbanip)),
    path('users/search/', login_required(views.searchusers), name='searchusers'),
    path('users/edit/<urlusername>/', login_required(views.edituser)),
    path('users/<urlusername>/', login_required(views.userdetail), name='userdetail'),
    path('users/verify/<urlusername>/', login_required(views.verify)),
    path('users/modify/<urlusername>/', login_required(views.modifyuser)),


    path('tournaments/', login_required(views.tournaments), name='tournamentlist'),
    path('tournaments/rulesets/', login_required(views.ruleset_list), name='tournamentrulesetlist'),
    path('tournaments/rulesets/<int:pk>/', login_required(views.ruleset_detail), name='tournamentrulesetdetail'),
    path('tournaments/rulesets/create', login_required(views.ruleset_create), name='tournamentrulesetcreate'),
    path('tournaments/<int:pk>/', login_required(views.tournament_detail), name='tournament_detail'),
    path('tournaments/edit/<int:pk>/', login_required(views.edit_tournament), name='edit_tournament'),
    path('tournaments/create/', login_required(views.create_tournament), name='create_tournament'),
    path('tournaments/delete/<int:pk>/', login_required(views.delete_tournament), name='delete_tournament'),
    path('tournaments/generatebracket/<int:pk>', login_required(views.generate_bracket), name='generate_bracket'),
    path('tournaments/advance/<int:pk>', login_required(views.advance), name='advance'),
    path('tournaments/winner/<int:pk>', login_required(views.DeclareTournamentWinner.as_view()), name='winner'),
    path('tournaments/<int:pk>/addteams/', login_required(views.add_teams), name='add_team'),
    path('tournaments/<int:pk>/addteams/<int:teamid>/', login_required(views.add_teams), name='add_team'),

    path('matches/', login_required(views.matches_index), name='matches_index'),
    path('match/<int:pk>', login_required(views.match_detail), name='match_detail'),
    path('match/<int:pk>/declare', login_required(views.MatchDeclareWinner.as_view()), name='match_declare_winner'),
    path('match/<int:pk>/delete', login_required(views.match_delete_winner), name='match_delete_winner'),
    path('match/<int:pk>/edit', login_required(views.match_edit), name='match_edit'),
    path('round/<int:pk>/edit', login_required(views.edit_round), name='edit_round'),
    path('round/<int:pk>/', login_required(views.round_detail), name='round_detail'),
    path('dispute/<int:pk>/', login_required(views.dispute_detail), name='dispute_detail'),

    path('games/', login_required(views.gamelist), name='gamelist'),
    path('games/<int:pk>/', login_required(views.game_detail), name='game_detail'),
    path('games/<int:pk>/delete/', login_required(views.delete_game), name='delete_game'),
    path('games/create/', login_required(views.create_gamechoice), name='create_gamechoice'),

    path('platforms/', login_required(views.platformlist), name='platformlist'),
    path('platforms/<int:pk>/', login_required(views.platform_detail), name='platform_detail'),
    path('platforms/<int:pk>/delete/', login_required(views.delete_platform), name='delete_platform'),
    path('platforms/create/', login_required(views.create_platformchoice), name='create_platformchoice'),

    path('news/', login_required(views.news_list), name='news_index'),
    path('news/list/', login_required(views.news_list), name='news_list'),
    path('news/create/', login_required(views.create_article), name='create_article'),
    path('news/<int:pk>/', login_required(views.detail_article), name='detail_article'),
    path('news/<int:pk>/edit', login_required(views.edit_post), name='edit_article'),
    path('news/remove', login_required(views.remove_article), name='remove_article'),

    path('store/', login_required(views.store_index), name='store'),
    path('store/transactions/list', login_required(views.TransactionView.as_view()), name='transaction_list'),
    path('store/transfers/list', login_required(views.TransferView.as_view()), name='transfer_list'),
    path('store/products/', login_required(views.products), name='product_list'),
    path('store/products/create/', login_required(views.create_product), name='create_product'),
    path('store/products/delete/', login_required(views.delete_product), name='delete_product'),
    path('store/products/<int:pk>/', login_required(views.product_detail), name='product_detail'),
    path('store/products/<int:pk>/edit/', login_required(views.edit_product), name='product_edit'),

    path('teams/', login_required(views.teams_index), name='teamindex'),
    path('teams/<int:pk>/', login_required(views.teams_detail), name='team_detail'),
    path('teams/<int:pk>/remove/', login_required(views.remove_user), name='remove_user'),
    path('teams/getrank/', login_required(views.getteamrank), name='getteamrank'),

    path('partners/', login_required(views.partnerlist), name='partner_list'),
    path('partners/create/', login_required(views.createpartner), name='partner_create'),
    path('partners/<int:pk>/', login_required(views.partner_detail), name='partner_detail')

]
