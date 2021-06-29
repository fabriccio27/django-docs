from django.contrib import admin
from .models import Question, Choice
# Register your models here.

""" By registering the Question model with admin.site.register(Question), Django was able to construct a default form 
representation. Often, you’ll want to customize how the admin form looks and works. 
You’ll do this by telling Django the options you want when you register the object. """

#podria poner admin.site.register(Choice) pero me daria una pagina donde agrego una choice 
#y tengo que vincularla a una question manualmente. Seria mejor que cuando cree question ya me de para agregarle choices

#otro modo de layout es StackedInline, pero ocupa mucho espacio
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3 


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date'] #como en models puse que es un DatetimeField, django sabe que filtros poner en la pagina de admin
    """ search_fields = ['question_text'] funciona como uno intuye """
    fieldsets = [
        #primer argumento de la tupla es titulo de la mini seccion dentro de esta pagina de admin
        (None, {'fields':['question_text']}),
        ('Date information', {'fields':['pub_date'], 'classes':['collapse']}),
    ]
    inlines = [ChoiceInline]

admin.site.register(Question, QuestionAdmin)
 