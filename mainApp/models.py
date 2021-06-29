import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin


# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    ) #esto me cambia el display en la pagina de admin, description va a ser el titulo de la columna si esta como TabularInline

    def was_published_recently(self):
        # si de alguna manera engaño para que pub_date sea en el futuro, para bocha de dias me va a dar true esto
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
        """ return self.pub_date >= timezone.now() - datetime.timedelta(days=1) """

    #I could call this later by querying the instance, saving it to a variable and calling q.was_published_recently()



# You can use an optional first positional argument to a Field to designate a human-readable name.

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
