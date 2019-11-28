from django.apps import AppConfig

class chatAppConfig(AppConfig):
    name = 'chat'

    def ready(self):
        import ChatApp.ChatApp.chat.signals