from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
""" Http404, """
from .models import Question, Choice
# Create your views here.

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    #armo un list comprehension y luego armo string con join a partir de la list
    """ output = ", ".join([q.question_text for q in latest_question_list] """
    context = {"latest_question_list":latest_question_list}

    #si mando el output como un HttpResponse no puedo estilizar 
    return render(request, "mainApp/index.html", context)

""" como esta ahora no importa que id pase en la ruta, porque no hace un query, solo muestra el texto de abajo """

def detail(request, question_id):
    """ como es muy comun hacer query a db y querer tirar un 404 si no esta hay un atajo para no hacer el try except de abajo """
    question = get_object_or_404(Question, pk=question_id)
    
    """ 
    try:
        question =  Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist") """

    return render(request, "mainApp/detail.html", {
        "question":question
    })

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    return render(request, "mainApp/results.html", {
        'question':question
    })

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        # whatever I send through with a form, is available as the request.POST dict, just got to hit the right key based on
        # the name of the html element, the radio buttons are all called 'choice'   
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(request, "mainApp/detail.html",{
            'question':question,
            'error_message':"You didn't select a choice."
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        """ Always return an HttpResponseRedirect after successfully dealing
        with POST data. This prevents data from being posted twice if a
        user hits the Back button. """
        return HttpResponseRedirect(reverse('mainApp:results', args=(question.id) ))
        # reverse function helps avoid having to hardcode a URL in the view function. 
        # It is given the name of the view that we want to pass control to, and the variable portion of the URL pattern
        # that points to that view.




