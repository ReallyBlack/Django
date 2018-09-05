from django.shortcuts import render, get_object_or_404

from Blog.models import Blog, BlogType


def blog_list(request):
    context = dict()
    context['blogs'] = Blog.objects.all()
    return render(request, 'Blog/blog_list.html', context)


def blog_detail(request, blog_pk):
    context = dict()
    print(blog_pk)
    context['blog'] = get_object_or_404(Blog, pk=blog_pk)
    return render(request, 'Blog/blog_detail.html', context)


def blogs_in_type(request, blog_in_type):
    blog_type = get_object_or_404(BlogType, pk=blog_in_type)
    context = dict()
    context['blogs'] = Blog.objects.filter(blog_type=blog_type)
    context['blog_type'] = blog_type
    return render(request, 'Blog/blogs_in_type.html', context)
