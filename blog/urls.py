from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("create/", views.create_post, name="create_post"),
    path("", views.index, name="index"),
    path("success/", views.success, name="success")
]