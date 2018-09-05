from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator  # 引入分页器
from Blog.models import Blog, BlogType


def blog_list(request):

    # 获得显示的数据页码，如果不存在默认为1
    page_num = request.GET.get('page', 1)

    # 使用分页器获得数据对象的分页
    blog = Blog.objects.all()
    paginator = Paginator(blog, 10)
    page_of_blog = paginator.page(page_num)

    # 将要传输的数据存入到上下文
    context = dict()
    context['page_of_blog'] = page_of_blog
    context['blog_types'] = BlogType.objects.all()
    return render(request, 'Blog/blog_list.html', context)


def blog_detail(request, blog_pk):

    # 获得参数blog_pk，用于获得对应的博客数据，将数据存入到上下文
    context = dict()
    print(blog_pk)
    context['blog'] = get_object_or_404(Blog, pk=blog_pk)
    return render(request, 'Blog/blog_detail.html', context)


def blogs_in_type(request, blog_in_type):

    # 获得显示的数据页码，如果不存在默认为1
    page_num = request.GET.get('page', 1)

    # 获得传入的博客类型对应的pk对象，从博客中获得类型与该对象相同的对象，存入上下文
    blog_type = get_object_or_404(BlogType, pk=blog_in_type)

    # 使用分页器获得数据对象的分页
    blog = Blog.objects.filter(blog_type=blog_type)
    paginator = Paginator(blog, 10)
    page_of_blog = paginator.page(page_num)

    # 将数据存入上下文
    context = dict()
    context['page_of_blog'] = page_of_blog
    context['blog_type'] = blog_type
    context['blog_types'] = BlogType.objects.all()
    return render(request, 'Blog/blogs_in_type.html', context)
