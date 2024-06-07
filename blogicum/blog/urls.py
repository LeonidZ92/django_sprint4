from django.urls import include, path

from . import views

app_name = 'blog'

posts_urls = [
    path('<int:post_id>/',
         views.PostDetailView.as_view(),
         name='post_detail'),
    path('create/',
         views.PostCreateView.as_view(),
         name='create_post'),
    path('<int:post_id>/edit/',
         views.PostUpdateView.as_view(),
         name='edit_post'),
    path('<int:post_id>/delete/',
         views.PostDeleteView.as_view(),
         name='delete_post'),
    path('<int:post_id>/comment/',
         views.add_comment,
         name='add_comment'),
    path('<int:post_id>/edit_comment/<int:comment_id>/',
         views.CommentUpdateView.as_view(),
         name='edit_comment'),
    path('<int:post_id>/delete_comment/<int:comment_id>/',
         views.CommentDeleteView.as_view(),
         name='delete_comment'),
]

urlpatterns = [
    path('category/<slug:category_slug>/',
         views.CategoryListView.as_view(),
         name='category_posts'),
    path('profile/<str:username>/',
         views.get_profile,
         name='profile'),
    path('edit_profile/',
         views.edit_profile,
         name='edit_profile'),
    path('',
         views.BlogListView.as_view(),
         name='index'),
    path('posts/', include(posts_urls)),
]
