from django.shortcuts import render
from django.views.generic import ListView
from .models import Tag, Author, Article, Category

class OrdersListViev(ListView):
    queryset = (Article.objects
                .defer("content")
                .select_related("author", "category", )
                # .select_related("category")
                .prefetch_related('tags').all()
    )

