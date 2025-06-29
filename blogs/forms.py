from django import forms
from .models import Blog, Post, Comment

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['text']
        labels = {'text': ''}
        widgets = {
            'text': forms.TextInput(attrs={
                'placeholder': 'Enter blog title...',
                'class': 'form-control'
            })
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'image']  # Исправлено: content → text
        labels = {'text': '', 'image': 'Upload Image:'}
        widgets = {
            'text': forms.Textarea(attrs={
                'cols': 80,
                'rows': 10,
                'placeholder': 'Write your post content...',
                'class': 'form-control'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            })
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {'text': ''}
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Add your comment...',
                'class': 'form-control'
            })
        }