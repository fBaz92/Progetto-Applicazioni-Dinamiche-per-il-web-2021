from django.urls import path
from . import views

urlpatterns = [path ('login', views.login_page, name = 'login_page'), 
path ('', views.index, name = 'index'), path ('register', views.register, name = 'register'), 
path ('logout', views.loggout, name = 'logout'), path ('Login', views.Login, name = 'Login'), path ('user/<str:username>', views.user, name = 'user'),
path ('getuser', views.getuser, name = 'getuser'), path('csrf', views.generate_csrf), path ('hide', views.hide, name = 'hide'), path ('retrive', views.retrive, name = 'retrive') ]

