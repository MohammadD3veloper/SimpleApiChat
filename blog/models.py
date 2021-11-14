from django.db import models
from django.conf import settings


# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=20)
    image = models.ImageField(upload_to='news/images/')
    text = models.TextField(max_length=11000)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    date = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.title
