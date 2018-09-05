from django.urls import path
from . import views


urlpatterns = [
    path('<int:blog_pk>', views.blog_detail, name='blog_detail'),
    path('type/<int:blog_in_type>', views.blogs_in_type, name='blogs_in_type'),
]