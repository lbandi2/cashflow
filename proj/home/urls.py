from django.urls import path

from . import views

app_name = 'home'

urlpatterns = [
    path('', views.SigninView.as_view(), name='login'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('logout/', views.LogoutInterfaceView.as_view(), name='logout'),
]
