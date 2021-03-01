from django.urls import path
from .views import *


# app_name = 'Post'
urlpatterns = [
    path('', posts_list, name='posts_list'),
    path('post_create/', post_create, name='post_create'),
    path('post/<int:pk>/', post_detail, name='post_detail'),
    path('post/update/<int:pk>/', EditPostView.as_view(), name='post_update'),
    path('post/delete/<int:pk>/', delete_post, name='post_delete'),
    path('comment/delete/<int:pk>/', comment_delete, name='comment_delete'),
    path('tags/', tags_list, name='tags_list'),
    path('tag/<str:slug>/', tag_detail, name='tag_detail'),
]