from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# from store.models import Product #bad way

# Create your models here.

class Tag(models.Model):
    label = models.CharField(max_length=255)

class TaggedItem(models.Model):
    # What tag is applied to what obj
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    # product = models.ForeignKey(Product) #Bad way of implementation as tag app is dependent on the store app

    # Generic way to identify with (Type (Product, video, article) to find the table, ID to find the record)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveBigIntegerField() # only works for the tables with id as integers
    content_object = GenericForeignKey() # to read the actual object
