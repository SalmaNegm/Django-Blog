import datetime
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Post,Comment,Tag
from django.shortcuts import render
from django.shortcuts import render
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from .forms import PostForm, CommentForm, UserForm
from django.contrib.auth.models import User
from django.core import serializers
from django.contrib.auth.decorators import login_required
import json
from collections import Counter
from django.contrib.auth.hashers import make_password

def index(request):
    posts=Post.objects.filter(is_published=True).order_by('-pub_date')[:6]
    return render(request,'myblog/index.html',{'posts':posts})

def log_in(request):
    return render(request,'myblog/login.html')

def signin(request):
    if request.method == 'POST':
        user=authenticate(username=request.POST['username'],password=request.POST['password'])
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
                # return HttpResponse('wellcome')
            else:
                return render(request,'myblog/inactive.html')
        else:
            return render(request,'myblog/login.html',{'error':'incorrect username/password'})
    else:
        return HttpResponseRedirect(reverse('login'))

def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

# @login_required(login_url='/blog/login/')
def create_post(request):
    # if request.user.is_authenticated(): # uathentication
        if request.user.is_active:
            if request.method == 'POST':
                # return HttpResponse(request.POST['is_published'])
                form=PostForm(request.POST,request.FILES)
                if form.is_valid():
                    new_post=form.save(commit=False)
                    new_post.user_id=request.user.id
                    if request.POST.has_key('is_published'):
                        new_post.pub_date=datetime.datetime.now()
                    tags=[ tag.lower() for tag in request.POST['tags'].split(',')] #for case insensitive comparison
                    tags=list(set(tags)) #unique list
                    new_tags=[Tag(name=tag) for tag in tags if not Tag.objects.filter(name__iexact=tag).exists() ]
                    Tag.objects.bulk_create(new_tags)
                    new_post.save()
                    for tag in tags:
                        new_post.tag_set.add(Tag.objects.get(name=tag))
                    return HttpResponseRedirect(reverse('create_post'))
                else:
                    all_tags=json.dumps([unicode(i) for i in Tag.objects.values_list('name',flat=True)])
                    return render(request,'myblog/create-post.html',{'form':form,'tags':all_tags})

            form = PostForm(request.POST or None)

            all_tags=json.dumps([unicode(i) for i in Tag.objects.values_list('name',flat=True)])

            return render(request,'myblog/create-post.html',{'form':form,'tags':all_tags})
        else:
            return render(request,'myblog/inactive.html')
    # else:
    #     return render(request,'myblog/login.html')
    # return render(request,'myblog/create-post.html')

@login_required(login_url='/blog/login/')
def show_posts(request):
    if request.user.is_active:
        posts=Post.objects.filter(user_id=request.user.id).order_by('-pub_date')
        return render(request,'myblog/show-posts.html',{'posts':posts})
    else:
        return render(request,'myblog/inactive.html')

# def single_post(request,pk):
#     post=get_object_or_404(Post,pk=pk)
#     comment_form=CommentForm(request.POST or None)
#     comment_form['post'].field.widget.attrs['value']=pk
#     return render(request,'myblog/single-articale.html',{'post':post,'comment_form':comment_form})

class PostView(generic.DetailView): #single post page

    model = Post
    template_name = 'myblog/single-articale.html'

    def get_context_data(self, **kwargs):
        post=get_object_or_404(Post,id=self.kwargs['pk'])
        post.num_views += 1
        post.save()
        context = super(PostView, self).get_context_data(**kwargs)
        context['comment_form'] = CommentForm(None)
        context['comment_form']['post'].field.widget.attrs['value'] = self.kwargs['pk']
        context['comments']=Comment.objects.filter(post=self.kwargs['pk'])
        context['latest_posts']=Post.objects.filter(is_published=True).order_by('-pub_date')[:3]
        context['most_viewed_posts']=Post.objects.filter(is_published=True).order_by('-num_views','-pub_date')[:3]
        context['similars']=[tuple[0] for tuple in Counter(Post.objects.filter(is_published=True,tag__name__in=['php','python'])).most_common(4)]
        return context

@login_required(login_url='/blog/login/')
def update_post(request,pk):
    if request.user.is_active:
        post=get_object_or_404(Post,id=pk)
        if request.user.id == post.user.id:
            if request.method == 'POST':
                    post=get_object_or_404(Post,id=pk)
                    form = PostForm(request.POST,request.FILES,instance=post)
                    if form.is_valid():
                        new_post=form.save(commit=False)
                        if request.POST.has_key('is_published'):
                            new_post.pub_date=datetime.datetime.now()

                        new_post.tag_set.clear()
                        new_tags_list=list(set([ tag.lower() for tag in request.POST['tags'].split(',')])) #for case insensitive comparison
                        new_tags=[Tag(name=tag) for tag in new_tags_list ]
                        new_new_tags=[tag for tag in new_tags if not Tag.objects.filter(name__iexact=tag.name).exists() ]
                        Tag.objects.bulk_create(new_new_tags)
                        for tag in new_tags:
                            new_post.tag_set.add(Tag.objects.get(name=tag.name))
                        new_post.save()

                        return HttpResponseRedirect(reverse('show_posts'))
                    else:
                        all_tags=json.dumps([unicode(i) for i in Tag.objects.values_list('name',flat=True)])
                        old_tags= str(','.join(Tag.objects.filter(post=get_object_or_404(Post,id=pk)).values_list('name',flat=True)))
                        return render(request,'myblog/update-post.html',{'form':form,'id':pk,'tags':all_tags,'old_tags':old_tags,'image':post.image.url})
        else:
            raise PermissionDenied

        form=PostForm(instance=post)
        all_tags=json.dumps([unicode(i) for i in Tag.objects.values_list('name',flat=True)])
        old_tags= str(','.join(Tag.objects.filter(post=get_object_or_404(Post,id=pk)).values_list('name',flat=True)))
        return render(request,'myblog/update-post.html',{'form':form,'id':pk,'tags':all_tags,'old_tags':old_tags,'image':post.image.url})
    else:
        return render(request,'myblog/inactive.html')

