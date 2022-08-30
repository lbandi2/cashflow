from django.urls import path

from . import views

app_name = 'trips'

urlpatterns = [
    path('', views.TripIndexView.as_view(), name='index'),
    path('add/', views.TripAddView.as_view(), name='add'),
    path('<pk>/edit/', views.TripEditView.as_view(), name='edit'),
    path('<pk>/delete/', views.TripDeleteView.as_view(), name='delete'),
]
