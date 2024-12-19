from django.db import models
from django.urls import reverse_lazy

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
        

class Books(BaseModel):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    price = models.IntegerField()
    
    class Meta:
        db_table = 'books'
    
    def get_absolute_url(self):
        return reverse_lazy('store:detail_book', kwargs={'book_id': self.pk})


class Pictures(BaseModel):
    picture = models.FileField(upload_to='pictures/')
    book = models.ForeignKey(
        Books, on_delete=models.CASCADE, related_name='pictures',
    )