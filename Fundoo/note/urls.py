from django.conf.urls import url
from .views import save_Contacts, get_Contacts

urlpatterns = [
    url('save-contacts', save_Contacts, name='save_contacts'),
    url('get-contacts', get_Contacts, name='get_contacts'),
]