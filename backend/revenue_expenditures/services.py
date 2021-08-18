from .models import RevenueExpenditure
from utils.custom_exceptions import *


def get_revenue_expenditure_by(raise_exception=True, **kwargs):
    revenue_expenditure = RevenueExpenditure.objects.filter(**kwargs).all()
    if not revenue_expenditure and raise_exception: 
        raise ObjectNotFound
    return revenue_expenditure

def add_revenue_expenditure(data, **kwargs):
    for key, value in kwargs.items():
        data[key] = value
    revenue_expenditure = get_revenue_expenditure_by(raise_exception=False, year=data['year'], month = data['month']).first()
    if revenue_expenditure:
        raise DuplicateEntry(entry=str(revenue_expenditure.year) + str(revenue_expenditure.month), key='year and month')
    revenue_expenditure = RevenueExpenditure.objects.create(**dict(data))
    return revenue_expenditure

def update_revenue_expenditure(revenue_expenditure, data):
    if not any(data.values()):
        raise ValidationError
    revenue_expenditure.revenue = data.get('revenue') or revenue_expenditure.revenue
    revenue_expenditure.expenditure = data.get('expenditure') or revenue_expenditure.expenditure
    revenue_expenditure.save(update_fields=['revenue', 'expenditure'])
    return revenue_expenditure

def delete_revenue_expenditure(revenue_expenditure):
    revenue_expenditure.delete()
    return revenue_expenditure
