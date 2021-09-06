from django.urls import path
from django.urls.conf import re_path, path
from .apis import *


urlpatterns = [
    path('import_exports/add', AddImportExportApi.as_view(), name='import_export_add'),
    re_path(r'^import_exports/list/(?:start=(?P<start>(?:19|20)\d{2}([1-9]|1[012])))&(?:end=(?P<end>(?:19|20)\d{2}([1-9]|1[012])))$', ImportExportListApi.as_view(), name='import_export_list'),
    path('import_exports/update/<int:import_export_id>', UpdateImportExportApi.as_view(), name='import_export_update'),
    path('import_exports/delete/<int:import_export_id>', DeleteImportExportApi.as_view(), name='import_export_delete'),
]