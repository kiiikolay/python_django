from django.contrib import admin
from .models import Article, Author, Tag, Category

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = "id", "title", "content", "pub_date"

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = "name", "bio"

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name"]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]