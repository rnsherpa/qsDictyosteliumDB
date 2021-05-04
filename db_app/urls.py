from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.home, name='db-home'),
    path('clones/', views.clones, name='db-clones'),
    path('papers/', views.papers, name='db-papers'),
    path('stats/', views.stats, name='db-stats'),
    path('about/', views.about, name='db-about'),
    path('clones/<str:qs_id>/', views.dynamic_clone_view, name='clone-details'), #clone url generation
    path('papers/<str:index>/', views.dynamic_paper_view, name='paper-details'), #clone url generation
    path('counts-chart/', views.counts_chart, name='counts-chart'),
]