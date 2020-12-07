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
    path('snippet-video/<int:boardPk>/<int:snippetPk>',
         views.snippet_video, name='snippet_video'),
    path('delete-snippet/<int:boardPk>/<int:snippetPk>',
         views.delete_snippet, name='delete_snippet'),
    path('configure', views.configure, name='configure'),
    path('download/<int:snippetPk>', views.download, name='download'),
    path('download-board/<int:boardPk>',
         views.download_board, name='download_board'),
]
