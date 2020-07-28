from django.urls import path

from game.api import views

app_name = "game_api"

urlpatterns = [
    path("", views.GameList.as_view(), name="game_list"),
    path("create", views.GameCreate.as_view(), name="game_create"),
    path("update", views.GameUpdate.as_view(), name="update_game"),
    path("leaderboard", views.GameLeaderboard.as_view(), name="leaderboard")
]