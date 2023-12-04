from django.urls import path, include

from lists.views import home_page
from lists import urls as list_urls

urlpatterns = [
    path('', home_page, name='home'),
    path('lists/', include(list_urls))
]
