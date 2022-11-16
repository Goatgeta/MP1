from django.contrib import admin
from django.urls import path
from Home import views

urlpatterns = [
    path("", views.myhome, name="home"),
    path("login/", views.signin, name="signin"),
    path("register/", views.register, name="register"),
    path("logout/", views.signout, name="logout"),
    path("about/", views.about, name="about"),
    path("blog/", views.blog, name="blog"),
    path("contact/", views.contact, name="contact"),
    path("details/", views.details, name="details"),
    path("gallery/", views.gallery, name="gallery"),
    path("index1/", views.index1, name="index1"),
    path("services/", views.services, name="services"),
    path("shopdet/", views.shopdet, name="shopdet"),
    path("shop/", views.shop, name="shop"),

]