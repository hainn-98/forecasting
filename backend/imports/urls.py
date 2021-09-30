from django.urls import path
from django.urls.conf import re_path, path
from .apis import *


urlpatterns = [
    path('imports/add', AddImportApi.as_view(), name='import_add'),
    re_path(r'^imports/list/(?:start=(?P<start>(?:19|20)\d{2}(0[1-9]|1[012])))&(?:end=(?P<end>(?:19|20)\d{2}(0[1-9]|1[012])))$', ImportListApi.as_view(), name='import_list'),
    path('imports/update/<int:import_id>', UpdateImportApi.as_view(), name='import_update'),
    path('imports/delete/<int:import_id>', DeleteImportApi.as_view(), name='import_delete'),
]