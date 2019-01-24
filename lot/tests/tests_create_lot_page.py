"""
Test that only authorized users can add Parking Lots
"""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse
from ..forms import CreateLotForm
from ..models import Lot
from ..views import NewLotView


class CreateNewLotViewBase(TestCase):
    def setUp(self):
        self.url = reverse('create_lot')
        User.objects.create_user(username='awesomeo',
                                 email='hacker@chammy.info',
                                 password='733t')


class CreateNewLotViewAuthorizedTest(CreateNewLotViewBase):
    def setUp(self):
        super().setUp()
        self.client.login(username='awesomeo', password='733t')
        self.response = self.client.get(self.url)
        self.data = {
            'group_name': 'acme company',
            'description':'introduction to data science',
            'location': 'new york',
            'start_date': '2019-01-01',
            'end_date': '2019-01-03',
            'timezone': 'America/Los_Angeles'
        }

    def test_create_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_lot_url_resolves_create_new_view(self):
        view = resolve('/lots/new/')
        self.assertEquals(view.func.view_class, NewLotView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, CreateLotForm)

    def test_new_parking_lot_valid_post_data(self):
        self.client.post(self.url, self.data)
        self.assertTrue(Lot.objects.exists())

    def test_new_parking_lot_no_redirect_and_displays_errors_on_empty_fields(self):
        blank_data = {key:'' for key in self.data}
        response = self.client.post(self.url, blank_data)
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Lot.objects.exists())
        self.assertTrue(form.errors)

    def test_new_parking_lot_no_redirect_and_displays_errors_on_invalid_post_data(self):
        for leave_out in self.data:
            malformed_data = {key: value for key, value in self.data.items() if key != leave_out}
            response = self.client.post(self.url, malformed_data)
            form = response.context.get('form')
            self.assertEquals(response.status_code, 200)
            self.assertFalse(Lot.objects.exists())
            self.assertTrue(form.errors)


class LoginRequiredCreateNewLotViewTest(CreateNewLotViewBase):
    def test_redirect(self):
        response = self.client.get(self.url)
        login_url = reverse('login')
        self.assertRedirects(response, f'{login_url}?next={self.url}')


class LoginRequiredEditNewLotViewTest(CreateNewLotViewBase):
    def setUp(self):
        super().setUp()
        Lot.objects.create(group_name='acme company',
                           description='we love umbrellas',
                           location='London, UK')

    def test_redirect(self):
        url = reverse('lot_update', kwargs={'lot_id': 'acme-company'})
        login_url = reverse('login')
        response = self.client.get(url)
        self.assertRedirects(response, f'{login_url}?next={url}')
