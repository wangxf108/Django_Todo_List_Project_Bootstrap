from django.contrib import admin
from .models import Todo


# 此处建立一个类，为了在admin页面中显示每个todo被建立的时间。将这个新建的类，添加到下面的admin中。
class TodoAdmin(admin.ModelAdmin):
    readonly_fields = ('created', ) 

admin.site.register(Todo, TodoAdmin)

