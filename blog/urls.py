from django.contrib.auth.decorators import login_required
from django.urls import path

from blog.apps import BlogConfig
from blog.views import BlogListView, BlogCreateView, BlogDetailView, BlogUpdateView, BlogDeleteView

app_name = BlogConfig.name

urlpatterns = [
    path('', BlogListView.as_view(), name='blog_list'),
    path('create_blog/', BlogCreateView.as_view(), name='blog_create'),
    path('blog/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
    path('update_blog/<int:pk>/', BlogUpdateView.as_view(), name='blog_update'),
    path('delete_blog/<int:pk>/', BlogDeleteView.as_view(), name='blog_delete')
]
