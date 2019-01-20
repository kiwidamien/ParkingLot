from django.test import TestCase
from django.urls import resolve, reverse
from ..views import home_page
from ..models import Lot

class HomePageTest(TestCase):
    def setUp(self):
        self.lot = Lot.objects.create(group_name="ACME umbrella co",
                                      description="Intro to data science",
                                      location="New York, New York")
        self.url = reverse('home')
        reverse_kwargs = {'lot_id': 'acme-umbrella-co'}
        self.redirect_url = reverse('list_questions', kwargs=reverse_kwargs)

    def test_home_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home_page)

    def test_csrf(self):
        response = self.client.get(self.url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_redirect_to_valid_parking_log(self):
        data = {
            'lot_slug': 'acme-umbrella-co',
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, self.redirect_url)

    def test_redirect_to_parking_lot_wrong_spaces_and_caps(self):
        data = {
            'lot_slug': 'ACME Umbrella Co'
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, self.redirect_url)

    def test_redirect_fails_to_wrong_lot_slug(self):
        data = {
            'lot_slug': 'not a company'
        }
        response = self.client.post(self.url, data)
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)

    def test_error_on_empty_form(self):
        response = self.client.post(self.url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)
