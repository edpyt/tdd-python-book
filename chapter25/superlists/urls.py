from django.urls import path, include

from lists.views import home_page

urlpatterns = [
    path('', home_page, name='home'),
    path('lists/', include('lists.urls')),
    path('accounts/', include('accounts.urls'))
]
