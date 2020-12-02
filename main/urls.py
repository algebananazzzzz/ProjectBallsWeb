from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('signup', views.signup, name='signup'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('board/<int:boardPk>', views.board, name='board'),
    path('board-config', views.board_config, name='board_config'),
    path('board-config/<int:boardPk>', views.board_config, name='board_config'),
    path('generate-thumbnail/<int:boardPk>',
         views.generate_thumbnail, name='generate_thumbnail'),
    path('video/<int:boardPk>', views.video, name='video'),
    path('snippets/<int:boardPk>/<int:snippetPk>',
         views.snippets, name='snippets'),
    path('configure', views.configure, name='configure'),
]
