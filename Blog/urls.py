from django.urls import path
from . import views


urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('<int:blog_pk>', views.blog_detail, name='blog_detail'),
    path('type/<int:blog_in_type>', views.blogs_in_type, name='blogs_in_type'),
    path('date/<int:blog_in_year>&<int:blog_in_month>', views.blog_in_date, name='blog_in_date'),
]
