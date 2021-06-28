from django.test import SimpleTestCase, TestCase
from django.utils import timezone

import datetime
from .models import Question
# Create your tests here.

class QuestionModelTests(SimpleTestCase):
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