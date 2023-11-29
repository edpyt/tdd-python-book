from django.urls import path
from lists.views import add_item, home_page, new_list, view_list

urlpatterns = [
    path('', home_page, name='home'),
    path('lists/new', new_list, name='new_list'),
    path('lists/<int:list_id>/', view_list, name='view_list'),
    path('lists/<int:list_id>/add_item', add_item, name='add_item')
]
