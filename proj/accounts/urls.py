from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('operation/<int:pk>/edit/', views.OpUpdate.as_view(), name='update_op'),
    path('operations/filter/by_table/', views.LastOpsView.as_view(), name='last_ops'),
    path('operations/filter/by_day/', views.LastOpsByDayView.as_view(), name='last_ops_by_day'),
    path('operations/filter/by_account/', views.LastOpsByAccountView.as_view(), name='last_ops_by_account'),
]
