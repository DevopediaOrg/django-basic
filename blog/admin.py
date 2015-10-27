from django.contrib import admin
from django.db.models import Q
from .models import Topic, Tag, Option, Post

class TopicAdmin(admin.ModelAdmin):
    pass


class TagAdmin(admin.ModelAdmin):
    pass


class OptionAdmin(admin.ModelAdmin):
    pass


class PostAdmin(admin.ModelAdmin):
    pass


admin.site.register(Topic, TopicAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Option, OptionAdmin)
admin.site.register(Post, PostAdmin)
