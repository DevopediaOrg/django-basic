from django.contrib import admin
from django.db.models import Q
from .models import Category, Tag, Option, Post

class CategoryAdmin(admin.ModelAdmin):
    pass


class TagAdmin(admin.ModelAdmin):
    pass


class OptionAdmin(admin.ModelAdmin):
    pass


class PostAdmin(admin.ModelAdmin):
    pass


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Option, OptionAdmin)
admin.site.register(Post, PostAdmin)
