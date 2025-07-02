from django.urls import path
from . import views

app_name = 'blogs'

urlpatterns = [
    path('', views.index, name='index'),
    path('new_blog/', views.new_blog, name='new_blog'),
    path('blogs/<int:blog_id>/new_post/', views.new_post, name='new_post'),
    path('posts/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('blogs/<int:blog_id>/', views.blog, name='blog'),
    path('bloges/', views.bloges, name='bloges'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
]
