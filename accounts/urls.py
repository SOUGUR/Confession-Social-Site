# accounts/urls.py
from django.urls import path
from accounts.views import register, user_login, user_logout,home, postconfession, view_post, start, aboutus, like_post

urlpatterns = [
    path('', start, name='start'),
    path('aboutus/', aboutus, name='aboutus'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('home/', home, name='home'),
    path('postconfession/', postconfession, name='postconfession'),
    path('viewpost/', view_post, name='viewpost'),
    path('post/<int:post_id>/like/', like_post, name='like_post'),
]
