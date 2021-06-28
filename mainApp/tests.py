from django.test import SimpleTestCase, TestCase
from django.utils import timezone
from django.urls import reverse

import datetime
from .models import Question
# Create your tests here.

def create_question(question_text, days):
    time =  timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionDetailViewTest(TestCase):
    
    def test_future_question(self):
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse('mainApp:detail', args=(future_question.id,))
        response = self.client.get(url)
        #no tendria que estar disponible, asi que deberia arrojar un 404 esa solicitud del cliente
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        past_question = create_question(question_text="Past question.", days=-5)
        url = reverse('mainApp:detail', args=(past_question.id,))
        response = self.client.get(url)
        #aca testea que el html de la respuesta tengo el texto de question_text
        self.assertContains(response, past_question.question_text)
        


class QuestionIndexViewTest(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse('mainApp:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('mainApp:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_future_question(self):
        question = create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('mainApp:index'))
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['latest_question_list'],[])
    
    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('mainApp:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

class QuestionModelTests(TestCase):
    """ databases = {'testHere'} """
    def test_was_published_recently_with_future_question(self):

        time = timezone.now() + datetime.timedelta(days=30)
        futureQuestion = Question(pub_date=time)
        self.assertIs(futureQuestion.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        oldQuestion = Question(pub_date=time)
        self.assertIs(oldQuestion.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recentQuestion = Question(pub_date=time)
        self.assertIs(recentQuestion.was_published_recently(), True)