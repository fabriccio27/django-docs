from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from .models import BlogPost
from .forms import BlogPostForm
# Create your views here.

# esto lo podria hacer con una class based view
def index(request):
    blogPosts = BlogPost.objects.all()
    return render(request, "blog/index.html", {"posts":blogPosts})

def create_post(request):
    if request.method=="POST":
        #pueblo una instancia de form con lo que vino en la request
        #a la instancia aplico metodo de validacion.
        form = BlogPostForm(request.POST)
        if form.is_valid():
            #crear objeto y guardarlo
            title = form.cleaned_data["title"]
            body = form.cleaned_data["body"]
            p = BlogPost(title=title, body=body)
            p.save()
            #la sintaxis para reverse es la misma que si estuviera usando {% url %} en el template
            return HttpResponseRedirect(reverse("blog:success"))
        else:
            return render(request, "blog/create_post.html", {"form":form})
    form =  BlogPostForm() #porque la estaria pasando vacia
    return render(request, "blog/create_post.html", {'form':form})

def success(request):
    return render(request, "blog/success.html",{})