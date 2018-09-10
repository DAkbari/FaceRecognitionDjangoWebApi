from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from identify.Serializer import PersonSerializer
from identify.models import Person
from django.views import generic
from django.urls import reverse_lazy
from django.views.generic import View
from identify import forms
from django.core.files import File
from django.shortcuts import redirect
import base64
from django.core.files.base import ContentFile
from identify.FaceDetection import faceDetection
from rest_framework.views import APIView, Response
import uuid
import os

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

    #display a blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

        # process form data
    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            # clean normalized data
            # facePicture = form.cleaned_data['facePicture']
            user.save()

            Data_face_image = face_recognition.load_image_file(user.facePicture.path)
            try:
                faceEncode = face_recognition.face_encodings(Data_face_image)[0]
                filename = "numpySave/" + str(user.id)
                numpy.save(filename, faceEncode)

                # f = open(filename)
                # user.faceEncode.save(str(user.id), File(f))
                # f.close()
                # os.remove(filename)
                # user.save()
            except Exception as e:
                print(str(e))

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
        try:
            data = request.POST['facePic']
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            filename = "recorded/"
            filename += "newPhoto"
            filename += "." + ext

            imagedata = base64.b64decode(imgstr)
            fh = open(filename, 'wb')
            fh.write(imagedata)
            fh.close()

            ids = faceDetection()
            # for val in ids:
            #     newcommer = Person.objects.filter(id=val)[0]
            #     newcommer.lastLoginPicture.save(str(newcommer.id), File(fh))
            names = ""
            for iden in ids:
                detectedPerson = Person.objects.filter(id=iden).first()
                names += detectedPerson.firstName + ' ' + detectedPerson.lastName + ','
            names = names[:len(names) - 1]

            return render(request, 'identify/capture.html', {'names': names})
        except Exception as e:
            print(e)


class capture_api(APIView):
    def post(self, request):
        try:
            data = request.POST['facePicJson']
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            filename = "recorded/"
            filename += "newPhoto"
            filename += "." + ext

            imagedata = base64.b64decode(imgstr)
            fh = open(filename, 'wb')
            fh.write(imagedata)
            fh.close()

            ids = faceDetection()
            result = Person.objects.filter(id__in=ids)
            serializer = PersonSerializer(result, many=True)
            return Response(serializer.data)
        except Exception as e:
            print(e)



