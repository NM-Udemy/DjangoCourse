from django.db import models
from accounts.models import User

class ThemeManager(models.Manager):
    
    def fetch_all_themes(self):
        return self.order_by('id').all()

class Theme(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
    )
    
    objects: ThemeManager = ThemeManager()
    
    class Meta:
        db_table = 'theme'

class CommentManager(models.Manager):

    def fetch_by_theme_id(self, theme_id):
        return self.filter(theme_id=theme_id).order_by('id').all()

class Comment(models.Model):
    comment = models.CharField(max_length=1000)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
    )
    theme = models.ForeignKey(
        Theme, on_delete=models.CASCADE,
    )
    
    objects: CommentManager = CommentManager()
    
    class Meta:
        db_table = 'comment'
