from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
    title = models.CharField(max_length=100)
    memo = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  #加一个外键，使上述memo归属于特定用户

    def __str__(self):
        return self.title    #可以使，在后台admin管理页中显示不同的title，而不是统一的项目名称。
