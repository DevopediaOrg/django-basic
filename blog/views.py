import os
import json
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import reverse_lazy
from django.db.models import Count, Q
from django.views import generic
from django.http import Http404
from .models import Topic, Tag, Author, Post
from .forms import PostForm
from .utils import get_search_query


# Can be replaced with LoginRequiredMixin from django-braces
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
        curr_topic, curr_tag, curr_state = None, None, None
        path_items = []
        if 'pk' in self.kwargs: # DetailView
            curr_topic = self.object.topic.name
            path_items = ['topics', curr_topic]
        elif 'topic' in self.kwargs: # ListView
            curr_topic = Topic.unslugify(self.kwargs['topic'])
            path_items = ['topics', curr_topic]
        elif 'tag' in self.kwargs: # ListView
            curr_tag = Tag.unslugify(self.kwargs['tag'])
            path_items = ['tags', curr_tag]
        elif ('state' in self.kwargs and 
              not isinstance(self.request.user, AnonymousUser)): # ListView
            curr_state = self.kwargs['state']
            path_items = ['states', self.kwargs['state']]
        elif 'authors' in self.request.path:
            path_items = ['authors']
        elif 'about' in self.request.path:
            path_items = ['about']
        elif ('post/new' in self.request.path or # CreateView
              'post/' in self.request.path and '/edit' in self.request.path or # UpdateView
              'states' in self.request.path or # ListView
              'tags' in self.request.path or # ListView
              'topics' in self.request.path): # ListView
            path_items = ['topics']
    
        return path_items, curr_topic, curr_tag, curr_state

    def make_home_charts(self, context):
        # Pie chart of posts by topics
        basedir = os.path.dirname(os.path.abspath(__file__)) + '/static/'
        context['chart1'] = 'tmp/topics.json'
        data = [{"label":k, "value":v} for k,_,v in context['topics']]
        with open(basedir + context['chart1'],'w') as f:
            json.dump(data, f)

        # Horizontal bar chart of author posts
        context['chart2'] = 'tmp/authors.json'
        data = []
        prev_s = None
        curr = {}
        values = []
        authors = set()
        for fn,ln,s,c in Post.all_author_posts():
            if prev_s != s:
                prev_s = s
                if curr and values:
                    curr['values'] = values
                    data.append(curr)
                curr = {"key": s}
                values = []
            author = "{} {}".format(fn, ln)
            values.append({"label":author, "value":c})
            authors.add(author)
        else: # no break above, always execute
            if curr and values:
                curr['values'] = values
                data.append(curr)

        # Need to do zero-filling in case JS library doen't handle missing points
        for author in authors:
            for d in data:
                for v in d['values']:
                    if author == v['label']:
                        break
                else:
                    d['values'].append({"label":author, "value":0})

        with open(basedir + context['chart2'],'w') as f:
            json.dump(data, f)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        path_items, curr_topic, curr_tag, curr_state = self.get_path_items()
        context.update({
            'path_items': path_items,
            'curr_topic': curr_topic,
            'topics': Topic.topics(),
            'curr_tag': curr_tag,
            'tags': Tag.distribution(),
            'curr_state': curr_state,
            'search_query': self.request.GET.get('q',None),
        })

        if not path_items: # HomeView
            context['featured_posts'] = Post.featured_posts()
            self.make_home_charts(context)

        if not isinstance(self.request.user, AnonymousUser):
            context['author_post_states'] = Post.author_posts(self.request.user.username)

        return context


class AboutView(ContextMixin, generic.TemplateView):
    template_name = 'blog/about.html'


class AuthorListView(ContextMixin, generic.ListView):
    context_object_name = 'authors' # default is object_list or post_list
    template_name = 'blog/author_list.html'

    def get_queryset(self):
        return Author.objects.filter(user__post__state='Published') \
                     .annotate(num_posts=Count('user__post')) \
                     .order_by('user__first_name','user__last_name')


class SearchResultsView(ContextMixin, generic.ListView):
    context_object_name = 'posts' # default is object_list or post_list
    template_name = 'blog/search_results.html'
    paginate_by = 12

    def get_queryset(self):
        q = self.request.GET.get('q',None)
        if q:
            query = get_search_query(q, ['title', 'text'])
            perms = Q(state='Published') | Q(author__id=self.request.user.id)
            return Post.objects.filter(query).filter(perms)
        else:
            return []


class ListView(ContextMixin, generic.ListView):
    context_object_name = 'posts' # default is object_list or post_list
    paginate_by = 8

    def get_queryset(self):
        filters = {}

        if 'state' in self.kwargs:
            if not isinstance(self.request.user, AnonymousUser):
                if self.kwargs['state'] in Post.states:
                    filters['author'] = self.request.user
                    filters['state'] = self.kwargs['state']
                else:
                    raise Http404("The specified state does not exist")
            else:
                raise Http404("You must be logged in as author to view your posts by state")
        else:
            filters['published_date__lte'] = timezone.now()
            filters['state'] = 'Published'

        if 'topic' in self.kwargs:
            curr_topic = Topic.unslugify(self.kwargs['topic'])
            if not curr_topic: raise Http404("The specified topic does not exist")
            filters['topic__name'] = curr_topic

        if 'tag' in self.kwargs:
            curr_tag = Tag.unslugify(self.kwargs['tag'])
            if not curr_tag: raise Http404("The specified tag does not exist")
            filters['tags__name'] = curr_tag

        return Post.objects.filter(**filters) \
                           .prefetch_related('author','topic','tags')


class HomeView(ListView):
    context_object_name = 'posts' # default is object_list or post_list
    template_name = 'blog/home.html'
    paginate_by = 0


class CreateView(LoginRequiredMixin, ContextMixin, generic.CreateView):
    model = Post
    form_class = PostForm # OR fields = ['title','text']
    template_name = 'blog/post_edit.html' # default is blog/post_form.html

    #An alternative to using LoginRequiredMixin
    #from django.utils.decorators import method_decorator
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

    def dispatch(self, *args, **kwargs):
        if self.request.user.id!=self.get_object().author.id:
            raise Http404("Only the original creator can edit the post")
        return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        post = form.save(commit=False)
        post.commit(self.request.user)
        return super().form_valid(form)


class DetailView(ContextMixin, generic.DetailView):
    model = Post

class DeleteView(LoginRequiredMixin, ContextMixin, generic.DeleteView):
    model = Post
    success_url = reverse_lazy('blog:author_list')