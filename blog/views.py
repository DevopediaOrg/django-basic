from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy
from django.views import generic
from .models import Category, Post
from .forms import PostForm


def get_path_items(path, pk=None, category=None):
    ''' Obtain path items to aid the display of menu and breadcrumbs.
        What we get from URL is a slug. This has to be matched
        against the actual category name.
    '''
    
    topics = Category.objects.all().values_list('name', flat=True)
    slugs = [slugify(x) for x in topics]

    if pk: # DetailView
        curr_post = Post.objects.all().select_related('category').get(pk=pk)
        curr_topic = curr_post.category.name
        path_items = ['topics', curr_topic]
    elif category: # ListView
        tindex = slugs.index(category)
        curr_topic = topics[tindex]
        path_items = ['topics', curr_topic]
    elif ('post/new' in path or # CreateView
          'post/' in path and '/edit' in path): # UpdateView
        curr_topic = None
        path_items = ['topics']
    else:
        curr_topic = None
        path_items = []

    return path_items, curr_topic, topics


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **kwargs):
        view = super().as_view(**kwargs)
        return login_required(view)


class ListView(generic.ListView):
    context_object_name = 'posts' # default is object_list or post_list
    paginate_by = 8

    def get_queryset(self):
        filters = { 'published_date__lte' : timezone.now() }
        if 'category' in self.kwargs:
            path_items, curr_topic, topics = \
                get_path_items(self.request.path, category=self.kwargs['category'])
            filters['category__name'] = curr_topic
        return Post.objects.filter(**filters) \
                           .prefetch_related('author','category','tags')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'category' in self.kwargs: cat = self.kwargs['category']
        else: cat = None
        path_items, curr_topic, topics = \
            get_path_items(self.request.path, category=cat)
        cats = Category.get_categories()
        context.update({
            'path_items': path_items,
            'topics': topics,
            'curr_topic': curr_topic,
            'categories': cats,
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
        path_items, curr_topic, topics = \
            get_path_items(self.request.path)
        cats = Category.get_categories()
        context.update({
            'path_items': path_items,
            'topics': topics,
            'curr_topic': curr_topic,
            'categories': cats,
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
        path_items, curr_topic, topics = \
            get_path_items(self.request.path)
        cats = Category.get_categories()
        context.update({
            'path_items': path_items,
            'topics': topics,
            'curr_topic': curr_topic,
            'categories': cats,
        })
        return context


class DetailView(generic.DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        path_items, curr_topic, topics = \
            get_path_items(self.request.path, pk=self.kwargs['pk'])
        cats = Category.get_categories()
        context.update({
            'path_items': path_items,
            'topics': topics,
            'curr_topic': curr_topic,
            'categories': cats,
        })
        return context
