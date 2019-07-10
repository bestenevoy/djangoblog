from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from user.models import User


# Create your models here.
class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name='内容类型')
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id', )

    body = models.TextField('正文', max_length=300)
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE, verbose_name='评论人')
    root = models.ForeignKey('self', verbose_name='根评论', blank=True, null=True, related_name='rev_root_comment',
                             on_delete=models.CASCADE)
    parent = models.ForeignKey('self', verbose_name='父评论', null=True, blank=True, related_name='rev_parent_comment',
                               on_delete=models.CASCADE)

    created_time = models.DateTimeField('评论时间', auto_now_add=True)
    is_enable = models.BooleanField('选中显示', default=True, blank=False, null=False)

    def __str__(self):
        return f"{self.content_object}:{self.user}:{self.body}"

    def get_content(self):
        return f"{self.content_type}：{self.content_object}"

    class Meta:
        db_table = 'comment'
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        ordering = ['created_time']
