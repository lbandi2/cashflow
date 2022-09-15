from django.urls import path

from . import views

app_name = 'bills'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('credit_cards/', views.CardsView.as_view(), name='credit_cards'),
    path('credit_card/<bill>/view/', views.CardsViewDetail.as_view(), name='credit_card_view'),
    # path('credit_card/<bill>/operation/<op_bill>/view/', views.BillOpViewDetail.as_view(), name='bill_op_view'),
    path('credit_card/<bill_id>/operation/<pk>/view/', views.BillOpUpdate.as_view(), name='bill_op_view'),
    path('credit_card/<pk>/toggle_pay/', views.bill_toggle_pay, name='bill_toggle_pay'),
    path('credit_card/<bill_id>/operation/<pk>/remove_cardop/', views.billop_remove_cardop, name='billop_remove_cardop'),
    # path('accounts/', views.AccountsView.as_view(), name='accounts'),
    # path('account/<pk>/view/', views.AccountsViewDetail.as_view(), name='account_view'),
]
