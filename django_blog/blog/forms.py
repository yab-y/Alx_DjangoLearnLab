from django import forms
from .models import Post, Comment
from taggit.forms import TagWidget  # make sure this exact import is present

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']  # include tags
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Post Title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your post...'}),
            'tags': TagWidget(),  # <-- ensure TagWidget() is used exactly like this
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write a comment...'}),
        }
