from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include

urlpatterns = [
    url('api/', include('users.urls')),
    url('api/', include('clients.urls')),
    url('api/', include('cpis.urls')),
    url('api/', include('iips.urls')),
    url('api/', include('imports.urls')),
    url('api/', include('exports.urls')),
    url('api/', include('revenue_expenditures.urls')),
    url('api/', include('unemployments.urls'))
]