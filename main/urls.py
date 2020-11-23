from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('signup', views.signup, name='signup'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('board', views.board, name='board'),
    path('snippets', views.snippets, name='snippets'),
    path('configure', views.configure, name='configure'),
    path('configure/<int:boardPk>', views.configure, name='configure'),

]
