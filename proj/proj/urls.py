"""proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls'), name='home'),
    path('portal/', include('portal.urls'), name='portal'),
    path('dolar/', include('dolar.urls'), name='dolar'),
    path('cashflow/', include('cashflow.urls'), name='cashflow'),
    path('accounts/', include('accounts.urls'), name='accounts'),
    path('credit_cards/', include('credit_cards.urls'), name='credit_cards'),
    path('bills/', include('bills.urls'), name='bills'),
    path('categories/', include('categories.urls'), name='categories'),
]
