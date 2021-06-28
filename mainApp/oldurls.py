from django.urls import path
from . import views 


app_name = "mainApp"

""" app_name lo uso para anteponer el valor en url de template, porque cuando tengo varios servicios tengo que indicarle a cual
de todos lo servicios le estoy apuntando """

""" url, cual es la view function que va a correrse cuando haya match de la ruta y como apunto a la view desde template """
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:question_id>/", views.detail, name="detail"),
    path("<int:question_id>/results/", views.results, name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
]

""" esto es la config de paths para esta app en particular, lo que tengo que hacer es que la URLconfig del project apunte aca """

