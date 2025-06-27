from django.db import models

from django.contrib.auth.models import User

class Blog(models.Model):
    text = models.CharField(max_length=200)
    #описание блога
    author = models.CharField(max_length=100)
    #АВТОР БЛОГА
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.text
    

class Post(models.Model):
    topic = models.CharField(max_length=100)
    #тема поста
    text = models.TextField()
    #само сообщение
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    #автор поста
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
    

class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.author.username}:{self.text[:50]}"

# Create your models here.
