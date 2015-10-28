from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy
from django.views import generic
from django.http import Http404
from .models import Topic, Post
from .forms import PostForm


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **kwargs):
        view = super().as_view(**kwargs)
        return login_required(view)


class ContextMixin(object):
    def get_path_items(self):
        ''' Obtain path items to aid the display of menu and breadcrumbs.
            What we get from URL is a slug. This has to be matched
            against the actual topic name.
        '''    
        if 'pk' in self.kwargs: # DetailView
            curr_topic = self.object.topic.name
            path_items = ['topics', curr_topic]
        elif 'topic' in self.kwargs: # ListView
            curr_topic = Topic.unslugify(self.kwargs['topic'])
            path_items = ['topics', curr_topic]
        elif ('post/new' in self.request.path or # CreateView
              'post/' in self.request.path and '/edit' in self.request.path): # UpdateView
            curr_topic = None
            path_items = ['topics']
        else:
            curr_topic = None
            path_items = []
    
        return path_items, curr_topic

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        path_items, curr_topic = self.get_path_items()
        context.update({
            'path_items': path_items,
            'curr_topic': curr_topic,
            'topics': Topic.get_topics(),
        })
        return context


class AboutView(ContextMixin, generic.TemplateView):
    template_name = 'blog/about.html'


class ListView(ContextMixin, generic.ListView):
    context_object_name = 'posts' # default is object_list or post_list
    paginate_by = 8

    def get_queryset(self):
        filters = {
          'published_date__lte' : timezone.now(),
          'state__exact' : 'Published',
        }
        if 'topic' in self.kwargs:
            curr_topic = Topic.unslugify(self.kwargs['topic'])
            if not curr_topic: raise Http404("Topic does not exist")
            filters['topic__name'] = curr_topic
        return Post.objects.filter(**filters) \
                           .prefetch_related('author','topic','tags')


class CreateView(LoginRequiredMixin, ContextMixin, generic.CreateView):
    model = Post
    form_class = PostForm # OR fields = ['title','text']
    template_name = 'blog/post_edit.html' # default is blog/post_form.html

    #An alternative to using LoginRequiredMixin
    #@method_decorator(login_required)
    #def dispatch(self, *args, **kwargs):
    #    return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        post = form.save(commit=False)
        post.commit(self.request.user)
        return super().form_valid(form)


class UpdateView(LoginRequiredMixin, ContextMixin, generic.UpdateView):
    model = Post
    form_class = PostForm
    template_name_suffix = '_edit' # default is _form

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        post = form.save(commit=False)
        post.commit(self.request.user)
        return super().form_valid(form)


class DetailView(ContextMixin, generic.DetailView):
    model = Post
