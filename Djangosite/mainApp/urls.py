from django.urls import path

from . import views

urlpatterns = [
    path('', views.welcome, name='welcome-page'),
    # path('login', views.login, name='login-page'),
    path('about', views.about, name='about-page'),
    path('contact', views.contact, name='contact-page'),
    path('features', views.features, name='features-page'),
    path('home', views.home, name='home-page'),
    path('benchmarking', views.benchmarking, name='benchmarking-page'),
    path('logout', views.logout, name='logout'),
    path('profile', views.profile, name='profile-page'),
    path('edit', views.edit, name="edit-user-page"),
    path('updateDatabaseFromApiPath/<str:metric_name>/', views.updateDatabaseByApi, name="updateDatabaseFromApi")
]
