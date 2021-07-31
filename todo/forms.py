# 此处，为createtodo的页面，单独创建一个类，为了让画面能够显示出类Todo中title,memo,importan这三个conlium

from django.forms import ModelForm
from .models import Todo


class TodoForm(ModelForm):
    class Meta:
        model = Todo
        fields =['title', 'memo', 'important']