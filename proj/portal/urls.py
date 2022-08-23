from django.urls import path

from . import views

app_name = 'portal'

urlpatterns = [
    path('', views.PortalView.as_view(), name='index')
]
