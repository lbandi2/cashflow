from django.urls import path

from . import views

app_name = 'cashflow'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('last_operations/', views.LastOpsView.as_view(), name='last_ops'),
    path('last_operations_by_day/', views.LastOpsByDayView.as_view(), name='last_ops_by_day'),
    path('last_operations_by_card/', views.LastOpsByCardView.as_view(), name='last_ops_by_card'),
]
