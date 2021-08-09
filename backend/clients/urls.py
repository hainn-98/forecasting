from django.urls import path
from .apis import *

urlpatterns = [
    path('auth/sign_up', SignUpApi.as_view(), name='sign_up'),
    path('clients/<int:client_id>', ClientDetailApi.as_view(), name='client_detail'),
    path('clients/update', ClientUpdateApi.as_view(), name='client_update'),
    path('clients/deactivate', ClientDeactivateApi.as_view(), name='client_deactivate'),
    path('clients/users', ClientListUsersApi.as_view(), name='client_list_users')
]