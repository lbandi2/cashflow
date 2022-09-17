from django.urls import path

from . import views

app_name = 'categories'

urlpatterns = [
    path('', views.CatIndexView.as_view(), name='index'),
    path('add/', views.CatAddView.as_view(), name='add'),
    path('<pk>/edit/', views.CatEditView.as_view(), name='edit'),
    path('<pk>/delete/', views.CatDeleteView.as_view(), name='delete'),
    path('<pk>/keyword_add/', views.KwAddView.as_view(), name='add_keyword'),
    # path('keyword/<pk>/edit/', views.KeywordEditView.as_view(), name='edit_keyword'),
    path('<pk>/keyword_delete/<kw>/', views.remove_keyword, name='delete_keyword'),
]
