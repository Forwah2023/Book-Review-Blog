from django.shortcuts import render
from django.contrib.auth.mixins import (LoginRequiredMixin,PermissionRequiredMixin)
from django.core.exceptions import PermissionDenied
from django.views.generic import TemplateView,ListView,DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .forms import SubscriberForm
from django.db.models import Q

from .models import Post,Bookmark
# Create your views here.

#CRUD viewa
class BlogListView(ListView):
	model = Post
	template_name = 'home.html'
	context_object_name = 'all_posts_list'
	paginate_by = 10
	
	def get_queryset(self):
		qs = super().get_queryset()
		qs = qs.order_by('-date')
		return qs
	def get_context_data(self, **kwargs):
		data = super().get_context_data(**kwargs)
		featured=super().get_queryset().order_by('-date').filter(genre='FE')
		if featured:
			#index 0 selects the most recent article
			data['featured']=featured[0]
			data['featured_id']=featured[0].pk
		else:
			data['featured']=None
		return data


class BlogDetailView(DetailView): 
	model = Post
	template_name = 'post_detail.html'	
	context_object_name = 'indiv_post'

	def get_context_data(self, **kwargs):
		data = super().get_context_data(**kwargs)
		qs = Post.objects.all()
		qs=qs.order_by('-date')
		cur_obj=qs.get(pk=self.kwargs['pk'])
		# select three recent related reviews
		qs=qs.filter(genre=cur_obj.genre)[:4] 
		data['recent_related']=qs
		# prepare bookmark data
		data['user_bookmarked_this'] =cur_obj.bookmarks.filter(user=self.request.user.id,post=cur_obj).exists()
		return data
		
	def post(self, request, *args, **kwargs):
		if request.accepts("application/json"):
			# Handle AJAX 
			if request.POST.get("operation") == 'bookmark_update':
				post_pk=request.POST.get('post_pk', None)
				curr_post=get_object_or_404(Post,pk=post_pk)
				new_bookmark, created = Bookmark.objects.get_or_create(user=request.user, post=curr_post)
				if not created:
					Bookmark.objects.get(user=request.user, post=curr_post).delete()
					bookmarked=False
				else:
					bookmarked=True
				data={'bookmarked':bookmarked,'post_pk':post_pk}
				return JsonResponse(data)
		else:
		# Proceed with regular view logic
			return super().post(request, *args, **kwargs)

class BlogCreateView(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
	model = Post
	template_name = 'post_new.html'
	#fields = '__all__'
	fields = ('title','genre', 'body','summary','rating','affiliate_link')
	permission_required = 'blog.is_blogger'
	# matches created form to current user
	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)
	
class BlogUpdateView(LoginRequiredMixin,PermissionRequiredMixin,UpdateView): 
	model = Post
	template_name = 'post_edit.html'
	fields =['title', 'body','summary','rating','affiliate_link']#  '__all__'
	permission_required = 'blog.is_blogger'
	def dispatch(self, request, *args, **kwargs):
		obj = self.get_object()
		if obj.author != self.request.user:
			raise PermissionDenied
		return super().dispatch(request, *args, **kwargs)

class BlogDeleteView(LoginRequiredMixin,PermissionRequiredMixin,DeleteView): 
	model = Post
	template_name = 'post_delete.html'
	success_url = reverse_lazy('home')
	permission_required = 'blog.is_blogger'
	def dispatch(self, request, *args, **kwargs):
		obj = self.get_object()
		if obj.author != self.request.user:
			raise PermissionDenied
		return super().dispatch(request, *args, **kwargs)
	

class BookmarkListView(LoginRequiredMixin,ListView):
	paginate_by = 10
	template_name = 'bookmark_list.html'
	context_object_name = 'bookmark_list'
	def get_queryset(self):
		qs=Bookmark.objects.filter(user=self.request.user)
		return qs


class BlogGenreListView(ListView):
	model = Post
	template_name = 'genre_detail.html'
	context_object_name = 'genre_detail'
	paginate_by = 10
	
	def get_queryset(self):
		qs = super().get_queryset()
		qs = qs.order_by('-date')
		qs=qs.filter(genre=self.kwargs['gnr'])
		return qs
		
	def get_context_data(self, **kwargs):
		data = super().get_context_data(**kwargs)
		query=self.kwargs['gnr']
		data['sub_genre']=dict(Post._meta.get_field('genre').choices).get(query, "")   
		return data
	
class AllGenreView(TemplateView):
	template_name = 'All_genre.html'

#subscription views
	
class SubscribeView(CreateView):
	form_class = SubscriberForm
	success_url = reverse_lazy('thanks')
	template_name = 'subscribe.html'

class SubscribeThanksView(TemplateView):
	template_name = 'thanks.html'


# Search views
class SearchListView(ListView):
	model = Post
	template_name = 'search_results.html'
	context_object_name = 'search_query'
	paginate_by = 10
	def get_queryset(self):
		query = self.request.GET.get('q')
		return Post.objects.filter(Q(title__icontains=query) | Q(author__username__icontains=query) | Q(genre__icontains=query))

#About ME views

class AboutView(TemplateView):
	template_name = 'aboutMe.html'
	
class AccountInfoView(LoginRequiredMixin,TemplateView):
	template_name = 'account_detail.html'
	def get_context_data(self, **kwargs):
		data = super().get_context_data(**kwargs)
		data['num_created_posts']=len(Post.objects.filter(author=self.request.user))
		data['num_bookmarked_posts']=len(Bookmark.objects.filter(user=self.request.user))
		return data
	
class PrivacyView(TemplateView):
	template_name = 'privacy_statement.html'