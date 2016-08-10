import datetime
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Post,Comment,Tag
from django.shortcuts import render
from django.shortcuts import render
from django.http import Http404
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from .forms import PostForm
# from django.contrib.auth.decorators import login_required

def index(request):
    posts=Post.objects.filter(is_published=True).order_by('-pub_date')[:6]
    return render(request,'myblog/index.html',{'posts':posts})

def log_in(request):
    return render(request,'myblog/login.html')

def signin(request):
    user=authenticate(username=request.POST['username'],password=request.POST['password'])
    if user:
        if user.is_active:
            login(request,user)
            return HttpResponseRedirect(reverse('index'))
            # return HttpResponse('wellcome')
        else:
            return HttpResponse('not active :(')
    else:
        return HttpResponse('incorrect!!')

def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

# @login_required
def create_post(request):
    if request.user.is_authenticated(): # uathentication
        if request.method == 'POST':
            # return HttpResponse(request.POST['is_published'])
            form=PostForm(request.POST,request.FILES)
            if form.is_valid():
                new_post=form.save(commit=False)
                new_post.user_id=request.user.id
                if request.POST.has_key('is_published'):
                    new_post.pub_date=datetime.datetime.now()
                new_post.save()
                return HttpResponseRedirect(reverse('create_post'))
            # return HttpResponse(request.FILES['image'].name)
        form = PostForm(request.POST or None)
        return render(request,'myblog/create-post.html',{'form':form})
    else:
        return render(request,'myblog/login.html')
    # return render(request,'myblog/create-post.html')

def show_posts(request):
    posts=Post.objects.filter(user_id=request.user.id).order_by('-pub_date')
    return render(request,'myblog/show-posts.html',{'posts':posts})

# def single_post(request,pk):
#     post=get_object_or_404(Post,pk=pk)
#     return render(request,'myblog/single-articale.html',{'post':post})

class PostView(generic.DetailView):
    model = Post
    template_name = 'myblog/single-articale.html'

def update_post(request,pk):
    if request.method == 'POST':
        post=get_object_or_404(Post,id=pk)
        form = PostForm(request.POST,request.FILES,instance=post)
        if form.is_valid():
            new_post=form.save(commit=False)
            if request.POST.has_key('is_published'):
                new_post.pub_date=datetime.datetime.now()
            new_post.save()
        return HttpResponseRedirect(reverse('update_post',args=[pk]))

    form=PostForm(instance=get_object_or_404(Post,pk=pk))
    return render(request,'myblog/update-post.html',{'form':form,'id':pk})

def delete_post(request,pk):
    post=Post.objects.get(pk=pk).delete()
    return HttpResponseRedirect(reverse('show_posts'))
# def post(request,post_id):
#
#         # post=Post.objects.get(id=post_id)
#         post=get_object_or_404(Post,id=post_id)
#
#
#         return render(request,'myblog/post.html',{'post':post})
    # return HttpResponse(post.title+'...'+post.content)

