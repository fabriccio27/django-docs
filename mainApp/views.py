from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.http import HttpResponseRedirect
from django.utils import timezone

from .models import Choice, Question
from .forms import UploadFileForm
from .utils import handle_uploaded_file

def upload_file(request):
    if request.method=="POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            #file es el atributo del form que hice con FileField
            """ During file uploads, the actual file data is stored in request.FILES. 
            Each entry in this dictionary is an UploadedFile object (or a subclass) – a wrapper around an uploaded file.
            You’ll usually use one of these methods to access the uploaded content: """

            handle_uploaded_file(request.FILES["file"])
            return HttpResponseRedirect("mainApp/success")
    else:
        form = UploadFileForm()
    return render(request, "mainApp/upload.html", {
        'form':form
        })
        
def success(request):
    render(request, 'mainApp/success.html', {})

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
        """ __lte es less than or equal """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name =  "mainApp/detail.html"
    #esto de aca abajo lo pongo porque tengo que filtrar preguntas que tienen fecha futura a las que podrian llegar por url
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

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

    