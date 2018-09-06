from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator  # 引入分页器
from django.db.models import Count
from Blog.models import Blog, BlogType
from .method_for_blog import read_add_numm


# 对博客数据进行初步的处理
def get_blogs_info_code(request, blogs):
    # 获得显示的数据页码，如果不存在默认为1
    page_num = request.GET.get('page', 1)

    # 使用分页器获得数据对象的分页
    paginator = Paginator(blogs, 10)
    page_of_blog = paginator.page(page_num)

    # 日期归档博客数量
    blogs_date = Blog.objects.dates('create_time', 'month', order='DESC')
    blogs_date_dict = dict()
    for blogs_date in blogs_date:
        blogs_count = Blog.objects.filter(create_time__year=blogs_date.year,
                                          create_time__month=blogs_date.month).count()
        blogs_date_dict[blogs_date] = blogs_count

    # 将要传输的数据存入到上下文
    context = dict()
    context['blog_dates'] = blogs_date_dict  # 获得全部时间列表
    context['page_of_blog'] = page_of_blog  # 页面要获得的博客数据
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))  # 获取全部博客类型和数量
    return context


def blog_list(request):
    blogs = Blog.objects.all()
    # 博客数据预处理
    context = get_blogs_info_code(request, blogs)
    return render(request, 'Blog/blog_list.html', context)


def blog_detail(request, blog_pk):

    # 获得参数blog_pk，用于获得对应的博客数据，将数据存入到上下文
    context = dict()
    blog = get_object_or_404(Blog, pk=blog_pk)
    read_cookie_key = read_add_numm(request, blog)
    context['blog'] = blog
    context['previous_blog'] = Blog.objects.filter(create_time__gt=blog.create_time).last()
    context['next_blog'] = Blog.objects.filter(create_time__lt=blog.create_time).first()
    response = render(request, 'Blog/blog_detail.html', context)
    response.set_cookie(read_cookie_key, 'true')
    return response


def blogs_in_type(request, blog_in_type):
    # 获得传入的博客类型对应的pk对象，从博客中获得类型与该对象相同的对象，存入上下文
    blog_type = get_object_or_404(BlogType, pk=blog_in_type)
    # 博客数据预处理
    blog_in_type = Blog.objects.filter(blog_type=blog_type)
    context = get_blogs_info_code(request, blog_in_type)
    context['blog_type'] = blog_type
    return render(request, 'Blog/blogs_in_type.html', context)


def blog_in_date(request, blog_in_year, blog_in_month):
    # 获得传入的博客日期的参数，寻找对应的对象
    blogs_in_date = Blog.objects.filter(create_time__month=blog_in_month, create_time__year=blog_in_year)
    # 博客数据预处理
    context = get_blogs_info_code(request, blogs_in_date)
    context['blog_date'] = '%s年%s月' % (blog_in_year, blog_in_month)
    return render(request, 'Blog/blogs_in_date.html', context)
