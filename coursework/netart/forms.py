from django import forms
from .models import *


class ProfileEditForm(forms.Form):
    first_name = forms.CharField(label='First name:', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'John'
    }
    )
    )
    last_name = forms.CharField(label='Last name:', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Smith'
    }
    )
    )
    city = forms.CharField(label='City:', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Kyiv'
    }
    )
    )
    birthdate = forms.DateField(label='Birth date:', widget=forms.SelectDateWidget(
                                     empty_label=('Year:', 'Month:', 'Day:'), years=range(1900, 2000),
        attrs={'class': 'form-control'}
    )
    )
    role = forms.ChoiceField(label='Are you an artist?', choices=(('artist', 'Yes'), ('user', 'No')),
                             widget=forms.Select(attrs={'class': 'form-control'}))


class ChangeAvatarForm(forms.Form):
    image = forms.ImageField(label="Choose avatar:", widget=forms.ClearableFileInput(
        attrs={'class': 'form-control-file'}))


class PictureUploadForm(forms.Form):
    title = forms.CharField(label='Title:', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Just name it...'
    }))
    theme = forms.ChoiceField(label='Theme:', choices=(('nature', 'Nature'), ('people', 'People'),
                                                       ('sketch', 'Sketch'), ('animals', 'Animals')),
                              widget=forms.Select(attrs={'class': 'form-control'}))
    style = forms.CharField(label='Style:', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Some stylish...'
    }))
    image = forms.ImageField(label="Upload image:", widget=forms.ClearableFileInput(attrs=
                                                                                    {'class': 'form-control-file'}))


class SendMessageForm(forms.Form):
    receiver = forms.CharField(label='To:', widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    msg_content = forms.CharField(label='Message:', widget=forms.Textarea(attrs={
        'class': 'form-control'
    }))


class AddNewsForm(forms.Form):
    title = forms.CharField(label='Title:', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Title...'
    }))
    text = forms.CharField(label='Text:', widget=forms.Textarea(attrs={'class': 'form-control'}))
    expodate = forms.DateField(label='Exhibition date:', widget=forms.SelectDateWidget(
        empty_label=('Year:', 'Month:', 'Day:'), attrs={'class': 'form-control'}
    ))
    expotheme = forms.CharField(label='Exhibition theme:', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Theme...'
    }))
    image = forms.ImageField(label='Picture:', widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))