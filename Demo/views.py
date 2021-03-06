from django.shortcuts import render
from Blog.models import Blog
from django.contrib.contenttypes.models import ContentType
from read_statistics.method_for_blog import get_a_week_read_date, get_hot_blog


def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_a_week_read_date(blog_content_type)
    today_hot_blog = get_hot_blog(blog_content_type)
    context = dict()
    context['read_nums'] = read_nums
    context['dates'] = dates
    context['today_hot_blog'] = today_hot_blog
    return render(request, 'home.html', context)
