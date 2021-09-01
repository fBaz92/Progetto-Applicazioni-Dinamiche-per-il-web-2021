from django.urls import path
from . import views

urlpatterns = [path ('login', views.Login, name = 'Login'), 
path ('', views.index, name = 'index'), path ('register', views.register, name = 'register'), 
path ('logout', views.Logout, name = 'Logout'), path ('user/<str:username>', views.user, name = 'user'),
path ('getuser', views.getuser, name = 'getuser'), path('csrf', views.generate_csrf), path ('hide', views.hide, name = 'hide'),
path ('retrive', views.retrive, name = 'retrive'), path ('getupdates', views.GetUpdates, name = 'getupdates'), path ('loadupdates', views.LoadUpdates, name = 'loadupdates')  ]

