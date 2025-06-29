from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField  # добавлено

class Blog(models.Model):
    text = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.text
    

class Post(models.Model):
    topic = models.CharField(max_length=100)
    text = models.TextField()
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    # заменяем ImageField → CloudinaryField
    image = CloudinaryField('image', blank=True, null=True)

    def __str__(self):
        return self.text
    

class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username}:{self.text[:50]}"
