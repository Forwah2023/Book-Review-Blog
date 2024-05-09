from django.test import TestCase,SimpleTestCase
from django.contrib.auth import get_user_model
from django.urls import reverse, resolve
from .models import Post
from django.contrib.auth.models import Permission

from .views import BlogListView,BlogDetailView,AboutView,PrivacyView,SubscribeView,BlogGenreListView,AllGenreView
from .forms import SubscriberForm


class BlogTests(TestCase):
	def setUp(self):
		self.user = get_user_model().objects.create_user(
		username='testuser',
		email='test@email.com',
		password='secret'
		)
		self.blogger_permission = Permission.objects.get(codename='is_blogger')
		self.post = Post.objects.create(
		title='A good title',
		body='Nice body content',
		author=self.user,
		genre="NF",
		summary='a test summary',
		)
		self.post_url='/post/'+str(self.post.pk)+'/'

	def test_get_absolute_url(self):
		self.assertEqual(self.post.get_absolute_url(), self.post_url) 
		
	def test_string_representation(self):
		self.assertEqual(str(self.post), self.post.title)

	def test_post_content(self):
		self.assertEqual(f'{self.post.title}', 'A good title')
		self.assertEqual(f'{self.post.author}', 'testuser')
		self.assertEqual(f'{self.post.body}', 'Nice body content')
		self.assertEqual(f'{self.post.genre}', 'NF')
		self.assertEqual(f'{self.post.summary}','a test summary')
		
	def test_post_list_view(self):
		response = self.client.get(reverse('home'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'a test summary')
		self.assertNotContains(response, 'Hi there! I should not be on the page.')
		self.assertTemplateUsed(response, 'home.html')
		view = resolve('/')
		self.assertEqual(view.func.__name__,BlogListView.as_view().__name__)

	def test_post_detail_view(self):
		response = self.client.get(self.post_url)
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'A good title')
		self.assertNotContains(response, 'Hi there! I should not be on the page.')
		self.assertTemplateUsed(response, 'post_detail.html')
		response_4_0_4= self.client.get('/post/100000/')		
		self.assertEqual(response_4_0_4.status_code, 404)
		view = resolve(self.post_url)
		self.assertEqual(view.func.__name__,BlogDetailView.as_view().__name__)
		
	def test_genre_view(self):
		response_NF_genre = self.client.get('/genre/NF/')
		response_all_genre = self.client.get('/genre/')
		self.assertEqual(response_NF_genre.status_code, 200)
		self.assertEqual(response_all_genre.status_code, 200)
		self.assertContains(response_NF_genre, 'A good title')
		self.assertNotContains(response_NF_genre, 'Hi there! I should not be on the page.')
		self.assertTemplateUsed(response_NF_genre, 'genre_detail.html')
		view = resolve('/genre/NF/')
		self.assertEqual(view.func.__name__,BlogGenreListView.as_view().__name__)
		view = resolve('/genre/')
		self.assertEqual(view.func.__name__,AllGenreView.as_view().__name__)
		
	def test_create_post_for_logged_out_user(self): 
		response = self.client.post(reverse('post_new'), {
		'title': 'New title',
		'body': 'New text',
		'author': self.user,
		'genre': "NF",
		'summary': 'a test summary',
		})
		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, '%s?next=/post/new/' % (reverse('account_login')))
		response = self.client.get('%s?next=/post/new/' % (reverse('account_login')))
		self.assertContains(response, 'Log In')
		
		# tests for logged in users
	def test_list_view_for_logged_in_user(self):
		self.client.login(username='testuser', password='secret')
		response = self.client.get(reverse('home'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'testuser')
		self.assertNotContains(response, 'Hi there! I should not be on the page.')
		self.assertTemplateUsed(response, 'home.html')
		self.client.logout()

        # tests for logged in bloggers 
		
	def test_CRUD_for_logged_in_user_without_permission(self):
		'''Checking if non-bloggers cannot create, edited, and delete posts but can view posts'''
		self.client.login(username='testuser', password='secret')
		response_create = self.client.post(reverse('post_new'), {
		'title': 'New title',
		'body': 'New text',
		'author': self.user,
		'genre': "NF",
		'summary': 'a test summary',
		})
		
		response_edit = self.client.post(reverse('post_edit', args=[str(self.post.pk)]), {
		'title': 'Updated title',
		'body': 'Updated text',
		'summary': 'a test summary',
		'rating': 5
		})
		response_delete = self.client.get(reverse('post_delete', args=[str(self.post.pk)]))
		response_detail = self.client.get(self.post_url)
		self.assertEqual(response_create.status_code, 403) #forbidden
		self.assertEqual(response_edit.status_code,403)
		self.assertEqual(response_delete.status_code,403)
		# check that post detail does not contain edit and delete links.
		self.assertEqual(response_detail.status_code,200)
		self.assertTemplateUsed(response_detail, 'post_detail.html')
		self.assertContains(response_detail, 'A good title')
		self.assertNotContains(response_detail, '+ Edit Post')
		self.assertNotContains(response_detail, '- Delete Blog Post')
		self.client.logout()

	def test_CRUD__for_users_with_permissions(self): 
		self.client.login(username='testuser', password='secret')
		self.user.user_permissions.add(self.blogger_permission)
		response_create = self.client.post(reverse('post_new'), {
		'title': 'New title',
		'body': 'New text',
		'author': self.user,
		'genre': "NF",
		'summary': 'a test summary',
		})
		
		response_edit = self.client.post(reverse('post_edit', args=[str(self.post.pk)]), {
		'title': 'Updated title',
		'body': 'Updated text',
		'summary': 'a test summary',
		'rating': 5
		})
		
		response_delete = self.client.get(reverse('post_delete', args=[str(self.post.pk)]))
		response_detail = self.client.get(self.post_url)
		response_home = self.client.get(reverse('home'))
		
		self.assertEqual(response_create.status_code,302)
		self.assertEqual(response_edit.status_code,302)
		self.assertEqual(response_delete.status_code, 200)
		self.assertContains(response_delete, 'Are you sure you want to delete')
		self.assertTemplateUsed(response_delete, 'post_delete.html')
		self.assertContains(response_detail, '+ Edit Post')
		self.assertContains(response_detail, '- Delete Blog Post')
		self.assertTemplateUsed(response_detail, 'post_detail.html')
		self.assertContains(response_home, 'New Post')
		self.assertTemplateUsed(response_home, 'home.html')	
		self.client.logout()
			

class SubscribePageTests(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse('subscribe'))

    def test_subscribe_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'subscribe.html')
        self.assertContains(self.response, 'Subscribe to our Newsletter!')
        self.assertNotContains(self.response, 'Hi there! I should not be on the page.')
    
    def test_subscribe_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SubscriberForm)
        self.assertContains(self.response, 'csrfmiddlewaretoken')
    
    def test_subscribe_view(self): 
        view = resolve('/subscribe/')
        self.assertEqual(view.func.__name__,SubscribeView.as_view().__name__)



