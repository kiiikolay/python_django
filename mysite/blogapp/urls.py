from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import (
    ArticleListView,
    ArticleDetaleView,
    LatestArticlesFeed,
)

app_name = "blog"

urlpatterns = (
    path("articles/", ArticleListView.as_view(), name="articles"),
    path("articles/<int:pk>/", ArticleDetaleView.as_view(), name="article"),
    path("articles/feed/", LatestArticlesFeed(), name="feed"),

)