@login_required(login_url='/blog/login/')
def delete_post(request,pk):
    if request.user.is_active:
        post=Post.objects.get(pk=pk)
        if post.user.id == request.user.id:
            post.delete()
            return HttpResponseRedirect(reverse('show_posts'))
        else:
            raise PermissionDenied
    else:
        return render(request,'myblog/inactive.html')

# def create_comment(request):
#     form = CommentForm(request.POST)
#     if form.is_valid():
#         new_comment=form.save(commit=False)
#         new_comment.user=request.user
#         if request.POST.has_key('parent'):
#             new_comment.parent=get_object_or_404(Comment,id=request.POST['parent'])
#         else:
#             new_comment.parent=None
#         new_comment.save()
#         return  HttpResponse('done')

@login_required(login_url='/blog/login/')
def create_comment(request):
    if request.user.is_active:
        new_comment=Comment(content=request.POST['content'],)
        if request.POST['parent'] != 'c':
             new_comment.parent=get_object_or_404(Comment,id=request.POST['parent'])
        else:
            new_comment.parent=None
        new_comment.user=get_object_or_404(User,id=request.POST['user'])
        new_comment.post=get_object_or_404(Post,id=request.POST['post'])
        new_comment.save()
        return HttpResponse(serializers.serialize('json',Comment.objects.filter(id=new_comment.id)))
    else:
        return render(request,'myblog/inactive.html')

@login_required(login_url='/blog/login/')
def delete_comment(request):
    if request.user.is_active:
        comment=get_object_or_404(Comment,id=request.POST['id'])
        if comment.user.id == request.user.id:
            comment.delete()
            return HttpResponse('done')
        else:
            raise PermissionDenied
    else:
        return render(request,'myblog/inactive.html')

@login_required(login_url='/blog/login/')
def like_comment(request):
    if request.user.is_active:
        comment=get_object_or_404(Comment,id=request.POST['comment_id'])
        user=request.POST['user_id']
        comment.likes.add(user)
        return HttpResponse('done')
    else:
        return render(request,'myblog/inactive.html')

@login_required(login_url='/blog/login/')
def unlike_comment(request):
    if request.user.is_active:
        comment=get_object_or_404(Comment,id=request.POST['comment_id'])
        user=request.POST['user_id']
        comment.likes.remove(user)
        return HttpResponse('done')
    else:
        return render(request,'myblog/inactive.html')

def get_tags(request):
    return HttpResponse(serializers.serialize('json',Tag.objects.all().values_list('name',flat=True)))


def similar_posts(request,tag_id):
    posts=Post.objects.filter(tag__id=tag_id,is_published=True).order_by('-pub_date')
    latest_posts=Post.objects.filter(is_published=True).order_by('-pub_date')[:3]
    most_viewed_posts=Post.objects.filter(is_published=True).order_by('-num_views','-pub_date')[:3]
    return render(request,'myblog/similar_posts.html',{'posts':posts,'latest_posts':latest_posts,'most_viewed_posts':most_viewed_posts})
    # new_comment=form.save(commit=False)
    # new_comment.user=request.user
    # if request.POST.has_key('parent'):
    #     new_comment.parent=get_object_or_404(Comment,id=request.POST['parent'])
    # else:
    #     new_comment.parent=None
    # new_comment.save()
    # return  HttpResponse('done')


    # return HttpResponseRedirect(reverse('PostView'))
@login_required(login_url='/blog/login/')
def mark_post(request,post_id):
    if request.user.is_active:
        post=get_object_or_404(Post,id=post_id)
        post.marked.add(get_object_or_404(User,id=request.POST['user_id']))
        return HttpResponse('done')
    else:
        return render(request,'myblog/inactive.html')

@login_required(login_url='/blog/login/')
def unmark_post(request,post_id):
    if request.user.is_active:
        post=get_object_or_404(Post,id=post_id)
        post.marked.remove(request.POST['user_id'])
        return HttpResponse('done')
    else:
        return render(request,'myblog/inactive.html')

@login_required(login_url='/blog/login/')
def marked_posts(request):
    if request.user.is_active:
        posts=request.user.mark.all()
        return render(request,'myblog/marked-posts.html',{'posts':posts})
    else:
        return render(request,'myblog/inactive.html')

def signup(request):
    if request.method == 'POST':
        form=UserForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.password=make_password(user.password)
            user.save()
            return render(request,'myblog/login.html')
    form=UserForm(request.POST or None)
    return render(request,'myblog/signup.html',{'form':form})

# def post(request,post_id):
#
#         # post=Post.objects.get(id=post_id)
#         post=get_object_or_404(Post,id=post_id)
#
#
#         return render(request,'myblog/post.html',{'post':post})
    # return HttpResponse(post.title+'...'+post.content)

