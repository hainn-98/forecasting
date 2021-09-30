from django.urls import path, re_path
from .apis import *


urlpatterns = [
    path('iips/add', AddIipApi.as_view(), name='iip_add'),
    re_path(r'^iips/list/(?:start=(?P<start>(?:19|20)\d{2}(0[1-9]|1[012])))&(?:end=(?P<end>(?:19|20)\d{2}(0[1-9]|1[012])))$', IipListApi.as_view(), name='iip_list'),
    path('iips/update/<int:cpi_id>', UpdateIipApi.as_view(), name='iip_update'),
    path('iips/delete/<int:cpi_id>', DeleteIipApi.as_view(), name='iip_delete'),
]