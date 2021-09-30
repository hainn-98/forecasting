from django.urls import path
from django.urls.conf import re_path, path
from .apis import *


urlpatterns = [
    path('exports/add', AddExportApi.as_view(), name='export_add'),
    re_path(r'^exports/list/(?:start=(?P<start>(?:19|20)\d{2}(0[1-9]|1[012])))&(?:end=(?P<end>(?:19|20)\d{2}(0[1-9]|1[012])))$', ExportListApi.as_view(), name='export_list'),
    path('exports/update/<int:export_id>', UpdateExportApi.as_view(), name='export_update'),
    path('exports/delete/<int:export_id>', DeleteExportApi.as_view(), name='export_delete'),
]