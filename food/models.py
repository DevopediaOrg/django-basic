from django.db import models

class Topping(models.Model):
    name = models.CharField(max_length=30)

class Pizza(models.Model):
    name = models.CharField(max_length=50)
    toppings = models.ManyToManyField(Topping)
    vegetarian = models.BooleanField(default=False)

    def __str__(self):
        return "{:s}: {:s}".format(self.name, ", ".join(topping.name for topping in self.toppings.all()))
        
class Restaurant(models.Model):
    pizzas = models.ManyToManyField(Pizza, related_name='restaurants')
    best_pizza = models.ForeignKey(Pizza, related_name='championed_by')

    def __str__(self):
        return "{:d} pizzas & best {:s}".format(self.pizzas.count(), self.best_pizza.name)
