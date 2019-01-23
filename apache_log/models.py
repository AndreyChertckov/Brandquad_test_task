from django.db import models


class Log(models.Model):
    
    ip = models.GenericIPAddressField()
    date = models.DateTimeField()
    http_method = models.CharField(max_length=7)
    uri = models.CharField(max_length=500)
    status_code = models.CharField(max_length=3)
    response_size = models.IntegerField()
