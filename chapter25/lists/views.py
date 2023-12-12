import time
from typing import Optional

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import User
from lists.forms import ExistingListItemForm, ItemForm, NewListForm
from lists.models import List


def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)

    if request.method == 'POST':
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        
        if form.is_valid():
            form.save()
            return redirect(list_)
    return render(request, 'list.html', {'list': list_, 'form': form})


def new_list(request):
    form = NewListForm(data=request.POST)
    if form.is_valid():
        list_ = form.save(owner=request.user)
        return redirect(list_)
    return render(request, 'home.html', {'form': form})


def share_list(request, list_id: int):
    if request.method == 'POST':
        list_ = get_object_or_404(List, id=list_id)
        
        if request.user == list_.owner:
            user_append_email = request.POST.get('sharee')
            user = _get_user_or_add_messages(request, user_append_email)
            if user:
                list_.shared_with.add(user_append_email)
                list_.save()
            return redirect('view_list', list_id=list_id)
    return redirect('/')


def my_lists(request, email: str):
    owner = User.objects.get(email=email)
    return render(request, 'my_lists.html', {'owner': owner})


def _get_user_or_add_messages(request, user_email: str) -> Optional[User]:
    """Получить пользователя по email или добавить сообщение в messages"""
    try:
        return User.objects.get(email=user_email)
    except User.DoesNotExist:
        messages.error(request, 'Пользователь не найден!')
