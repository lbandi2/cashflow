from django.urls import path

from . import views

app_name = 'credit_cards'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('operation/<int:pk>/edit/', views.OpUpdate.as_view(), name='update_op'),
    path('operations/filter/by_table/<int:page>', views.LastOpsView, name="last_ops"),
    # path('operations/filter/by_table/', views.LastOpsView.as_view(), name='last_ops'),
    path('operations/filter/by_day/', views.LastOpsByDayView.as_view(), name='last_ops_by_day'),
    path('operations/filter/by_card/', views.LastOpsByCardView.as_view(), name='last_ops_by_card'),
    path('operations/filter/<card>/unbilled/', views.UnbilledSpending.as_view(), name='unbilled_spending'),
    path('operations.json', views.LastOpsView_api, name="terms-api"),  # Operations API
    path('charts/', views.ChartsView.as_view(), name='charts')
]
