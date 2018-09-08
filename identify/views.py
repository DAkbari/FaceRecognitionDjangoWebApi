from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from identify.models import Person
from django.views import generic
from django.urls import reverse_lazy
from django.views.generic import View
from identify import forms
import base64
from django.core.files.base import ContentFile
from identify.FaceDetection import faceDetection

import numpy
import face_recognition


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


# class Capture(View):
#     form_class = forms.ImageForm
#     template_name = "identify/capture.html"
#
#     def get(self, request):
#         form = self.form_class(None)
#         return render(request, self.template_name, {'form': form})


class PersonCreate(View):
    form_class = forms.UserForm
    template_name = 'identify/new_person_form.html'

    #display a blink form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

        # process form data
    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            # clean normalized data

            facePicture = form.cleaned_data['facePicture']
            Data_face_image = face_recognition.load_image_file(facePicture)

            try:
                user.faceEncode = face_recognition.face_encodings(Data_face_image)[0]

            except:
                print("error")

            user.save()

        return render(request, self.template_name, {'form': form})


class PersonUpdate(UpdateView):
    model = Person
    fields = ['firstName', 'lastName', 'facePicture', 'code']


class PersonDelete(DeleteView):
    model = Person
    success_url = reverse_lazy('identify:index')


def capture(request):

    if request.method == 'GET':
        return render(request, 'identify/capture.html')

    if request.method == 'POST':
        data = request.POST['imgBase64']
        format, imgstr = data.split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        personellCodes = Person.objects.all()
        faceDetection(data, )
        return HttpResponse("successful")

