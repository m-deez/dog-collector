from django.shortcuts import render
from django.views import View # <- View class to handle requests
from django.http import HttpResponse # <- a class to handle sending a type of response
from django.views.generic.base import TemplateView
from .models import Dog


class Home(TemplateView):
    template_name = "home.html"

class About(TemplateView):
    template_name = "about.html"

# class Dog:
#     def __init__(self, name, breed, image, bio):
#         self.name = name
#         self.breed = breed
#         self.image = image
#         self.bio = bio

dogs = [
    Dog("Lilly", "Beagle", "https://i.imgur.com/EuYvkb3.jpeg", "Lilly is the bestest gurl ever."),
    Dog("Lilly2", "Also Beagle", "https://i.imgur.com/NgFZl5a.jpeg", "Lilly2 is a test."),
    Dog("Lilly3", "Weiner doggo", "https://i.imgur.com/79RWIBH.jpeg", "Lilly3 is a doofus.")
]

class DogList(TemplateView):
    template_name = 'dog_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name")
        # If a query exists we will filter by name 
        if name != None:
            # .filter is the sql WHERE statement and name__icontains is doing a search for any name that contains the query param
            context["dogs"] = Dog.objects.filter(name__icontains=name)
            context["header"] = f"Searching for {name}"
        else:
            context["dogs"] = Dog.objects.all()
            context["header"] = "Trending Doggos"
        return context