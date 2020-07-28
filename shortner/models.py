from django.db import models
from .utils import code_generator,create_shortcode
from.validators import validate_url,validate_dot_com

# Create your models here.

class rickUrl(models.Model):
    url=models.TextField()
    shortcode=models.CharField(max_length=20,unique=True,blank=True)

    def save(self,*args,**kwargs):
        if self.shortcode=='':
            self.shortcode = create_shortcode(self)
        super(rickUrl,self).save(*args,**kwargs)
    def __str__(self):
        return str(str(self.shortcode)+ " ===>> " + self.url)