class AboutMeTests(SimpleTestCase): 
	def setUp(self):
		self.response = self.client.get(reverse('about')  )
		
	def test_aboutpage_status_code(self):
		self.assertEqual(self.response.status_code, 200)
		
	def test_aboutpage_template(self):
		self.assertTemplateUsed(self.response, 'aboutMe.html')
		
	def test_aboutpage_contains_correct_html(self):
		self.assertContains(self.response, 'About Me')
		
	def test_aboutpage_does_not_contain_incorrect_html(self):
		self.assertNotContains(self.response, 'I should not be on the page.')
		
	def test_aboutpage_url_resolves_aboutpageview(self):
		view = resolve('/about/')
		self.assertEqual(view.func.__name__,AboutView.as_view().__name__)
		

class PrivacyStatementTests(SimpleTestCase): 
	def setUp(self):
		self.response = self.client.get(reverse('privacy')  )
		
	def test_privacy_statement_status_code(self):
		self.assertEqual(self.response.status_code, 200)
		
	def test_privacy_statement_template(self):
		self.assertTemplateUsed(self.response, 'privacy_statement.html')
		
	def test_privacy_statement_contains_correct_html(self):
		self.assertContains(self.response, 'Privacy Policy for strongbookreviews.com')
		
	def test_privacyStatement_does_not_contain_incorrect_html(self):
		self.assertNotContains(self.response, 'I should not be on the page.')
		
	def test_privacy_url_resolves_privacyview(self):
		view = resolve('/privacy/')
		self.assertEqual(view.func.__name__,PrivacyView.as_view().__name__)