from django.test import TestCase
from django.urls import reverse,resolve
from django.contrib.auth import views as auth_views

class PasswordResetDoneTest(TestCase):
	def test_page_staus_code(self):
		url=reverse('password_reset_done')
		response=self.client.get(url)

		self.assertEquals(response.status_code,200)

	def test_page_resolve_view(self):
		view=resolve('/reset/done/')

		self.assertEquals(view.func.view_class,auth_views.PasswordResetDoneView)