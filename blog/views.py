from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy
from django.views import generic
from .models import Post
from .forms import PostForm


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **kwargs):
        view = super().as_view(**kwargs)
        return login_required(view)


class PublishedPostFilterMixin(object):
    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()) \
                           .order_by('-published_date')


class ListView(PublishedPostFilterMixin, generic.ListView):
    context_object_name = 'posts' # default is object_list or post_list    


class CreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    form_class = PostForm # OR fields = ['title','text']
    template_name = 'blog/post_edit.html' # default is blog/post_form.html

    #@method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        post = form.save(commit=False)
        post.commit(self.request.user)
        return super().form_valid(form)


class UpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Post
    form_class = PostForm
    template_name_suffix = '_edit' # default is _form

    #@method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        print(self.request)
        return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        post = form.save(commit=False)
        post.commit(self.request.user)
        return super().form_valid(form)


class DetailView(generic.DetailView):
    model = Post
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = Post.objects.select_related('author').get(pk=self.object.pk).author
        return context