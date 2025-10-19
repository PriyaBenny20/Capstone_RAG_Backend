from django.db import models

# Create your models here.
from django.db import models

class Metadata(models.Model):
    metadataid = models.CharField(max_length=200, unique=True)
    region = models.CharField(max_length=200, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    extra = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.metadataid

class Document(models.Model):
    metadata = models.ForeignKey(Metadata, on_delete=models.CASCADE)
    chunk = models.TextField()

class Embedding(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    vector = models.JSONField()  
