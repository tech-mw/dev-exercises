from django.urls import path
from . views import signup_func, login_func, board_func, detail_func, good_func, read_func, BoardCreate

urlpatterns = [
    path('signup/', signup_func, name='signup'),
    path('login/', login_func, name='login'),
    path('board/', board_func, name='board'),
    path('detail/<int:pk>', detail_func, name='detail'),
    path('good/<int:pk>', good_func, name='good'),
    path('read/<int:pk>', read_func, name='read'),
    path('create/', BoardCreate.as_view(), name='create'),
]
