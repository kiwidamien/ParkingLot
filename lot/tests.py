"""Test the different views"""

from django.test import TestCase
from django.urls import resolve, reverse
from .views import home_page, new_question, questions_in_lot, LotListView
from .models import Lot


class HomePageTest(TestCase):
    def test_home_view_status_code(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home_page)


class LotListViewTest(TestCase):
    def setUp(self):
        self.lot = Lot.objects.create(group_name='Umbrella Co',
                                      description='ACME Raingear 6',
                                      location='London, UK')
        url = reverse('list_lots')
        self.response = self.client.get(url)

    def test_lot_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_lot_url_resolves_lot_list_view(self):
        view = resolve('/lots/')
        self.assertEquals(view.func.view_class, LotListView)

    def test_lot_list_view_contains_link_to_lot_view(self):
        single_lot_url = reverse('list_questions', kwargs={'lot_id':
                                                           self.lot.slug})
        self.assertContains(self.response, f'href="{single_lot_url}"')


class LotQuestionListTests(TestCase):
    def setUp(self):
        Lot.objects.create(group_name="Umbrella Corp",
                           description="Acme Raingear 6",
                           location="London, UK")

    def test_lot_quetsions_view_success_status_code(self):
        url = reverse('list_questions', kwargs={'lot_id': 'umbrella-corp'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_lot_questions_view_not_found_status_code(self):
        url = reverse('list_questions', kwargs={'lot_id': 'nowhere-co'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_lot_questions_url_resolves_list_of_questions_view(self):
        view = resolve('/lots/umbrella-corp/')
        self.assertEquals(view.func, questions_in_lot)


class NewQuestionTests(TestCase):
    def setUp(self):
        Lot.objects.create(group_name="Umbrella Corp",
                           description="Acme Raingear 6",
                           location="London, UK")

    def test_new_topic_view_success_status_code(self):
        url = reverse('new_question', kwargs={'lot_id': 'umbrella-corp'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_new_tpoic_not_found_status_code(self):
        url = reverse('new_question', kwargs={'lot_id': 'nowhere-co'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_new_topic_url_resolves_new_topic_view(self):
        view = resolve('/lots/umbrella-corp/new/')
        self.assertEquals(view.func, new_question)
