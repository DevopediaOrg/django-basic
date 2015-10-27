from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy
from django.views import generic
from .models import Topic, Post
from .forms import PostForm


def get_path_items(path, pk=None, topic=None):
    ''' Obtain path items to aid the display of menu and breadcrumbs.
        What we get from URL is a slug. This has to be matched
        against the actual topic name.
    '''
    
    topics = Topic.objects.all().values_list('name', flat=True)
    slugs = [slugify(x) for x in topics]

    if pk: # DetailView
        curr_post = Post.objects.all().select_related('topic').get(pk=pk)
        curr_topic = curr_post.topic.name
        path_items = ['topics', curr_topic]
    elif topic: # ListView
        tindex = slugs.index(topic)
        curr_topic = topics[tindex]
        path_items = ['topics', curr_topic]
    elif ('post/new' in path or # CreateView
          'post/' in path and '/edit' in path): # UpdateView
        curr_topic = None
        path_items = ['topics']
    else:
        curr_topic = None
        path_items = []

    return path_items, curr_topic


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **kwargs):
        view = super().as_view(**kwargs)
        return login_required(view)


class AboutView(generic.TemplateView):
    template_name = 'blog/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        path_items, curr_topic = \
            get_path_items(self.request.path)
        topics = Topic.get_topics()
        context.update({
            'path_items': path_items,
            'topics': topics,
            'curr_topic': curr_topic,
            'topics': topics,
        })
        return context


class ListView(generic.ListView):
    context_object_name = 'posts' # default is object_list or post_list
    paginate_by = 8

    def get_queryset(self):
        filters = { 'published_date__lte' : timezone.now() }
        if 'topic' in self.kwargs:
            path_items, curr_topic = \
                get_path_items(self.request.path, topic=self.kwargs['topic'])
            filters['topic__name'] = curr_topic
        return Post.objects.filter(**filters) \
                           .prefetch_related('author','topic','tags')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'topic' in self.kwargs: topic = self.kwargs['topic']
        else: topic = None
        path_items, curr_topic = \
            get_path_items(self.request.path, topic=topic)
        topics = Topic.get_topics()
        context.update({
            'path_items': path_items,
            'topics': topics,
            'curr_topic': curr_topic,
            'topics': topics,
        })
        return context


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        path_items, curr_topic = \
            get_path_items(self.request.path)
        topics = Topic.get_topics()
        context.update({
            'path_items': path_items,
            'topics': topics,
            'curr_topic': curr_topic,
            'topics': topics,
        })
        return context


class UpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Post
    form_class = PostForm
    template_name_suffix = '_edit' # default is _form

    #@method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        post = form.save(commit=False)
        post.commit(self.request.user)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        path_items, curr_topic = \
            get_path_items(self.request.path)
        topics = Topic.get_topics()
        context.update({
            'path_items': path_items,
            'topics': topics,
            'curr_topic': curr_topic,
            'topics': topics,
        })
        return context


class DetailView(generic.DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        path_items, curr_topic = \
            get_path_items(self.request.path, pk=self.kwargs['pk'])
        topics = Topic.get_topics()
        context.update({
            'path_items': path_items,
            'topics': topics,
            'curr_topic': curr_topic,
            'topics': topics,
        })
        return context
