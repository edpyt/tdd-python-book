from django.db import models


class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey('List', default=None, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.text


class List(models.Model):
    ...
