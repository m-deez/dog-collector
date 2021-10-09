from django.shortcuts import render, redirect
from django.views import View # <- View class to handle requests
from django.http import HttpResponse # <- a class to handle sending a type of response
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView
from django.urls import reverse
from .models import Dog, Collar, Walker
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Main Classes ====================================================

class Home(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['walkers'] = Walker.objects.all()
        return context

class About(TemplateView):
    template_name = "about.html"

class Signup(View):

    def get(self, request):
        form = UserCreationForm()
        context = {"form": form}
        return render(request, "registration/signup.html", context)

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("artist_list")
        else:
            context = {"form": form}
            return render(request, "registration/signup.html", context)

# Dog Classes ======================================================

@method_decorator(login_required, name='dispatch')
class DogList(TemplateView):
    template_name = 'dog_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name")
        if name != None:
            context["dogs"] = Dog.objects.filter(name__icontains=name, user=self.request.user)
            context["header"] = f"Searching for {name}"
        else:
            context["dogs"] = Dog.objects.filter(user=self.request.user)
            context["header"] = "Trending Doggos"
        return context

@method_decorator(login_required, name='dispatch')
class DogCreate(CreateView):
    model = Dog
    fields = ['name', 'breed', 'img', 'bio', 'verified_doggo']
    template_name = "dog_create.html"
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(DogCreate, self).form_valid(form)

    def get_success_url(self):
        print(self.kwargs)
        return reverse('dog_detail', kwargs={'pk': self.object.pk})

@method_decorator(login_required, name='dispatch')
class DogDetail(DetailView):
    model = Dog
    template_name = "dog_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["walkers"] = Walker.objects.all()
        return context

@method_decorator(login_required, name='dispatch')
class DogUpdate(UpdateView):
    model = Dog
    fields = ['name', 'breed', 'img', 'bio', 'verified_doggo']
    template_name = "dog_update.html"
    def get_success_url(self):
        return reverse('dog_detail', kwargs={'pk': self.object.pk})

@method_decorator(login_required, name='dispatch')
class DogDelete(DeleteView):
    model = Dog
    template_name = "dog_delete_confirmation.html"
    success_url = "/dogs/"

@method_decorator(login_required, name='dispatch')
class CollarCreate(View):

    def post(self, request, pk):
        brand = request.POST.get("brand")
        length = request.POST.get("length")
        color = request.POST.get("color")
        dog = Dog.objects.get(pk=pk)
        Collar.objects.create(brand=brand, length=length, color=color, dog=dog)
        return redirect('dog_detail', pk=pk)

@method_decorator(login_required, name='dispatch')
class WalkerDogAssoc(View):

    def get(self, request, pk, dog_pk):
        assoc = request.GET.get("assoc")

        if assoc == "remove":
            Walker.objects.get(pk=pk).dog.remove(dog_pk)

        if assoc == "add":
            Walker.objects.get(pk=pk).dog.add(dog_pk)
        return redirect('home')