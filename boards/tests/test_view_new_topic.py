from django.urls import reverse, resolve
from django.test import TestCase
from boards.views import home,board_topics,new_topic
from boards.models import Board,Topic,Post
from django.contrib.auth.models import User
from boards.forms import NewTopicForm


class LoginReqiredNewTopictest(TestCase):
	def setUp(self):
		Board.objects.create(name='bingo',description='original style')
		self.url=reverse('new_topic',kwargs={'board_id':1})
		self.response=self.client.get(self.url)

	def test_redirection(self):
		login_url=reverse('login')
		self.assertRedirects(self.response,f"{login_url}?next={self.url}")


class NewTopicTests(TestCase):
	def setUp(self):
		Board.objects.create(name='bingo',description='bingo is lottery game')
		self.user=User.objects.create_user(username='Ram',email='ram@gmail.com',password='1475')
		self.client.login(username='Ram',password='1475')
		
	def test_new_topic_sucess_status_code(self):
		url=reverse('new_topic',kwargs={'board_id':1})
		response=self.client.get(url)
		self.assertEquals(response.status_code,200)

	def test_new_topic_status_code_not_found(self):
		url=reverse('new_topic',kwargs={'board_id':99})
		response=self.client.get(url)
		self.assertEquals(response.status_code,404)

	def test_new_topic_resloves_new_topic_views(self):
		view=resolve('/boards/1/new/')
		self.assertEquals(view.func,new_topic)

	def test_new_topic_view_contains_link_back_to_board_topics(self):
		new_topic_url=reverse('new_topic',kwargs={'board_id':1})
		board_topics_url=reverse('board_topics',kwargs={'board_id':1})
		response=self.client.get(new_topic_url)
		
		self.assertContains(response,'href="{0}"'.format(board_topics_url))

	def test_csrf(self):
		url=reverse('new_topic',kwargs={'board_id':1})
		response=self.client.get(url)
		self.assertContains(response,'csrfmiddlewaretoken')
		

	def test_new_topic_valid_post_data(self):
		url=reverse('new_topic',kwargs={'board_id':1})

		data={'subject':'test subject title','message':'test message'}

		response=self.client.post(url,data)

		self.assertTrue(Topic.objects.exists())
		self.assertTrue(Post.objects.exists())

	def test_new_topic_invalid_post_data(self):
		url=reverse('new_topic',kwargs={'board_id':1})
		response=self.client.post(url,{})
		form=response.context.get('form')

		self.assertEquals(response.status_code,200)
		self.assertTrue(form.errors)

	def test_new_topic_post_with_empty_fields(self):
		url=reverse('new_topic',kwargs={'board_id':1})
		data={'subject':'','message':''}

		response=self.client.post(url,data)
		self.assertEquals(response.status_code,200)
		self.assertFalse(Topic.objects.exists())
		self.assertFalse(Post.objects.exists())

	def test_page_contain_form(self):
		url=reverse('new_topic',kwargs={'board_id':1})
		response=self.client.get(url)

		form=response.context.get('form')

		self.assertIsInstance(form,NewTopicForm)

