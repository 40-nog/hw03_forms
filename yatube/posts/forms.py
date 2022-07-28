from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    text = forms.CharField(
        widget=forms.Textarea,
        label='Напишите что-нибудь',
        required=True,
        help_text='Ваше сочинение',
    )

    class Meta:
        model = Post
        fields = ('group', 'text')
        labels = {'group': 'Выберите подходящую группу'}
        help_texts = {'group': 'Группа'}
