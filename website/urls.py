from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('products/', views.products, name='products'),
    path('projects/', views.projects, name='projects'),
    path('contact/', views.contact, name='contact'),
    path('gallery/', views.gallery_list, name='gallery_list'),  # Added trailing slash
    path('item/<slug:slug>/', views.gallery_detail, name='gallery_detail'),
]