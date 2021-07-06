from django.test import TestCase
from django.urls import reverse,resolve
from django.contrib.auth.models import User


class LoginRequiredPasswordChangeTest(TestCase):

	def test_redirection(self):
		url=reverse('password_change')
		login_url=reverse('login')
		response=self.client.get(url)
		self.assertRedirects(response, f'{login_url}?next={url}')


class PasswordChangeTestCase(TestCase):
	def setUp(self,data={}):
		self.user = User.objects.create_user(username='dinesh',email='reachingdinesh@gmail.com',password='old_password')
		self.client.login(username='dinesh',password='old_password')
		self.url=reverse('password_change')
		self.response = self.client.post(self.url,data)

class SuccessfullPasswordChangeTest(PasswordChangeTestCase):
	def setUp(self):
		super().setUp({
			'old_password':'old_password',
			'new_password1':'new_password',
			'new_password2':'new_password'
			})

	def test_redirection(self):
		password_change_done_url=reverse('password_change_done')
		self.assertRedirects(self.response, password_change_done_url)

	def test_password_changed(self):
		self.user.refresh_from_db()
		self.assertTrue(self.user.check_password('new_password'))

	def test_user_authentication(self):
		home_url=reverse('home')
		response=self.client.get(home_url)
		user=response.context.get('user')
		self.assertTrue(user.is_authenticated)

class InvalidPasswordChangeTest(PasswordChangeTestCase):

	def test_redirection(self):
		'''invalid data must return to same page'''
		response=self.client.get(self.url)
		self.assertEquals(response.status_code,200)

	def test_password_not_changed(self):
		self.user.refresh_from_db()
		self.assertTrue(self.user.check_password('old_password'))

	def test_form_errors(self):
		form=self.response.context.get('form')
		self.assertTrue(form.errors)
