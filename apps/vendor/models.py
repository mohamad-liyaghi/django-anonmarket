from django.db import models


class Category(models.Model):

    parent = models.ForeignKey('self', default=None, null=True, blank=True, on_delete=models.SET_NULL,
                               related_name='children')

    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, max_length=120)

    def __str__(self):
        return self.title


class Country(models.Model):
    '''supported countries that vendors ship product to'''

    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, max_length=120)

    def __str__(self):
        return self.name