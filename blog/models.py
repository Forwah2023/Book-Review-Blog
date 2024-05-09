import uuid
from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator


class Post(models.Model):
	id = models.UUIDField(
	primary_key=True,
	default=uuid.uuid4,
	editable=False)
	title = models.CharField(max_length=200)
	genre= models.CharField(max_length=2,choices=[
	("SF", "Science-Fiction"),("NF", "Non-Fiction"),("TH", "Thriller and Action"),("HO", "Horror"),("RO", "Romance"),("CO", "Comedy"),("OT", "Other")
	,("FE", "Featured")
	])
	author = models.ForeignKey(
	get_user_model(),
	on_delete=models.CASCADE,
	)
	body = models.TextField()
	summary=models.CharField(max_length=300)
	date = models.DateTimeField(auto_now_add=True)
	rating=models.PositiveIntegerField(null=True,blank=True,default=1,validators=[MinValueValidator(1), MaxValueValidator(5)])
	affiliate_link = models.URLField(verbose_name='Affiliate Link', help_text='Enter the URL of the affiliate link for this product',null=True,blank=True)
	cover = models.ImageField(upload_to='covers/',null=True,blank=True)
	
	class Meta:
		permissions = [
		('is_blogger', 'Can create, read, update, and their posts'),
		]
	def __str__(self):
		return self.title
		
	def get_absolute_url(self):
		return reverse('post_detail', args=[str(self.id)])



class Bookmark(models.Model):
	user = models.ForeignKey(
	get_user_model(),
	on_delete=models.CASCADE,
	)
	post = models.ForeignKey(
	Post,
	on_delete=models.CASCADE,
	related_name='bookmarks',)
	created = models.DateTimeField(auto_now_add=True)

class Subscriber(models.Model):
	email = models.EmailField(unique=True)
	name = models.CharField(max_length=100)
	
	def __str__(self):
		return self.email
	def get_absolute_url(self):
		return reverse('home')