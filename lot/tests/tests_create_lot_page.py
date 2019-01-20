from django.test import TestCase
from django.urls import resolve, reverse
from ..views import NewLotView


class CreateNewLotViewTest(TestCase):
    def setUp(self):
        self.url = reverse('create_lot')

    def test_create_lot_status_code(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)

    def test_url_resolves_to_create_lot(self):
        view = resolve('/lots/new/')
        self.assertEquals(view.func.view_class, NewLotView)
