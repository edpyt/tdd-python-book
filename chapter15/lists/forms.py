from typing import Optional
from django import forms

from .models import Item, List

EMPTY_ITEM_ERROR = "You can't have an empty list item"


class ItemForm(forms.ModelForm):
    def save(self, for_list: List):
        self.instance.list = for_list
        return super().save()

    class Meta:
        model = Item
        fields = ('text',)
        widgets = {
            'text': forms.fields.TextInput(attrs={
                'placeholder': 'Enter a to-do item',
                'class': 'form-control input-lg'
            })
        }
        error_messages = {
            'text': {'required': EMPTY_ITEM_ERROR}
        }