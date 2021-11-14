from django.db import models
from django.template.defaultfilters import slugify
from django.conf import settings


# Create your models here.
class Category(models.Model):
    parent = models.ForeignKey('self', related_name='child', 
                                    on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=25)
    interested_in = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                            related_name='liked_categories', null=True, blank=True)
    
    def __str__(self):
        return self.title


class Chat(models.Model):
    reply_to = models.ForeignKey('self', related_name='replied_to',
                                                on_delete=models.CASCADE, null=True, blank=True)   
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=25)
    text = models.TextField(max_length=11000)
    image = models.ImageField(upload_to='posts/images/', null=True, blank=True)
    category = models.ManyToManyField(Category, blank=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Chat, self).save(*args, **kwargs)