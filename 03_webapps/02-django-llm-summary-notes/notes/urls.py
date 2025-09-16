from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from notes import views

app_name = 'notes'

urlpatterns = [
    path('', views.NoteIndex.as_view(), name='index'),
    path('signin/', LoginView.as_view(
        redirect_authenticated_user=True,
        template_name='notes/note_signin.html'
    ),
         name='signin'),
    path("signout/", LogoutView.as_view(next_page='notes:signin'), name="signout"),
    path('create/', views.NoteCreate.as_view(), name='create'),
]
