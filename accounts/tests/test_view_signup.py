from django.test import TestCase
from django.urls import reverse,resolve
from accounts.views import signup
from django.contrib.auth.models import User
from accounts.forms import NewSignUpForm

class SignupTest(TestCase):
	def setUp(self):
		url=reverse('signup')
		self.response=self.client.get(url)

	def test_signup_page_status_code(self):
		self.assertEquals(self.response.status_code,200)

	def test_signup_page_reslove_views(self):
		views=resolve('/signup/')

		self.assertEquals(views.func,signup)

	def test_csrf(self):
		self.assertContains(self.response, 'csrfmiddlewaretoken')

	def test_singup_page_contain_form(self):
		form=self.response.context.get('form')
		self.assertIsInstance(form,NewSignUpForm)

	def test_form_inputs(self):
		'''form must contain 5 input
		csrf, username, email, password1, password2'''

		self.assertContains(self.response,'<input',5)
		self.assertContains(self.response,'type="text"',1)
		self.assertContains(self.response,'type="email"',1)
		self.assertContains(self.response,'type="password"',2)


class SuccessfullSignupTests(TestCase):

	def setUp(self):
		url=reverse('signup')
		data={
				'username':"dinesh",
				'email':'rachingdinesh@gmail.com',
				'password1':'din159raju',
				'password2': 'din159raju'
		}

		self.response=self.client.post(url,data)
		self.home_url=reverse('home')

	def test_redirection(self):
		self.assertRedirects(self.response,self.home_url)

	def test_user_creation(self):
		self.assertTrue(User.objects.exists())

	def test_user_athentication(self):
		response=self.client.get(self.home_url)
		user=response.context.get('user')
		self.assertTrue(user.is_authenticated)

class InvalidSignupTests(TestCase):

	def setUp(self):
		url=reverse('signup')
		self.response=self.client.post(url,{})

	def test_signup_status_code(self):
		self.assertEquals(self.response.status_code,200)

	def test_dont_create_user(self):
		self.assertFalse(User.objects.exists())

	def test_signup_form_errors(self):
		form=self.response.context.get('form')
		self.assertTrue(form.errors)

class SignUpFormTest(TestCase):
	def test_form_contain_fields(self):
		form=NewSignUpForm()
		expected=['username','email','password1','password2']
		actual=list(form.fields)
		self.assertSequenceEqual(expected,actual)
