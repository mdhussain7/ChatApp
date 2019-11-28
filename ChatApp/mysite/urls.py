from django.contrib import admin
# from django.urls import path, include
from django.conf.urls import url

urlpatterns = [
    url('admin/', admin.site.urls),
    #url('', include('chat.urls', namespace='mysite')),
    # path('admin/', admin.site.urls),
   # path('chat/', include('chat.urls', namespace='chat'))
]
