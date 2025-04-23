"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
# from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
   path('', views.openpos, name = "openpos"),
   path('list_item', views.list_item, name="list_item"),
   path('view_orders', views.view_orders, name="view_orders"),
   path('to_add', views.to_add, name="to_add"),
   path('add_item', views.add_item, name="add_item"),
   path('edit_item/<int:pk>', views.edit_item, name="edit_item"),
   path('delete_item/<int:pk>/', views.delete_item, name='delete_item'),
   path('confirm_order', views.confirm_order, name="confirm_order"),
]
