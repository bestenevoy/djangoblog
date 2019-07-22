from django.db import models
from django.conf import settings

from mdeditor.fields import MDTextField
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.


# 文章分类
class Category(models.Model):
    name = models.CharField('博客分类', max_length=100)
    index = models.IntegerField(default=999, verbose_name='分类排序')

    class Meta:
        db_table = 'article_category'
        verbose_name = '文章-分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 文章标签
class Tag(models.Model):
    name = models.CharField('文章标签',max_length=100)
    class Meta:
        db_table = 'article_tag'
        verbose_name = '文章-标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 文章
class Article(models.Model):
    title = models.CharField('标题', max_length=70)
    # excerpt = models.TextField('摘要', max_length=200, blank=True)
    content = MDTextField()
    # content = RichTextUploadingField()
    # img = models.ImageField(upload_to='article_img/%Y/%m/%d/', verbose_name='文章图片', blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, verbose_name='作者')
    views = models.PositiveIntegerField('阅读量', default=0)
    # tui = models.ForeignKey(Tui, on_delete=models.DO_NOTHING, verbose_name='推荐位', blank=True, null=True)
    created_time = models.DateTimeField('发布时间', auto_now_add=True)
    modified_time = models.DateTimeField('修改时间', auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, verbose_name='分类', blank=True, null=True)
    tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True)

    class Meta:
        db_table = 'article'
        verbose_name = '文章'
        verbose_name_plural = '文章'
        ordering = ['-created_time'] # 按创建时间倒叙排列

    def __str__(self):
        return self.title