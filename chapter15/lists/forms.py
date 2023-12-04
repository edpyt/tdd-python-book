from collections.abc import Mapping
from typing import Any, Optional
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList

from .models import Item, List

EMPTY_ITEM_ERROR = "You can't have an empty list item"
DUPLICATE_ITEM_ERROR = "You've already got this in your list"


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


class ExistingListItemForm(ItemForm):
    def __init__(self, for_list: List, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.instance.list = for_list

    def validate_unique(self) -> None:
        try:
            self.instance.validate_unique()
        except forms.ValidationError as e:
            e.error_dict = {'text': [DUPLICATE_ITEM_ERROR]}
            self._update_errors(e)
        return super().validate_unique()
