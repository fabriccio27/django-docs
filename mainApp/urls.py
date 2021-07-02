from django.urls import path
from . import views 


app_name = "mainApp"

""" The DetailView generic view expects the primary key value captured from the URL to be called "pk",
 so we’ve changed question_id to pk for the generic views. """

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('<int:pk>/', views.DetailView.as_view(), name="detail"),
    path('<int:pk>/results/', views.ResultsView.as_view(), name="results"),
    path('<int:question_id>/vote/', views.vote, name="vote"),
    path('success/', views.success, name="success"),
    path('upload/', views.upload_file, name="upload_file")
]

""" esto es la config de paths para esta app en particular, lo que tengo que hacer es que la URLconfig del project apunte aca """

