from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.test import TestCase
from django.urls import reverse,resolve
from django.core import mail
from django.contrib.auth.forms import PasswordResetForm,SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views

class PasswordResetTest(TestCase):

	def setUp(self):
		url=reverse('password_reset')
		self.response=self.client.get(url)

	def test_password_reset_staus_code(self):
		self.assertEquals(self.response.status_code,200)

	def test_password_reset_resolve_view(self):
		view=resolve('/reset/')
		self.assertEquals(view.func.view_class,auth_views.PasswordResetView)

	def test_csrf_token(self):
		self.assertContains(self.response,'csrfmiddlewaretoken')

	def test_password_reset_inputs(self):
		self.assertContains(self.response,'<input',2)
		self.assertContains(self.response,'type="email"',1)

	def test_contains_form(self):
		form=self.response.context.get('form')
		self.assertIsInstance(form,PasswordResetForm)


class SuccessfullPasswordResetTest(TestCase):

	def setUp(self):
		email='reachingdinesh@gmail.com'
		User.objects.create_user(username='dinesh',email=email,password='159dr')
		url=reverse('password_reset')
		self.response=self.client.post(url,{'email':email})

	def test_redirection(self):
		url=reverse('password_reset_done')
		self.assertRedirects(self.response,url)

	def test_send_password_reset_mail(self):
		self.assertEquals(1,len(mail.outbox))

class InvalidPasswordResetTest(TestCase):

	def setUp(self):
		email='doesnotexists@gmail.com'
		url=reverse('password_reset')
		self.response=self.client.post(url,{'email':email})

	def test_redirection(self):
		url=reverse('password_reset_done')
		self.assertRedirects(self.response,url)

	def test_send_password_reset_mail(self):
		self.assertEquals(0,len(mail.outbox))


class PasswordResetConfirmTest(TestCase):
	def setUp(self):
		user=User.objects.create_user(username='dinesh',email='reachingdinesh@gmail.com',password='dr159')

		self.uid = urlsafe_base64_encode(force_bytes(user.pk))
		self.token = default_token_generator.make_token(user)
		url=reverse('password_reset_confirm',kwargs={'uidb64':self.uid,'token':self.token})

		self.response = self.client.get(url,follow=True)

	def test_page_status_code(self):

		self.assertEquals(self.response.status_code, 200)

	def test_csrf(self):
		self.assertContains(self.response,'csrfmiddlewaretoken')


	def test_conatians_form(self):
		form=self.response.context.get('form')
		self.assertIsInstance(form,SetPasswordForm)

	def test_page_inputs(self):
		self.assertContains(self.response,'<input',3)
		self.assertContains(self.response,'type="password"',2)

