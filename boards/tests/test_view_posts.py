from django.test import TestCase
from boards.views import Board,Topic,Post
from django.contrib.auth.models import User
from django.urls import reverse,resolve
from boards.views import PostListView


class TopicPostsTest(TestCase):
	def setUp(self):
		self.board=Board.objects.create(name='mangoDB',description='relational database')
		user=User.objects.create_user(username='dinesh',email='reachingdinesh@gmail.com', password='dr159')
		self.topic=Topic.objects.create(subject='hello', board=self.board, starter=user)
		post=Post.objects.create(message='nothing special', topic=self.topic, created_by=user)
		url=reverse('topic_posts', kwargs={'board_id':self.board.id,'topic_id':self.topic.id})
		self.response=self.client.get(url)

	def test_topic_posts_status_code(self):
		self.assertEquals(self.response.status_code,200)

	def test_topic_posts_resolve_view(self):
		view=resolve(f'/boards/{self.board.id}/topics/{self.topic.id}/')
		self.assertEquals(view.func.view_class, PostListView)
