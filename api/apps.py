from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = 'api'
    verbose_name = 'REST API'

    def ready(self):
        from django.contrib.auth.models import User
        from django.db.models.signals import post_save
        from rest_framework.authtoken.models import Token

        def create_auth_token(sender, instance=None, created=False, **kwargs):
            if created:
                Token.objects.create(user=instance)

        post_save.connect(create_auth_token, sender=User)