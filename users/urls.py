from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('logout', views.logout, name='logout'),
    path('post_hackathon', views.post_hackathon, name='post_hackathon'),
]
