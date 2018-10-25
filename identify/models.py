from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Person(models.Model):
    firstName = models.CharField('نام', max_length=200)
    lastName = models.CharField('نام خانوادگی', max_length=200)
    faceEncode = models.FileField(upload_to="encodes/")
    facePicture = models.FileField('تصویر', upload_to="faces/")
    lastLoginPicture = models.FileField('آخرین تشخیص', upload_to='lastPhoto/')
    code = models.CharField('کد پرسنلی', max_length=100)
    associatedUser = models.ForeignKey(User, on_delete=models.CASCADE)

    def as_json(self):
        return dict(firsName=self.firstName,
                    lastName=self.lastName,
                    code=self.code)

    def get_absolute_url(self):
        return reverse('identify:detail', kwargs={'pk': self.pk})


