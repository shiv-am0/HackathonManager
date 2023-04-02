from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('logout', views.logout, name='logout'),
    path('post_hackathon', views.post_hackathon, name='post_hackathon'),
    path('get_hackathons', views.get_hackathons, name='get_hackathons'),
    path('register_for_hackathon', views.register_for_hackathon, name='register_for_hackathon'),
    path('get_all_submissions', views.get_all_submissions, name='get_all_submissions'),
    path('make_submission', views.make_submission, name='make_submission'),
]
