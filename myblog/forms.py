from django.forms import ModelForm
from .models import Post, Comment, Tag
from django.utils.translation import ugettext_lazy as _
from django.forms import widgets

class PostForm(ModelForm):
    class Meta:
        model=Post
        fields=['title','image','content','is_published']
        widgets = {
            'content': widgets.Textarea(attrs={'rows': 15, 'class':'col-lg-12'}),
            'title':widgets.TextInput({'class':'col-lg-12'}),
            'image':widgets.FileInput({'class':'col-lg-12'}),
        }
        labels = {
            'name': _('Writer'),
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