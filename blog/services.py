from django.core.cache import cache

from blog.models import Blog


def get_blog_cache():
    key = 'client_list'
    blog_list = cache.get(key)
    if blog_list is None:
        blog_list = Blog.objects.all()
        cache.set(key, blog_list)
    return blog_list
