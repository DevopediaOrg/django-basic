from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.models import User, AnonymousUser
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View
from .models import Post
from .forms import PostForm

class PostListView(View):
    def get(self, request):
        try:
            author = User.objects.get(username='admin')
            posts = Post.objects.filter(published_date__lte=timezone.now(),
                                        author=author) \
                                .order_by('-published_date')
        except ObjectDoesNotExist:
            posts = None
        return render(request, 'blog/post_list.html', {'posts': posts})

    
class PostNewView(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        form = PostForm()
        return render(request, 'blog/post_edit.html', {'form': form})    

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            if not isinstance(request.user, AnonymousUser):
                post.author = request.user
            else:
                post.author = User.objects.get(username='admin')
            post.published_date = timezone.now()
            post.save()
            return redirect('blog:post_detail', pk=post.pk)
        else:
            return render(request, 'blog/post_edit.html', {'form': form})


class PostEditView(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['pk'])
        form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form': form})    

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['pk'])
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            if not isinstance(request.user, AnonymousUser):
                post.author = request.user
            else:
                post.author = User.objects.get(username='admin')
            post.published_date = timezone.now()
            post.save()
            #return HttpResponseRedirect('/post/'+str(post.pk))
            return redirect('blog:post_detail', pk=post.pk)
        else:
            return render(request, 'blog/post_edit.html', {'form': form})


class PostDetailView(View):
    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['pk'])
        return render(request, 'blog/post_detail.html', {'post': post})
