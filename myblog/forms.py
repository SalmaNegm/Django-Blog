from django.forms import ModelForm
from .models import Post, Comment, Tag
from django.utils.translation import ugettext_lazy as _
from django.forms import widgets
from django.contrib.auth.models import User

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
        labels = {
            'first_name': _(''),
            'last_name': _(''),
            'username': _(''),
            'password': _(''),
            'email': _(''),
        }





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