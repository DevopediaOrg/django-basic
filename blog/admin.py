from django.contrib import admin
from django.db.models import Q
from .models import Post

class PublishedTimeFilter(admin.SimpleListFilter):
    title = 'published time'
    parameter_name = 'time'

    def lookups(self, request, model_admin):
        return (
            ('am', 'AM'),
            ('pm', 'PM'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'am':
            return queryset.filter(
                     Q(published_date__hour=0) | Q(published_date__hour=1) | Q(published_date__hour=2) |
                     Q(published_date__hour=3) | Q(published_date__hour=4) | Q(published_date__hour=5) |
                     Q(published_date__hour=6) | Q(published_date__hour=7) | Q(published_date__hour=8) |
                     Q(published_date__hour=9) | Q(published_date__hour=10) | Q(published_date__hour=11))
        if self.value() == 'pm':
            return queryset.filter(
                     Q(published_date__hour=12) | Q(published_date__hour=13) | Q(published_date__hour=14) |
                     Q(published_date__hour=15) | Q(published_date__hour=16) | Q(published_date__hour=17) |
                     Q(published_date__hour=18) | Q(published_date__hour=19) | Q(published_date__hour=20) |
                     Q(published_date__hour=21) | Q(published_date__hour=22) | Q(published_date__hour=23))


class PostAdmin(admin.ModelAdmin):
    def upper_case_title(obj):
        '''An attribute on Model called on model instance.'''
        return obj.title.upper()
    upper_case_title.short_description = 'Title'

    def created_fmt(self, obj):
        '''An attribute on ModelAdmin.'''
        return obj.created_date.strftime('%d-%m-%Y %H:%M')
    created_fmt.short_description = 'Created date'

    def truncate_text(obj):
        '''An attribute on Model called on model instance.'''
        if len(obj.text) > 53:
            return obj.text[:50]+'...'
        else:
            return obj.text
    truncate_text.short_description = 'Text'

    fieldsets = [
        (None, {'fields': ['title','author']}),
        ('Content', {'fields': ['text']}),
        ('Date information', {'fields': [('created_date','published_date')], 'classes': ['collapse']}),
    ]
    search_fields = ['title', 'text']
    readonly_fields = ('created_date',)
    list_display = (upper_case_title, 'author', 'created_fmt', 'published_date', truncate_text)
    list_filter = ('author', PublishedTimeFilter)
    ordering = ('title', '-published_date')
    list_per_page = 5


admin.site.register(Post, PostAdmin)
