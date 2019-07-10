from django.db import models
from django.contrib.auth.models import AbstractUser, Group as GroupBase
# Create your models here.


class User(AbstractUser):
    nickname = models.CharField('昵称', max_length=100, blank=True,)
    last_mod_time = models.DateTimeField('修改时间', auto_now=True)

    class Meta(AbstractUser.Meta):
        ordering = ['-id']
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def get_nickname_or_username(self):
        if self.nickname:
            return self.nickname
        else:
            return self.username


class Group(GroupBase):
    pass
