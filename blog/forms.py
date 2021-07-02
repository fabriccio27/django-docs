from .models import BlogPost
from django.forms import ModelForm

class BlogPostForm(ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'body']

    