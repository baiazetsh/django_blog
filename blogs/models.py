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

    # Новое поле для счетчика просмотров
    views_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.text
    
    def get_views_count(self):
        """Получить актуальное количество просмотров"""
        return self.post_views.count()
        
    def update_views_count(self):
        """Обновить кэшированный счетчик"""
        self.views_count = self.get_views_count()
        self.save(update_fields=['views_count'])
    


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username}:{self.text[:50]}"
    
    
    
class PostView(models.Model):
        post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_views')
        user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
        session_key = models.CharField(max_length=50, null=True, blank=True)
        viewed_at = models.DateTimeField(auto_now_add=True)
        ip_address = models.GenericIPAddressField(null=True, blank=True)
    
        class Meta:
            unique_together = ['post', 'user', 'session_key']
        
        def __str__(self):
            if self.user:
                return f"{self.user.username} viewed {self.post.topic}"
            return f"Anonymous viewed {self.post.topic}"
    