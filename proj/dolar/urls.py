from django.urls import path

from . import views

app_name = 'dolar'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('archive/', views.ArchiveView.as_view(), name='archive'),
    path('history/bna/', views.BNAHistory.as_view(), name='history_bna'),
    path('history/bbva/', views.BBVAHistory.as_view(), name='history_bbva'),
    path('history/santander/', views.SantanderHistory.as_view(), name='history_santander'),
    path('history/patagonia/', views.PatagoniaHistory.as_view(), name='history_patagonia'),
    path('history/blue/', views.BlueHistory.as_view(), name='history_blue'),
    path('history/cop/', views.COPHistory.as_view(), name='history_cop'),
]
