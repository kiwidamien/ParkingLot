"""
Test Lot List View, and ensure that only logged in users 
can access it
"""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from ..models import Lot
from ..views import LotListView


class LotListViewBase(TestCase):
    def setUp(self):
        self.lot = Lot.objects.create(group_name='Umbrella Co',
                                      description='Intro to DS',
                                      location='New York, New York')
        self.url = reverse('list_lots')
        self.user = User.objects.create_user(username='registered',
                                             email='chammy@bugmenot.com',
                                             password='123')
        self.response = self.client.get(self.url)


class LotListViewLoggedInTest(LotListViewBase):
    def setUp(self):
        super().setUp()
        self.client.login(username='registered', password='123')
        self.response = self.client.get(self.url)

    def test_lot_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_lot_url_resolves_lot_list_view(self):
        view = resolve('/lots/')
        self.assertEquals(view.func.view_class, LotListView)

    def test_lot_list_view_contains_link_to_lot_view(self):
        single_lot_url = reverse('list_questions', kwargs={'lot_id':
                                                           self.lot.slug})
        self.assertContains(self.response, f'href="{single_lot_url}"')

    def test_only_one_lot_registered(self):
        self.assertContains(self.response, 'Umbrella Co', 1)
        # should have one tr for the heading, another for the single
        # entry
        self.assertContains(self.response, '<tr', 2)

class LoginRequiredForLotListViewTest(LotListViewBase):
    def test_redirection(self):
        login_url = reverse('login')
        self.assertRedirects(self.response, f'{login_url}?next={self.url}')


