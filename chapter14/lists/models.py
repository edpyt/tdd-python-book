from django.db import models
from django.urls import reverse


class Item(models.Model):
    text = models.TextField(default='', unique=True)
    list = models.ForeignKey('List', default=None, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.text

    class Meta:
        unique_together = ('list', 'text')


class List(models.Model):
    def get_absolute_url(self):
        return reverse('view_list', args=[self.id])
