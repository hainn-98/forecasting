from django.urls import path, re_path
from .apis import *


urlpatterns = [
    path('cpis/add', AddCpiApi.as_view(), name='cpi_add'),
    re_path(r'^cpis/list/(?:start=(?P<start>(?:19|20)\d{2}([1-9]|1[012])))&(?:end=(?P<end>(?:19|20)\d{2}([1-9]|1[012])))$', CpiListApi.as_view(), name='cpi_list'),
    path('cpis/update/<int:cpi_id>', UpdateCpiApi.as_view(), name='cpi_update'),
    path('cpis/delete/<int:cpi_id>', DeleteCpiApi.as_view(), name='cpi_delete'),
]