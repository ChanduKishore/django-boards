from django.test import TestCase
from boards.models import Board, Topic, Post
from django.contrib.auth.models import User
from django.urls import reverse,resolve
from boards.views import PostUpdateView


class PostUpdateViewTestcase(TestCase):
	def setUp(self):
		self.board=Board.objects.create(name='mangoDB',description='relational database')
		self.username='dinesh'
		self.password='dr159'
		user=User.objects.create_user(username=self.username,email='reachingdinesh@gmail.com', password=self.password)
		self.topic=Topic.objects.create(subject='hello', board=self.board, starter=user)
		self.post=Post.objects.create(message='nothing special', topic=self.topic, created_by=user)
		self.url=reverse('edit_post', kwargs={
			'board_id':self.board.id,
			'topic_id':self.topic.id,
			'post_id':self.post.id
			})

class LoginRequiredPostUpdateViewTest(PostUpdateViewTestcase):
	def test_redirection(self):
		login_url=reverse('login')
		self.assertRedirects(self.client.get(self.url), f'{login_url}?next={self.url}')



class UnauthorisedPostUpdateViewTest(PostUpdateViewTestcase):
	def setUp(self):
		super().setUp()
		username='sam'
		password='dffd12'
		user=User.objects.create_user(username=username,email='reachingdinesh1@gmail.com', password=password)
		self.client.login(username=username,password=password)
		self.response=self.client.get(self.url)

	def test_page_status_code(self):
		self.assertEquals(self.response.status_code,404)
		

class PostUpdateViewTest(PostUpdateViewTestcase):
	def setUp(self):
		super().setUp()
		self.client.login(username=self.username,password=self.password)
		self.response=self.client.get(self.url)

	def test_page_status_code(self):
		self.assertEquals(self.response.status_code,200)

	def test_resolve_view(self):
		view=resolve(f'/boards/{self.board.id}/topics/{self.topic.id}/edit/{self.post.id}/')

		self.assertEquals(view.func.view_class, PostUpdateView)

	def test_csrf_token(self):
		self.assertContains(self.response,'csrfmiddlewaretoken')

	