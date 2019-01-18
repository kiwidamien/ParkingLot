from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from ..models import Lot, Question, Post
from ..views import question_comments


class PostsOnQuestionTests(TestCase):
    def setUp(self):
        lot = Lot.objects.create(group_name='umbrella corp',
                                 description='ACME umbrellas',
                                 location='London, UK')
        user = User.objects.create_user(username='test',
                                        email='test@chammy.info',
                                        password='123456')
        question = Question.objects.create(subject='Hello', lot=lot,
                                           starter=user)
        Post.objects.create(message='Latin is cool', question=question,
                            created_by=user)
        url = reverse('question_comments', kwargs={'lot_id': 'umbrella-corp',
                                                 'question_pk': question.pk})
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/lots/umbrella-corp/questions/1/')
        self.assertEquals(view.func, question_comments)
