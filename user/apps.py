from django.apps import AppConfig


class UserConfig(AppConfig):
    name = 'user'

    def ready(self):
        from user.signals  import  save_kobocat_user,save_kobocat_token,delete_kobocat_token
