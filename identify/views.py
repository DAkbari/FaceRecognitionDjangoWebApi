from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from identify.models import Person
from django.views import generic
from django.urls import reverse_lazy


# Create your views here.


class IndexView(generic.ListView):
    template_name = 'identify/index.html'
    context_object_name = 'all_people'

    def get_queryset(self):
        return Person.objects.all()


class DetailView(generic.DeleteView):
    model = Person
    fields = ['firstName', 'lastName', 'code', 'facePicture']


class PersonCreate(CreateView):
    model = Person
    fields = ['firstName', 'lastName', 'facePicture', 'code']


class PersonUpdate(UpdateView):
    model = Person
    fields = ['firstName', 'lastName', 'facePicture', 'code']


class PersonDelete(DeleteView):
    model = Person
    success_url = reverse_lazy('identify:index')