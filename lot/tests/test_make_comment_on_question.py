from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse
from ..models import Lot, Question, Post
from ..views import post_comment


class ReplyTopicTestCase(TestCase):
    """
    Base case to be used in all reply topic views.
    Takes care of basic setup
    """
    def setUp(self):
        self.lot = Lot.objects.create(group_name='Umbrella corp',
                                      description='acme umbreallas',
                                      location='London, UK')
        self.username = 'noone'
        self.password = '123456'
        self.email = 'noone@nowhere.com'
        user = User.objects.create_user(username=self.username,
                                        email=self.email,
                                        password=self.password)
        self.question = Question.objects.create(subject='How to say hello in Mandarin',
                                                lot=self.lot,
                                                starter=user)
        Post.objects.create(message="Is it ni hao?", question=self.question,
                            created_by=user)
        self.url = reverse('post_comment', kwargs={'lot_id': self.lot.slug,
                                                   'question_pk': self.question.pk})

class PostCommentTests(ReplyTopicTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/lots/umbrella-corp/questions/1/post_comment/')
        self.assertEquals(view.func, post_comment)

    def test_form_inputs(self):
        """
        The view contains two inputs: csrf, message textarea
        """
        self.assertContains(self.response, '<input', 1)
        self.assertContains(self.response, '<textarea', 1)

