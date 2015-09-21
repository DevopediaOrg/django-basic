from django.contrib import admin
from .models import Topping, Pizza, Restaurant

admin.site.register(Topping)
admin.site.register(Pizza)
admin.site.register(Restaurant)