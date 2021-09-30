from django.urls import path, re_path
from .apis import *

urlpatterns = [
    path('unemployments/add', AddUnemploymentApi.as_view(), name='unemployment_add'),
    re_path(r'^unemployments/list/(?:start=(?P<start>(?:19|20)\d{2}(0[1-9]|1[012])))&(?:end=(?P<end>(?:19|20)\d{2}(0[1-9]|1[012])))$', UnemploymentListApi.as_view(), name='unemployment_list'),
    path('unemployments/update/<int:unemployment_id>', UpdateUnemploymentApi.as_view(), name='unemployment_update'),
    path('unemployments/delete/<int:unemployment_id>', DeleteUnemploymentApi.as_view(), name='unemployment_delete'),
]