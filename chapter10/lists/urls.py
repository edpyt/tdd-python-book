from django.urls import path
from lists.views import add_item, new_list, view_list

urlpatterns = [
    path('new', new_list, name='new_list'),
    path('<int:list_id>/', view_list, name='view_list'),
    path('<int:list_id>/add_item', add_item, name='add_item')
]
