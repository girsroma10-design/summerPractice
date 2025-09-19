from django import forms
from .models import Post, Comment, Profile, Settings, Category
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'image', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Введите заголовок поста')
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': _('Напишите содержание поста здесь...')
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        labels = {
            'is_published': _('Опубликовать сразу')
        }
        help_texts = {
            'image': _('Рекомендуемый размер: 1200x600px')
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 5:
            raise ValidationError(_('Заголовок слишком короткий (минимум 5 символов)'))
        return title


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': _('Оставьте ваш комментарий...')
            })
        }
        labels = {
            'text': ''
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'website', 'avatar']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': _('Расскажите о себе...')
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
        help_texts = {
            'avatar': _('Изображение будет обрезано до квадрата 200x200px')
        }


class SettingsForm(forms.ModelForm):
    THEME_CHOICES = [
        ('light', _('Светлая')),
        ('dark', _('Тёмная')),
        ('system', _('Как в системе'))
    ]

    theme = forms.ChoiceField(
        choices=THEME_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input'
        }),
        label=_('Цветовая тема')
    )

    notifications_enabled = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label=_('Получать уведомления'),
        help_text=_('Электронные уведомления о новых комментариях')
    )

    class Meta:
        model = Settings
        fields = ['theme', 'notifications_enabled']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'name': _('Категория'),
            'description': _('Описание'),
        }

