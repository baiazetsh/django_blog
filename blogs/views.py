from django.shortcuts import render, redirect, get_object_or_404

from . models import Blog, Post, Comment, PostView
from . forms import BlogForm, PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.contrib import messages


def index(request):
    blogs = Blog.objects.order_by('-date_added')[:6]
    #posts = Post.objects.order_by('date_added')
    context = {'blogs': blogs}    
    return render(request, 'blogs/index.html', context)


    


def blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    
    posts = blog.post_set.order_by('date_added')
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
            messages.success(request, "blog has been successfully added!")

            return redirect('blogs:index')
    context = {'form': form}
    return render(request, 'blogs/new_blog.html', context)

@login_required
def new_post(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)

    

    if request.method != 'POST':
        form = PostForm()
    else:
        form = PostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.blog = blog
            new_post.save()
            messages.success(request, "new post has been successfully added!")
            return redirect('blogs:blog', blog_id=blog.id)
    context = {'blog': blog, 'form': form}
    return render(request, 'blogs/new_post.html', context)

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    blog = post.blog
    
    # Проверка прав прямо здесь
    if blog.owner != request.user:
        messages.error(request, "You can't edit this post")
        return redirect('blogs:blog', blog_id=blog.id)

    if request.method != 'POST':
        form = PostForm(instance=post)
    else:
        form = PostForm(instance=post, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "The post has been successfully edited!")
            return redirect('blogs:blog', blog_id=blog.id)    
    context = {'post': post, 'blog': blog, 'form': form}
    return render(request, 'blogs/edit_post.html', context)

def bloges(request):
    blogs = Blog.objects.all()
    context = {'blogs': blogs}
    return render(request, 'blogs/bloges.html', context)




@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST': #Залогиненный комментирует
        form = CommentForm(data=request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
            messages.success(request, "comment has been successfully added!")
            return redirect('blogs:post_detail', post_id=post.id)           
    return redirect('blogs:post_detail',post_id=post.id)


    




def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    # Умная логика подсчета просмотров
    if request.user.is_authenticated:
        # Для авторизованных пользователей
        view, created = PostView.objects.get_or_create(
            post=post,
            user=request.user,
            defaults={
                'ip_address': request.META.get('REMOTE_ADDR'),
                'session_key': request.session.session_key
            }
        )
    else:
        # Для анонимных пользователей (по session_key)
        if not request.session.session_key:
            request.session.create()
        
        view, created = PostView.objects.get_or_create(
            post=post,
            session_key=request.session.session_key,
            user=None,
            defaults={
                'ip_address': request.META.get('REMOTE_ADDR')
            }
        )
    
    # Обновляем кэшированный счетчик если это новый просмотр
    if created:
        post.update_views_count()
    
    comments = post.comments.order_by('created_at')   
    form = CommentForm() if request.user.is_authenticated else None        
    context = {'post': post, 'comments': comments, 'form': form}
    return render(request, 'blogs/post_detail.html', context)




         












