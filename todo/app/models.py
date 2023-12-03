from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Category(models.Model): # название категории
    name = models.CharField(max_length=100)
    
    class Meta:
        verbose_name = ('Category')
        verbose_name_plural = ('Categories')
        
    def __str__(self):
        return self.name
    
class TodoList(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField(blank=True)
    created = models.DateField(default=timezone.now().strftime("%Y-%m-%d")) # дата создания
    due_date = models.DateField(default=timezone.now().strftime("%Y-%m-%d")) # дата дедлайна
    
    category = models.ForeignKey(Category,default='general',on_delete=models.PROTECT) # к какой категории относится
    user = models.ForeignKey(User,on_delete=models.CASCADE) # к какому пользователю он относится
    
    class Meta:
        ordering = ['-created'] # сортировка задач по убыванию даты создания
        
    def __str__(self):
        return self.title