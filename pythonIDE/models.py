from django.db import models
from django.conf import settings
# Create your models here.


class Integrated_development_env(models.Model):
    code = models.TextField(blank=True,null=True)
    
    def __str__(self) -> str:
        return f'{self.code}'
    
    
class CodeSnippet(models.Model):
    code = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.code}'
    
class Useraccess(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    access_code = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return  f'{self.user} asses code:{self.access_code}'
    
    
    

    