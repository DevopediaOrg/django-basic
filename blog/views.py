from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy
from django.views import generic
from .models import Category, Post
from .forms import PostForm


def get_path_items(path):
    ''' Obtain path items to aid the display of breadcrumbs. '''
    
    topics = Category.objects.all().values_list('name', flat=True)
    slugs = [slugify(x) for x in topics]

    path_items = path.strip('/').split('/')
    if len(path_items)>1 and path_items[-2]=='post' and path_items[-1].isdigit():
        # Process DetailView
        curr_post = Post.objects.all().select_related('category').get(pk=path_items[-1])
        curr_topic = curr_post.category.name
        path_items[-2] = 'topics'
        path_items[-1] = curr_topic
    elif 'topics' in path_items and path_items[-1]!='topics':
        # Process ListView
        tindex = slugs.index(path_items[-1])
        path_items[-1] = topics[tindex]
        curr_topic = topics[tindex]
    else:
        curr_topic = None

    return path_items, curr_topic, topics


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **kwargs):
        view = super().as_view(**kwargs)
        return login_required(view)


class PublishedPostFilterMixin(object):
    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()) \
                           .prefetch_related('author','category','tags')


class ListView(PublishedPostFilterMixin, generic.ListView):
    context_object_name = 'posts' # default is object_list or post_list
    queryset = Post.objects.all().prefetch_related('author','category','tags')
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        path_items, curr_topic, topics = get_path_items(self.request.path)
        context.update({
            'path_items': path_items,
            'topics': topics,
            'curr_topic': curr_topic,
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
        cats = Category.get_categories()
        context.update({
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


class DetailView(generic.DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        path_items, curr_topic, topics = get_path_items(self.request.path)
        cats = Category.get_categories()
        context.update({
            'path_items': path_items,
            'topics': topics,
            'curr_topic': curr_topic,
            'categories': cats,
        })
        return context
