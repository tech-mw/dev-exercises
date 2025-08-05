from django.urls import path
from . views import signup_func, login_func, board_func

urlpatterns = [
    path('signup/', signup_func, name='signup'),
    path('login/', login_func, name='login'),
    path('board/', board_func, name='board'),
]
