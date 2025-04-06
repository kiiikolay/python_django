from random import random
from http.client import responses
from itertools import product
from pkgutil import resolve_name
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LogoutView
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.template.context_processors import request
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import Profile
from .forms import ProfileForm
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _, gettext as __, ngettext_lazy
from django.views.decorators.cache import cache_page

import logging


def start_auth_view(request: HttpRequest):
    return render(request, "myauth/login.html")

class AboutMeView(TemplateView):
    template_name = "myauth/about-me.html"
    # model = Product
    queryset = Profile.objects.all()
    context_object_name = "profile"

class AboutMeDetailView(DetailView):
    template_name = "myauth/about-me-details.html"
    # model = Product
    queryset = Profile.objects.all()
    context_object_name = "profile"

class ProfileAvatarUpdateView(UserPassesTestMixin, UpdateView):
    model = Profile
    def test_func(self):
        profile = self.get_object()
        logging.warning(f"{profile.user_id}, {self.request.user.id}")
        if self.request.user.is_superuser:
            return True
        elif profile.user_id == self.request.user.id:
            return True
#     fields = "name", "description", "price", "discount", "preview"
    form_class = ProfileForm
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            "myauth:about-me-details",
            kwargs={"pk": self.object.pk},
        )


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "myauth/register.html"
    success_url = reverse_lazy("myauth:about-me")

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)

        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(
            self.request,
            username=username,
            password=password
        )
        login(request=self.request, user=user)
        return response

class MyLogoutView(LogoutView):
    next_page = reverse_lazy("myauth:login")

@user_passes_test(lambda u: u.is_superuser)
def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse("Cookie set")
    response.set_cookie("fizz", "buzz", max_age=3600)
    return response

@cache_page(60 * 2)
def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get("fizz", "default value")
    return HttpResponse(f"Cookie value: {value!r} + {random()}")

@permission_required("myauth.view_profile")
def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session["foobar"] = "spameggs"
    return HttpResponse("Session set")

@login_required
def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get("foobar", "default")
    return HttpResponse(f"Session value: {value!r}")

class FooBarView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
          return JsonResponse({'foo': 'bar', 'spam': 'eggs'})

class ProfileListView(ListView):
    template_name = 'myauth/profiles-list.html'
    # model = Profile
    context_object_name = "profiles"
    queryset = Profile.objects.all

class HelloView(View):
    welcome_message = _("welcome hello world")

    def get(self, request: HttpRequest) -> HttpResponse:
        items_str = request.GET("items") or 0
        items = int(items_str)
        products_line = ngettext_lazy(
            "one product",
            "{count} products",
            items,
        )
        products_line = products_line.format(count=items)
        return HttpResponse(
            f"<h1>{self.welcome_message}</h1>"
            f"\n<h2>{products_line}</h2>"
        )







""" ____________________________________________________________________________________
Самодельная View функция для Входа """

# def login_view(request: HttpRequest):
#     if request.method == "GET":
#         if request.user.is_authenticated:
#             return redirect('/admin/')
#
#         return render(request, 'shopapp/login.html')
#
#     username = request.POST['username']
#     password = request.POST['password']
#
#     user = authenticate(request, username=username, password=password)
#     if user:
#         login(request, user)
#         return redirect('/admin/')
#
#     return render(request, "shopapp/login.html", {"error": "Неверные значения"})
"""______________________________________________________________________
Самодельная View функция для Logout"""

# def logout_view(request: HttpRequest) -> HttpResponse:
#     logout(request)
#     return redirect(reverse("shopapp:login"))
"""______________________________________________________________________"""
