from django.test import TestCase
from django.urls import reverse,resolve
from boards.models import Board, Topic, Post
from django.contrib.auth.models import User


class ReplyPostViewTestCase(TestCase):
	def setUp(self):
		self.board=Board.objects.create(name='BenTen', description='cartoon nnetwork animated series')
		self.user=User.objects.create_user(username='xlr8',email='benfan@gmail.com', password='itsherotime')
		self.topic=Topic.objects.create(subject='fourarms', board=self.board, starter=self.user)
		self.post=Post.objects.create(message='hello benten fans',created_by=self.user, topic=self.topic)
		self.url=reverse('reply_topic', kwargs={'board_id':self.board.id,'topic_id':self.topic.id})
		

class ReplyPostView(ReplyPostViewTestCase):
	def setUp(self):
		super().setUp()
		User.objects.create_user(username='cannonbolt',email='benten@gmail.com',password='itsherotime')
		self.client.login(username='cannonbolt',password='itsherotime')
		
		self.response=self.client.post(self.url, {'message':'hi'})

	def test_redirection(self):
		url=reverse('topic_posts', kwargs={'board_id':self.board.id, 'topic_id':self.topic.id})
		topic_post_url='{url}?page=1#2'.format(url=url)
		self.assertRedirects(self.response,topic_post_url)
		

