from django.shortcuts import render, redirect, get_object_or_404

from . models import Blog, Post, Comment
from . forms import BlogForm, PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.http import Http404

def index(request):
    blogs = Blog.objects.order_by('-date_added')[:6]
    #posts = Post.objects.order_by('date_added')
    context = {'blogs': blogs}    
    return render(request, 'blogs/index.html', context)

def check_blog_owner(request, blog):
    #  функция проверка принадлкжности контента юзер
    print(f"Current user: {request.user}")
    print(f"blog's owner:{blog.owner}")
    if blog.owner != request.user:
        raise Http404

@login_required
def blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    #check_blog_owner(request, blog)
    posts = blog.post_set.order_by('-date_added')
    #blogs = Blog.objects.filter(owner=request.user).order_by('date_added')
    context = {'blog': blog, 'posts': posts}
    return render(request, 'blogs/blog.html', context)

@login_required
def new_blog(request):
    if request.method != 'POST':
        form = BlogForm()
    else:
        form = BlogForm(data=request.POST)
        if form.is_valid():
            new_blog = form.save(commit=False)
            new_blog.owner = request.user
            new_blog.save()

            return redirect('blogs:index')
    context = {'form': form}
    return render(request, 'blogs/new_blog.html', context)

@login_required
def new_post(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    #check_blog_owner(request, blog)
    

    if request.method != 'POST':
        form = PostForm()
    else:
        form = PostForm(data=request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.blog = blog
            new_post.save()
            return redirect('blogs:blog', blog_id=blog.id)
    context = {'blog': blog, 'form': form}
    return render(request, 'blogs/new_post.html', context)

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    blog = post.blog
    check_blog_owner(request, blog)

    if request.method != 'POST':
        form = PostForm(instance=post)
    else:
        form = PostForm(instance=post, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('blogs:blog', blog_id=blog.id)    
    context = {'post': post, 'blog': blog, 'form': form}
    return render(request, 'blogs/edit_post.html', context)

@login_required
def bloges(request):
    blogs = Blog.objects.all()
    context = {'blogs': blogs}
    return render(request, 'blogs/bloges.html', context)

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.order_by('-created_at')
    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
            return redirect('blogs:post_detail', post_id=post.id)
    else:
        form = CommentForm()
    context = {'post': post, 'comments': comments, 'form': form}
    return render(request, 'blogs/post_detail.html', context)

    








         












