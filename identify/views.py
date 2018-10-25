from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login, logout
from identify.Serializer import PersonSerializer
from identify.models import Person
from django.views import generic
from django.urls import reverse_lazy
from django.views.generic import View
from identify import forms
from django.db.models import Q
from django.core.files import File
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
import base64
from django.core.files.base import ContentFile
from identify.FaceDetection import faceDetection
from rest_framework.views import APIView, Response
import uuid
import os

import numpy
import face_recognition
# Create your views here.


class IndexView(LoginRequiredMixin, generic.ListView):
    login_url = 'identify/login'
    redirect_field_name = ''
    template_name = 'identify/index.html'
    context_object_name = 'all_people'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Person.objects.filter(Q(code__contains=query) | Q(firstName__contains=query) | Q(lastName__contains=query) & Q(associatedUser=self.request.user))
        return Person.objects.filter(associatedUser=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['active_menu'] = 'List'
        return context


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
        return render(request, self.template_name, {'form': form, 'active_menu': 'Create'})

        # process form data
    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.associatedUser = self.request.user
            # clean normalized data
            # facePicture = form.cleaned_data['facePicture']
            user.save()
            saveEncode(user)
        # return render(request, self.template_name, {'form': form, 'active_menu': 'Create'})
        return redirect('identify:index')


class PersonUpdate(UpdateView):
    model = Person
    fields = ['firstName', 'lastName', 'facePicture', 'code']

    def form_valid(self, form):
        person = form.save(commit=False)
        person.save()
        saveEncode(person)
        return redirect('identify:index')


class PersonDelete(DeleteView):
    model = Person
    success_url = reverse_lazy('identify:index')


def capture(request):
    if request.method == 'GET':
        return render(request, 'identify/capture.html', {'active_menu': 'Capture'})

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

            ids = faceDetection(request.user)
            # for val in ids:
            #     newcommer = Person.objects.filter(id=val)[0]
            #     newcommer.lastLoginPicture.save(str(newcommer.id), File(fh))
            names = ""
            for iden in ids:
                detectedPerson = Person.objects.filter(id=iden).first()
                names += detectedPerson.firstName + ' ' + detectedPerson.lastName + ','

            names = names[:len(names) - 1]

            return render(request, 'identify/capture.html', {'names': names, 'active_menu': 'Capture'})
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

            ids = faceDetection(self.request.user)
            result = Person.objects.filter(id__in=ids)
            serializer = PersonSerializer(result, many=True)
            return Response(serializer.data)
        except Exception as e:
            print(e)


def user_login(request):
    if request.method == "GET":
        return render(request, 'Registration/login.html')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/identify')
        else:
            return render(request, 'Registration/login.html', {'Error': 'نام کاربری و یا رمز عبور اشتباه است'})


def user_logout(request):
    logout(request)
    return render(request, 'Registration/login.html')


def user_register(request):
    # if request.method == "GET":
    #     return render(request, 'Registration/register.html')
    # if request.method == "POST":
    #     firstname = request.POST['first_name']
    #     lastname = request.POST['last_name']
    #     username = request.POST['username']
    #     password = request.POST['password']
    #     email = request.POST['email']
    #     user = User.objects.create_user(username, email, password, first_name=firstname, last_name=lastname)
    #     user.save()
    #     login(request, user)
    #     return redirect('/identify')
    if request.method == "GET":
        form = forms.NewUser();
        return render(request, 'Registration/register.html', {'form': form})
    if request.method == "POST":
        form = forms.NewUser(request.POST)
        if form.is_valid():

            existingUser = User.objects.filter(username=form.cleaned_data['username'])
            if len(existingUser)>0:
                form.add_error(None, 'نام کاربری قبلا استفاده شده است!')
                return render(request, 'Registration/register.html', {'form': form})
            user = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'],
                                            form.cleaned_data['password'],
                                            first_name=form.cleaned_data['first_name'],
                                            last_name=form.cleaned_data['last_name'])
            user.save()
            login(request, user)
            return redirect('/identify')
        else:
            return render(request, 'Registration/register.html', {'form': form})


def saveEncode(user):
    filepath = user.facePicture.path
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