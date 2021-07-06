from django.shortcuts				import render, get_object_or_404, redirect
from django.http 					import Http404
from boards.models					import Board,Topic,Post
from django.contrib.auth.models 	import User
from boards.forms 					import NewTopicForm, PostForm
from django.contrib.auth.decorators import login_required
from django.db.models 				import Count
from django.views.generic 			import UpdateView,ListView
from django.utils 					import timezone
from django.utils.decorators 		import method_decorator
from django.core.paginator 			import Paginator
from django.urls					import reverse


class BoardListView(ListView):
	model=Board
	context_object_name='boards'
	template_name='home.html'


class TopicListView(ListView):
	model=Topic
	context_object_name='topics'
	template_name='topics.html'
	paginate_by=20

	def get_context_data(self,**kwargs):
		kwargs['board']=self.board
		return super().get_context_data(**kwargs)

	def get_queryset(self):
		self.board=get_object_or_404(Board, id=self.kwargs.get('board_id'))
		queryset= self.board.topics.order_by('-last_updated').annotate(replies=Count('posts')-1)
		return queryset

'''
 old fbv
def topic_posts(request, board_id, topic_id):
	topic=get_object_or_404(Topic, board_id=board_id, id=topic_id)
	topic.views += 1
	topic.save()
	return render(request, 'topic_posts.html', {'topic':topic})
	'''

class PostListView(ListView):
	model=Post
	context_object_name='posts'
	template_name='topic_posts.html'
	paginate_by=20


	def get_context_data(self, **kwargs):
		session_key='view_topic_{}'.format(self.topic.id)
		if not self.request.session.get(session_key,False):
			self.topic.views +=1
			self.topic.save()
			self.request.session[session_key]=True

		kwargs['topic']=self.topic
		return super().get_context_data(**kwargs)

	def get_queryset(self):
		self.topic = get_object_or_404(Topic, board_id=self.kwargs.get('board_id'), id=self.kwargs.get('topic_id'))
		queryset = self.topic.posts.order_by('created_at')
		return queryset


@login_required
def new_topic(request,board_id):
	board=get_object_or_404(Board,id=board_id)

	if request.method=='POST':
		form=NewTopicForm(request.POST)
		if form.is_valid():
			topic=form.save(commit=False)
			topic.board=board
			topic.starter=request.user
			topic.save()

			post=Post.objects.create(
					message=form.cleaned_data.get('message'),
					topic=topic,
					created_by=request.user
					)

			return redirect('topic_posts', board_id=board_id, topic_id=topic.id)
	else: 
		form=NewTopicForm()

	return render(request,'new_topic.html',{'board':board, 'form':form})


@login_required
def reply_topic(request, board_id, topic_id):
	topic=get_object_or_404(Topic, board_id=board_id, id=topic_id)
	if request.method=="POST":
		form=PostForm(request.POST)
		if form.is_valid():
			post=form.save(commit=False)
			post.topic=topic
			post.created_by=request.user
			post.save()

			topic_url=reverse('topic_posts', kwargs={'board_id':board_id, 'topic_id':topic_id})
			topic_post_url='{url}?page={page}#{id}'.format(url=topic_url,page=topic.get_page_count(),id=post.id)
			return redirect(topic_post_url)
	else:
		form=PostForm()


	return render(request,'reply_topic.html',{'topic':topic,'form':form})


@method_decorator(login_required,name="dispatch")
class PostUpdateView(UpdateView):
	model=Post
	fields=('message',)
	template_name='edit_post.html'
	pk_url_kwarg='post_id'
	context_object_name='post'
	

	def get_queryset(self):
		queryset=super().get_queryset()
		return queryset.filter(created_by=self.request.user)

	def form_valid(self, form):
		post=form.save(commit=False)
		post.created_by=self.request.user
		post.created_at=timezone.now()
		post.save()
		return redirect('topic_posts', board_id=post.topic.board.id, topic_id=post.topic.id)


