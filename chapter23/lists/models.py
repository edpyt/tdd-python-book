from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import models
from django.urls import reverse

User = get_user_model()


class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey('List', default=None, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.text

    class Meta:
        ordering = ('id',)
        unique_together = ('list', 'text')


class List(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    def get_absolute_url(self):
        res = reverse('view_list', args=[self.id])
        return res
    
    @staticmethod
    def create_new(first_item_text, owner=None):
        list_ = List.objects.create(owner=owner)
        Item.objects.create(text=first_item_text, list=list_)
        return list_

    @property
    def name(self):
        return self.item_set.first().text