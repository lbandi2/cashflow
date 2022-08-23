from django.urls import path

from . import views

app_name = 'categories'

urlpatterns = [
    path('', views.CatIndexView.as_view(), name='index'),
    path('add/', views.CatAddView.as_view(), name='add'),
    path('<pk>/edit/', views.CatEditView.as_view(), name='edit'),
]
