from django.db import models
from django.urls import reverse


class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(max_length=500, blank=True)

class Category(models.Model):
    name = models.CharField(max_length=40)

class Tag(models.Model):
    name = models.CharField(max_length=200)

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(null=True, blank=True)
    pub_date = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, )
    tags = models.ManyToManyField(Tag)

    def get_absolute_url(self):
        return reverse("blog:article", kwargs={"pk": self.pk})






