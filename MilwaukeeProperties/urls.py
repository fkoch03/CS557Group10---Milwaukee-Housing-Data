"""
URL configuration for CS557Group10 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from django.urls import path, include
from .import views
from .views import *

urlpatterns = [
path('', views.HomeView.as_view(), name='home'),
path('property/<int:property_id>/', views.PropertyView.as_view(), name='property'),
path('favorites/', views.FavoritesView.as_view(), name='favorites'),
path('explore/', views.SearchView.as_view(), name='search'),
path('', include('django.contrib.auth.urls') ),
path('district/<int:district_id>/', views.HomeView.as_view(), name='district'),
path('realtor/<int:realtor_id>/', views.HomeView.as_view(), name='realtor'),
path("signup/", SignUpView.as_view(), name="signup"),




]
