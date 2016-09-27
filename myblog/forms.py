from django.forms import ModelForm
from .models import Post, Comment, Tag
from django.utils.translation import ugettext_lazy as _
from django.forms import widgets
from django.contrib.auth.models import User
from django import forms

class PostForm(ModelForm):
    class Meta:
        model=Post
        fields=['title','image','content','is_published']
        widgets = {
            'content': widgets.Textarea(attrs={'rows': 15, 'class':'col-lg-12 form-control'}),
            'title':widgets.TextInput({'class':'col-lg-12 form-control'}),
            'image':widgets.FileInput({'class':'col-lg-12 form-control'}),
        }
        # labels = {
        #     'name': _('Writer'),
        # }
    def clean_image(self):
        data=self.cleaned_data.get('image',False)
        try:
            if data:
                if (not data._size > 40*1024) or (not data._size < 1024*1024) :
                    raise forms.ValidationError('image size must be between 40Kb-1Mb.')

        except AttributeError:
            pass
        return data

class CommentForm(ModelForm):
    class Meta:
        model=Comment
        fields=['content','post']
        widgets = {
            'content': widgets.Textarea(attrs={'rows': 5, 'class':'col-lg-12','placeholder':'write comment ...'}),
            'post':widgets.HiddenInput(),
        }
        labels = {
            'content': _(''),
        }

class UserForm(ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password','email']
        widgets = {
            'first_name': widgets.TextInput(attrs={ 'class':'col-lg-12 form-control','placeholder':'First Name...'}),
            'last_name': widgets.TextInput(attrs={ 'class':'col-lg-12 form-control','placeholder':'Last Name...'}),
            'username': widgets.TextInput(attrs={ 'class':'col-lg-12 form-control','placeholder':'UserName...'}),
            'password': widgets.PasswordInput(attrs={ 'class':'col-lg-12 form-control','placeholder':'Password...'}),
            'email': widgets.EmailInput(attrs={ 'class':'col-lg-12 form-control','placeholder':'E-Mail...'}),
            # 'post':widgets.HiddenInput(),
        }
        # labels = {
        #     'first_name': _(''),
        #     'last_name': _(''),
        #     'username': _(''),
        #     'password': _(''),
        #     'email': _(''),
        # }
    def clean_first_name(self):
        first_name=self.cleaned_data.get('first_name','')
        if first_name =='':
            raise forms.ValidationError('first name is required.')
        if not first_name.isalpha():
            raise forms.ValidationError('first name must be alphabetic characters only')

        return first_name

    def clean_last_name(self):
        data=self.cleaned_data.get('last_name','')
        if data =='':
            raise forms.ValidationError('last name is required.')
        if not data.isalpha():
            raise forms.ValidationError('last name must be alphabetic characters only')
        return data

    def clean_email(self):
        data=self.cleaned_data.get('email','')
        if data =='':
            raise forms.ValidationError('email address is required.')
        return data


    # def __init__(self, *args, **kwargs):
    #     super(PostForm, self).__init__(*args, **kwargs)
    #     self.fields['title'].widget.attrs.update({
    #         'class': 'col-lg-12'
    #     })
    #     self.fields['image'].widget.attrs.update({
    #         'class': 'col-lg-12'
    #     })
    #     self.fields['content'].widget.attrs.update({
    #         'class': 'col-lg-12'
    #     })