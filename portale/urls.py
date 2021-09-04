from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.Login, name = 'Login'),  
    path('register', views.register, name = 'register'), 
    path('logout', views.Logout, name = 'Logout'), 
    path('user/<str:username>', views.user, name = 'user'),
    path('getuser', views.getuser, name = 'getuser'), 
    path('csrf', views.generate_csrf), 
    path('hide', views.hide, name = 'hide'),
    path('retrive', views.retrive, name = 'retrive'), 
    path('getupdates', views.GetUpdates, name = 'getupdates'), 
    path('loadupdates', views.LoadUpdates, name = 'loadupdates'),
    path('user/notices/<int:primary_key>', views.detail_notice, name='detail_notice'),
    #path('user/lesson/<int:primary_key>', views.detail_lesson, name='detail_lesson'),
    #path('user/office_hour/<int:primary_key>', views.detail_office_hour, name='detail_office_our'),
]

