from django.db import models
from django.core.validators import FileExtensionValidator

class User(models.Model):
    name = models.CharField(max_length=10)
    age = models.IntegerField()
    mail = models.EmailField()

class Post(models.Model):
    name = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    memo = models.CharField(max_length=255)

class Memo(models.Model):
    title = models.CharField(max_length=5)
    memo = models.CharField(max_length=255)

class Profile(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    picture = models.FileField(upload_to='picture/%Y/%m/%d',
        validators=[
            FileExtensionValidator(
                ['png',], 
                message='pngでアップロードしてください'
            )
        ]
    )
