# from django.conf.urls import url
import django.urls
from . import consumers

websocket_urlpatterns = [
    django.urls.re_path(r'^ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer),
]
