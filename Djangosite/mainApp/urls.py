from django.urls import path

from . import views

urlpatterns = [
    path('', views.welcome, name='welcome-page'),
    path('about', views.about, name='about-page'),
    path('contact', views.contact, name='contact-page'),
    path('features', views.features, name='features-page'),
    path('login', views.login, name='login-page'),
    path('home', views.home, name='home-page'),
    path('home/benchmarking', views.benchmarking, name='benchmarking-page'),
    path('home/user', views.user, name='user-profile')
]