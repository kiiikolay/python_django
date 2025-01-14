from django.contrib import admin
from django.contrib.admin.templatetags.admin_list import admin_actions
from django.db.models import QuerySet
from django.http import HttpRequest

from .models import Profile

admin.site.register(Profile)
