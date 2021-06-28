## What does migrate do?
The migrate command looks at the INSTALLED_APPS setting and creates any necessary database tables according to the database settings in your mysite/settings.py file and the database migrations shipped with the app (we’ll cover those later)

## How to add the app?
To include the app in our project, we need to add a reference to its configuration class in the INSTALLED_APPS setting. The PollsConfig class is in the polls/apps.py file, so its dotted path is 'polls.apps.PollsConfig'. Edit the mysite/settings.py file and add that dotted path to the INSTALLED_APPS setting. In my case it would be `mainApp.apps.MainappConfig`.
Then run 
```
python manage.py makemigrations mainApp
```

By running makemigrations, you’re telling Django that you’ve made some changes to your models (in this case, you’ve made new ones) and that you’d like the changes to be stored as a migration.

Migrations are how Django stores changes to your models (and thus your database schema) - they’re files on disk. By now in mainApp you should have `migrations/0001_initial.py`. With `sqlmigrate` command you can pass a migration name and see what are the statements made by the db manager to map your models to a db schema. 
```
python manage.py sqlmigrate mainApp 0001
```
**There's kind of a parallelism between makemigrations and migrate and git add  and git commit**

## Access the Django shell

```
python manage.py shell
```
We’re using this instead of simply typing “python”, because manage.py sets the DJANGO_SETTINGS_MODULE environment variable, which gives Django the Python import path to your `myproject/settings.py` file. Within the shell I could import the models made in mainApp/models and run queries through the mapper.
```
from mainApp import Question
Question.objects.all()
```
Which will return a QuerySet, kind of an list with the results from the query. I could also add data to a table by creating an instance of the models with the proper field data. E.g.
```
from django.utils import timezone
q = Question(question_text='Whats new?', pub_date=timezone.now())
q.save()
```
For more details about the API for lookups and methods, check the [docs](https://docs.djangoproject.com/en/3.2/topics/db/queries/)

## Views
Each view is responsible for doing one of two things: returning an HttpResponse object containing the content for the requested page, or raising an exception such as Http404. The rest is up to you.

Your view can read records from a database, or not. It can use a template system such as Django’s – or a third-party Python template system – or not. It can generate a PDF file, output XML, create a ZIP file on the fly, anything you want, using whatever Python libraries you wan. Each service or app should have a `templates` folder with another folder inside carrying the same name as the service and inside that last folder is where the html files should be. This enable to call the templates as `app/index.html` for example.

## Generic views

Common case of basic Web development: getting data from the database according to a parameter passed in the URL, loading a template and returning the rendered template. Because this is so common, Django provides a shortcut, called the “generic views” system. You'll need to refactor the url patterns and some other things.

