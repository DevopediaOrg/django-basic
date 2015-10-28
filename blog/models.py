from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django import forms
from django.db.models import Count
from django.contrib.auth.models import User, AnonymousUser


class Topic(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self):
        return "{:s}".format(self.name)

    class Meta:
        ordering = ('name',)

    @staticmethod
    def topics():
        return Topic.objects.filter(post__state='Published') \
                            .annotate(num_posts=models.Count('post')) \
                            .values_list('name','description','num_posts')

    @staticmethod
    def unslugify(topic):
        topics = Topic.objects.all().values_list('name', flat=True)
        slugs = [slugify(x) for x in topics]
        if slugs.count(topic):
          return topics[slugs.index(topic)]
        else:
          return None
        

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return "{:s}".format(self.name)


class Option(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return "{:s}".format(self.name)


class Post(models.Model):
    author = models.ForeignKey('auth.User')

    title = models.CharField(max_length=200, blank=False, null=False)

    topic = models.ForeignKey(Topic, blank=False)

    states = ['Draft', 'Published', 'Unpublished']
    state = models.CharField(max_length=20, choices=[(x,x) for x in states], default='Draft')

    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    text = models.TextField(blank=True)

    tags = models.ManyToManyField(Tag, blank=True)

    options = models.ManyToManyField(Option, blank=True)

    image = models.ImageField(upload_to='.', blank=True, null=True)

    class Meta:
        ordering = ('-published_date',)
        
    @staticmethod
    def author_posts(username):
        # order_by(): this is to clear default grouping due to class Meta
        # https://docs.djangoproject.com/en/1.8/topics/db/aggregation/#interaction-with-default-ordering-or-order-by
        return Post.objects.filter(author__username=username) \
                           .values('state') \
                           .annotate(Count('state')) \
                           .order_by('state')

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def commit(self, user):
        if not isinstance(user, AnonymousUser):
            self.author = user
        else:
            self.author = User.objects.get(username='admin')
        self.publish()