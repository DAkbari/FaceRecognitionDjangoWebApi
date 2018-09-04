from django.db import models


class Person:
    firstName = models.CharField(max_length=200)
    lastName = models.CharField(max_length=200)
    faceEncode = models.FileField()
    facePicture = models.FileField()
    lastLoginPicture = models.FileField()
    code = models.CharField(max_length=100)
    

