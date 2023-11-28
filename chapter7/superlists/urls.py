from django.urls import path
from lists.views import home_page, new_list, view_list

urlpatterns = [
    path('', home_page, name='home'),
    path('lists/new', new_list, name='new_list'),
    path('lists/<int:id>/', view_list, name='view_list')
]
