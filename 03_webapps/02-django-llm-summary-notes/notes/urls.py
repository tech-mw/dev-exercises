from django.urls import path
from notes import views

app_name = 'notes'

urlpatterns = [
    path('', views.IndexView, name='index')
]
