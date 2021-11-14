from django.db import models


# Create your models here.
class IpAddress(models.Model):
    ip_address = models.GenericIPAddressField()


class Blocklist(models.Model):
    ip_address = models.GenericIPAddressField()


