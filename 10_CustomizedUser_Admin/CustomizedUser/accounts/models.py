from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)

class UserManager(BaseUserManager):
    
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('メールアドレスは必須です')
        if not username:
            raise ValueError('ユーザー名は必須です')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_active'] = True
        extra_fields['is_superuser'] = True
        return self.create_user(email, username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    
    username = models.CharField(max_length=150)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    website = models.URLField(null=True)
    picture = models.FileField(null=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email' # このテーブルのレコードを一意に識別するField
    REQUIRED_FIELDS = ['username'] # createsuperuserの時に入力を求められる
    
    def __str__(self):
        return self.email

class Students(models.Model):
    name = models.CharField(max_length=20)
    age = models.IntegerField()
    score = models.IntegerField()
    school = models.ForeignKey(
        'Schools', on_delete=models.CASCADE, related_name='students',
    )
    
    class Meta:
        db_table = 'students'
        verbose_name_plural = '生徒'
        ordering = ('age', '-score',)
        
    def __str__(self):
        return f'{self.name}: {self.age}'

class Schools(models.Model):
    name = models.CharField(max_length=20,verbose_name='学校名')
    
    class Meta:
        db_table = 'schools'
        verbose_name_plural = '学校'
        

    def __str__(self):
        return self.name
