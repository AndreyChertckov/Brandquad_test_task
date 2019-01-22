from django.db import models


class Log(models.Model):
    
    ip = models.GenericIPAddressField()
    data = models.DateTimeField()
    http_method = models.CharField(max_length=7)
    uri = models.CharField(max_length=200)
    status_code = models.CharField(max_length=3)
    size_of_response = models.IntegerField()
