from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = "This command will create groups and assign permissions to said groups. WARNING: THIS WILL OVERWRITE THE 'Admin' and 'SuperAdmin' groups"

    def handle(self, *args, **options):
        Group.objects.get_or_create(name='Staff')
        Group.objects.get_or_create(name='Admin')

        # Leagues
        create_league = Permission.objects.get(codename='add_league')
        change_league = Permission.objects.get(codename='change_league')
        delete_league = Permission.objects.get(codename='delete_league')
        view_league = Permission.objects.get(codename='view_league')

        create_league_settings = Permission.objects.get(codename='add_leaguesettings')
        change_league_settings = Permission.objects.get(codename='change_leaguesettings')
        delete_league_settings = Permission.objects.get(codename='delete_leaguesettings')
        view_league_settings = Permission.objects.get(codename='view_leaguesettings')

        # Matches
        create_game = Permission.objects.get(codename='add_gamechoice')
        change_game = Permission.objects.get(codename='change_gamechoice')
        delete_game = Permission.objects.get(codename='delete_gamechoice')
        view_game = Permission.objects.get(codename='view_gamechoice')

        create_map = Permission.objects.get(codename='add_mapchoice')
        change_map = Permission.objects.get(codename='change_mapchoice')
        delete_map = Permission.objects.get(codename='delete_mapchoice')
        view_map = Permission.objects.get(codename='view_mapchoice')

        create_map_pool = Permission.objects.get(codename='add_mappoolchoice')
        change_map_pool = Permission.objects.get(codename='change_mappoolchoice')
        delete_map_pool = Permission.objects.get(codename='delete_mappoolchoice')
        view_map_pool = Permission.objects.get(codename='view_mappoolchoice')

        create_platform = Permission.objects.get(codename='add_platformchoice')
        change_platform = Permission.objects.get(codename='change_platformchoice')
        delete_platform = Permission.objects.get(codename='delete_platformchoice')
        view_platform = Permission.objects.get(codename='view_platformchoice')

        create_sport = Permission.objects.get(codename='add_sportchoice')
        change_sport = Permission.objects.get(codename='change_sportchoice')
        delete_sport = Permission.objects.get(codename='delete_sportchoice')
        view_sport = Permission.objects.get(codename='view_sportchoice')

        # News
        create_post = Permission.objects.get(codename='add_post')
        change_post = Permission.objects.get(codename='change_post')
        delete_post = Permission.objects.get(codename='delete_post')
        view_post = Permission.objects.get(codename='view_post')

        create_comment = Permission.objects.get(codename='add_comment')
        change_comment = Permission.objects.get(codename='change_comment')
        delete_comment = Permission.objects.get(codename='delete_comment')
        view_comment = Permission.objects.get(codename='view_comment')

        # Pages
        create_slide = Permission.objects.get(codename='add_frontpageslide')
        change_slide = Permission.objects.get(codename='change_frontpageslide')
        delete_slide = Permission.objects.get(codename='delete_frontpageslide')
        view_slide = Permission.objects.get(codename='view_frontpageslide')

        create_partner = Permission.objects.get(codename='add_partner')
        change_partner = Permission.objects.get(codename='change_partner')
        delete_partner = Permission.objects.get(codename='delete_partner')
        view_partner = Permission.objects.get(codename='view_partner')

        change_social_info = Permission.objects.get(codename='change_socialinfo')
        view_social_info = Permission.objects.get(codename='view_socialinfo')

        change_static_info = Permission.objects.get(codename='change_staticinfo')
        view_static_info = Permission.objects.get(codename='view_staticinfo')

        # Profiles
        change_profile = Permission.objects.get(codename='change_userprofile')
        view_profile = Permission.objects.get(codename='view_userprofile')

        ban_user = Permission.objects.get(codename='add_banneduser')
        unban_user = Permission.objects.get(codename='delete_banneduser')

        # Single elimination tournaments
        create_single_tournament = Permission.objects.get(codename='add_singleeliminationtournament')
        change_single_tournament = Permission.objects.get(codename='change_singleeliminationtournament')
        delete_single_tournament = Permission.objects.get(codename='delete_singleeliminationtournament')
        view_single_tournament = Permission.objects.get(codename='view_singleeliminationtournament')

        create_single_tournament_ruleset = Permission.objects.get(codename='add_singletournamentruleset')
        change_single_tournament_ruleset = Permission.objects.get(codename='change_singletournamentruleset')
        delete_single_tournament_ruleset = Permission.objects.get(codename='delete_singletournamentruleset')
        view_single_tournament_ruleset = Permission.objects.get(codename='view_singletournamentruleset')

        # Store
        create_product = Permission.objects.get(codename='add_product')
        change_product = Permission.objects.get(codename='change_product')
        delete_product = Permission.objects.get(codename='delete_product')
        view_product = Permission.objects.get(codename='view_product')

        # Support
        create_qa_category = Permission.objects.get(codename='add_questionanswercategory')
        change_qa_category = Permission.objects.get(codename='change_questionanswercategory')
        delete_qa_category = Permission.objects.get(codename='delete_questionanswercategory')
        view_qa_category = Permission.objects.get(codename='view_questionanswercategory')

        create_qa_topic = Permission.objects.get(codename='add_questionanswer')
        change_qa_topic = Permission.objects.get(codename='change_questionanswer')
        delete_qa_topic = Permission.objects.get(codename='delete_questionanswer')
        view_qa_topic = Permission.objects.get(codename='view_questionanswer')

        create_ticket_category = Permission.objects.get(codename='add_ticketcategory')
        change_ticket_category = Permission.objects.get(codename='change_ticketcategory')
        delete_ticket_category = Permission.objects.get(codename='delete_ticketcategory')
        view_ticket_category = Permission.objects.get(codename='view_ticketcategory')

        create_ticket = Permission.objects.get(codename='add_ticket')
        change_ticket = Permission.objects.get(codename='change_ticket')
        delete_ticket = Permission.objects.get(codename='delete_ticket')
        view_ticket = Permission.objects.get(codename='view_ticket')

        create_ticket_comment = Permission.objects.get(codename='add_ticketcomment')
        change_ticket_comment = Permission.objects.get(codename='change_ticketcomment')
        delete_ticket_comment = Permission.objects.get(codename='delete_ticketcomment')
        view_ticket_comment = Permission.objects.get(codename='view_ticketcomment')

        # Teams
        create_team = Permission.objects.get(codename='add_team')
        change_team = Permission.objects.get(codename='change_team')
        delete_team = Permission.objects.get(codename='delete_team')
        view_team = Permission.objects.get(codename='view_team')

        Group.objects.get(name='Staff').permissions.set([

        ])
        Group.objects.get(name='Admin').permissions.set([

        ])
