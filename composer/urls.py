from django.urls import path

from . import views

app_name = 'composer'

urlpatterns = [
    path('', views.index, name='index'),
    path('download/', views.download, name='download'),
    path('produce/', views.produce, name='produce'),
    path('upload/', views.user_upload, name='upload'),
    path('team/', views.team, name='team'),
    path('learn/', views.learn, name='learn'),
    path('sheet/', views.download_sheet, name='sheet'),
    path('comparison/', views.comparison, name='comparison'),
]