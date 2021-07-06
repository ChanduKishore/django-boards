from django.test import TestCase
from django.contrib.auth.models import User
from django.core import mail
from django.urls import reverse,resolve

class PasswordResetMailTest(TestCase):

	def setUp(self):
		email='reachingdinesh@gmail.com'
		User.objects.create_user(username='dinesh',email=email,password='159dr')
		url=reverse('password_reset')
		self.response=self.client.post(url,{'email':email})
		self.email=mail.outbox[0]

	def test_email_subject(self):
		self.assertEquals('[django boards] reset your password',self.email.subject)

	def test_email_to(self):
		self.assertEquals(['reachingdinesh@gmail.com'],self.email.to)

	def test_email_body(self):
		context=self.response.context
		token=context.get('token')
		uid=context.get('uid')

		password_reset_token_url=reverse('password_reset_confirm',kwargs={'uidb64':uid,'token':token})

		self.assertIn(password_reset_token_url,self.email.body)
		self.assertIn('dinesh',self.email.body)
		self.assertIn('reachingdinesh@gmail.com',self.email.body)

	