from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.home, name='db-home'),
    path('about/', views.about, name='db-about'),
    
    path('clones/', views.clones, {"exportCSV": False}, name='db-clones'),
    path('clones/export_csv/', views.clones, {"exportCSV": True}, name='clones-csv'), #export url for main clones page
    path('clones/<str:qs_id>/', views.dynamic_clone_view, {"exportCSV": False}, name='clone-details'), #clone url generation
    path('clones/<str:qs_id>/export_csv/', views.dynamic_clone_view, {"exportCSV": True}, name='papers-using-clone-csv'), #export url for papers of a clone
    
    path('papers/', views.papers, {"exportCSV": False}, name='db-papers'),
    path('papers/export_csv/', views.papers, {"exportCSV": True}, name='papers-csv'), #export url for main papers page
    path('papers/<str:index>/', views.dynamic_paper_view, {"exportCSV": False}, name='paper-details'), #clone url generation
    path('papers/<str:index>/export_csv', views.dynamic_paper_view, {"exportCSV": True}, name='clones-in-paper-csv'), #export url for clones in a paper
    
    path('counts_chart/', views.counts_chart, name='counts-chart'),
]