from django.urls import path
from . import views

app_name = 'transactions'
urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('income/', views.income_categories, name='income_categories'),
    path('expense/', views.expense_categories, name='expense_categories'),
    path('add-income/<int:category_id>/', views.add_income, name='add_income'),
    path('add-expense/<int:category_id>/', views.add_expense, name='add_expense'),
]