from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.http import HttpResponseRedirect

from .models import Choice, Question

class IndexView(generic.ListView):
    """ 
    Si a una generic no le paso el template_name,
    va a buscar templates que coincidan con el formato esperado de django,
    por ejemplo para una view de Detail va buscar 
    <app name>/<model name>_detail.html
    """
    template_name = 'mainApp/index.html'
    context_object_name = 'latest_question_list' #en el template tengo los for en base a una variable llamada asi

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name =  "mainApp/detail.html"

class ResultsView(generic.DetailView):
    model = Question
    template_name = "mainApp/results.html"

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
        return HttpResponseRedirect(reverse('mainApp:results', args=(question.id,) ))
        # the comma is important in args, because it stablishes a difference between a tuple and some arguments
        # reverse function helps avoid having to hardcode a URL in the view function. 
        # It is given the name of the view that we want to pass control to, and the variable portion of the URL pattern
        # that points to that view.

    