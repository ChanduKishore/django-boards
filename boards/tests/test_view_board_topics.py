from django.urls import reverse, resolve
from django.test import TestCase
from boards.views import TopicListView
from boards.models import Board,Topic,Post

class BoardTopicTests(TestCase):
	def setUp(self):
		self.board=Board.objects.create(name='Flask',description='Flask board')
		url=reverse('home')
		self.response=self.client.get(url)
		

	def test_board_topic_view_sucess_staus_code(self):
		url=reverse('board_topics', kwargs={'board_id':1})
		response=self.client.get(url)
		self.assertEquals(response.status_code,200) 

	def test_board_topic_view_status_code_not_found(self):
		url=reverse('board_topics',kwargs={'board_id':99})
		response=self.client.get(url)
		self.assertEquals(response.status_code,404)

	def test_home_page_contain_bpard_topics_url(self):
		board_topics_url= reverse('board_topics',kwargs={'board_id':self.board.id})
		self.assertContains(self.response,'href="{0}"'.format(board_topics_url))

	def test_board_topics_contain_homepage_url(self):
		board_topics_url=reverse('board_topics',kwargs={'board_id':1})
		response=self.client.get(board_topics_url)
		homepage_url=reverse('home')
		new_topic_url=reverse('new_topic',kwargs={'board_id':1})

		self.assertContains(response,'href="{0}"'.format(homepage_url))
		self.assertContains(response,'href="{0}"'.format(new_topic_url))

