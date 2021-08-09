from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include

urlpatterns = [
    url('api/', include('users.urls')),
    url('api/', include('clients.urls')),
]