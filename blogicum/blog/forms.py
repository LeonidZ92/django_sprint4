from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Comment, Post, User


class NewUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username',)


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ('author',)
        widgets = {
            'pub_date': forms.DateTimeInput(
                format='%d/%m/%Y %H:%M',
                attrs={'type': 'datetime-local'},
            )
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs['rows'] = 3
