from django import forms
from django_summernote.widgets import SummernoteWidget

from .models import Post, Images, Comment

class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].widget.attrs['class']='form-control'
        self.fields['text'].label = 'Body of post'
        self.fields['title'].widget.attrs['class']='form-control' # adds bootstrap form-control class

    class Meta:
        model = Post
        fields = ('author', 'title', 'text',)
        widgets = {
        'text': SummernoteWidget(),
        }

class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')    
    class Meta:
        model = Images
        fields = ('image',)


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].widget.attrs['class']='form-control'
        self.fields['text'].widget.attrs['class']='form-control'
        self.fields['text'].widget.attrs['rows']='3'
        self.fields['text'].label = 'Comment'

    class Meta:
        model = Comment
        fields = ('author', 'text',)
