from django.urls import path
from django.urls.conf import path, re_path
from .apis import *


urlpatterns = [
    path('rev_exps/add', AddRevenueExpenditureApi.as_view(), name='rev_exp_add'),
    re_path(r'^rev_exps/list/(?:start=(?P<start>(?:19|20)\d{2}([1-9]|1[012])))&(?:end=(?P<end>(?:19|20)\d{2}([1-9]|1[012])))$', RevenueExpenditureListApi.as_view(), name='rev_exp_list'),
    path('rev_exps/update/<int:revenue_expenditure_id>', UpdateRevenueExpenditureApi.as_view(), name='rev_exp_update'),
    path('rev_exps/delete/<int:revenue_expenditure_id>', DeleteRevenueExpenditureApi.as_view(), name='rev_exp_delete'),
]