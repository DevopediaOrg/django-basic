from django import forms
from .models import Post

class PostForm(forms.ModelForm):

    class Meta:
        model = Post

        # forms.ALL_FIELDS or '__all__' for all fields
        fields = ('title', 'topic', 'state', 'featured', 
                  'text', 'tags', 'options', 'image')

        labels = {
            'title': 'Post title'.title(),
            'text': 'Full text'.title(),
        }

        help_texts = {
            'text': 'An ideal blog post is about 700-1000 words. Avoid technical jargon. Keep it simple.',
        }

        error_messages = {
            'title': {
                'required': "Title is mandatory.",
            },
        }

        widgets = {
            'text': forms.Textarea(attrs={'cols': 80, 'rows': 20}),
            'state': forms.RadioSelect(),
            'options': forms.CheckboxSelectMultiple(),
        }
