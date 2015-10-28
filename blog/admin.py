from django.contrib import admin
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



from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Author

class AuthorInline(admin.StackedInline):
    model = Author
    can_delete = False
    verbose_name_plural = 'author'

class UserAdmin(UserAdmin):
    inlines = (AuthorInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

