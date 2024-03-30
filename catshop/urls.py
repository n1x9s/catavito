from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cats/<int:cat_id>/', views.show_cat, name='show_cat'),
    path('about/', views.about, name='about'),
]
