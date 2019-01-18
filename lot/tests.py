"""Test the different views"""

from django.test import TestCase
from django.urls import resolve, reverse
from .views import home_page, LotListView


class HomePageTest(TestCase):
    def test_home_view_status_code(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)


    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home_page)


class LotListViewTest(TestCase):
    def test_lot_view_status_code(self):
        url = reverse('list_lots')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)


    def test_lot_url_resolves_lot_list_view(self):
        view = resolve('/lots/')
        self.assertEquals(view.func.view_class, LotListView)
