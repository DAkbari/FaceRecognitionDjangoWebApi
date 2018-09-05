from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from identify.models import Person
from django.views import generic
from django.urls import reverse_lazy
from django.views.generic import View
from .forms import UserForm


# Create your views here.


class IndexView(generic.ListView):
    template_name = 'identify/index.html'
    context_object_name = 'all_people'

    def get_queryset(self):
        return Person.objects.all()


class DetailView(generic.DeleteView):
    model = Person
    fields = ['firstName', 'lastName', 'code', 'facePicture']
    template_name = 'identify/detail.html'


class PersonCreate(View):
    form_class = UserForm
    template_name = 'identify/new_person_form.html'

    #display a blink form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

        # process form data
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # clean normalized data
            facePicture = form.cleaned_data['username']
            FName = form.cleaned_data['firstName']
            LName = form.cleaned_data['lastName']
            code = form.cleaned_data['code']
            user.save()

        return render(request, self.template_name, {'form': form})


class PersonUpdate(UpdateView):
    model = Person
    fields = ['firstName', 'lastName', 'facePicture', 'code']


class PersonDelete(DeleteView):
    model = Person
    success_url = reverse_lazy('identify:index')