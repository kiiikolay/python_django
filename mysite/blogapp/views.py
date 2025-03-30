from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.syndication.views import Feed
from django.urls import reverse, reverse_lazy

from .models import Tag, Author, Article, Category

class ArticleListView(ListView):
    queryset = (Article.objects
                .defer("content")
                .select_related("author", "category", )
                # .select_related("category")
                .prefetch_related('tags').all()
                .filter(pub_date__isnull=False)
                .order_by("-pub_date")
    )

class ArticleDetaleView(DetailView):
    model = Article

class LatestArticlesFeed(Feed):
    title = "Блог статей"
    description = "Изменения поступают в блок когда вы изменяете содержимое или создаёте новые статьи"
    link = reverse_lazy("blog:articles")

    def items(self):
        return (
            Article.objects
                .defer("content")
                .select_related("author", "category", )
                # .select_related("category")
                .prefetch_related('tags').all()
                .filter(pub_date__isnull=False)
                .order_by("-pub_date")[:5]
    )

    def item_title(self, item: Article):
        return item.title

    def item_description(self, item: Article):
        return item.content[:200]
