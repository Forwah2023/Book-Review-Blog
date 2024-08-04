from django.urls import path
from .views import BlogListView,BlogDetailView,BlogCreateView,BlogUpdateView,BlogDeleteView,AllGenreView,\
BlogGenreListView,SubscribeView,SubscribeThanksView,SearchListView,AboutView,PrivacyView,AccountInfoView,BookmarkListView,LikeListView


urlpatterns = [
path('', BlogListView.as_view(), name='home'),
path('post/<uuid:pk>/', BlogDetailView.as_view(), name='post_detail'),
path('post/new/', BlogCreateView.as_view(), name='post_new'),
path('post/<uuid:pk>/edit/',BlogUpdateView.as_view(), name='post_edit'),
path('post/<uuid:pk>/delete/', BlogDeleteView.as_view(), name='post_delete'),
path('genre/', AllGenreView.as_view(), name='All_genre'),
path('genre/<gnr>/', BlogGenreListView.as_view(), name='genre_detail'),
path('subscribe/', SubscribeView.as_view(), name='subscribe'),
path('subscribe/thanks/', SubscribeThanksView.as_view(), name='thanks'),
path('search/', SearchListView.as_view(), name='search_results'),
path('about/', AboutView.as_view(), name='about'),
path('privacy/', PrivacyView.as_view(), name='privacy'),
path('user/<current_user>/', AccountInfoView.as_view(), name='accountinfo'),
path('user/<current_user>/bookmarks', BookmarkListView.as_view(), name='bookmarks'),
path('user/<current_user>/likes', LikeListView.as_view(), name='likes'),


]