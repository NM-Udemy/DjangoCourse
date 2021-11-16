from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)


class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Enter Email!')
        user = self.model(
            username=username,
            email=email
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None):
        user = self.model(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    website = models.URLField(null=True)
    picture = models.FileField(null=True)

    USERNAME_FIELD = 'email' # このテーブルのレコードを一意に識別
    REQUIRED_FIELDS = ['username'] # スーパーユーザ作成時に入力する

    objects = UserManager()

    def __str__(self):
        return self.email


class Students(models.Model):

    name = models.CharField(max_length=20)
    age = models.IntegerField()
    score = models.IntegerField()
    school = models.ForeignKey(
        'Schools', on_delete=models.CASCADE
    )
    
    class Meta:
        db_table = 'students'
        verbose_name_plural = '生徒'
        ordering = ('age',)

    def __str__(self):
        return  self.name + ': ' + str(self.age)

class Schools(models.Model):
    name = models.CharField(max_length=20, verbose_name='学校名')
    
    class Meta:
        db_table = 'schools'
        verbose_name_plural = '学校'
    
    def __str__(self):
        return  self.name
