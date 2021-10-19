from django import forms
from django.forms import ModelForm
from .models import Post

class NewPostForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewPostForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
        })
        
    content = forms.CharField(required=True, label='', max_length=280, widget=forms.Textarea(attrs={
                                'class': 'form-control',
                                'autofocus': 'autofocus',
                                'placeholder': 'Tell me something'
    }))

    class Meta:
        model = Post
        fields = ['content']
