from django.contrib import admin

# Register your models here.
from .models import Post,Subscriber,Bookmark

class BookmarkInline(admin.TabularInline):
	model = Bookmark

class PostAdmin(admin.ModelAdmin):
	inlines = [
		BookmarkInline,
		]
	list_display = ("title","author","rating",)

admin.site.register(Post,PostAdmin)
admin.site.register(Subscriber)
admin.site.register(Bookmark)