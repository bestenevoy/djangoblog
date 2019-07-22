from django.contrib import admin
from django.db import models
from .models import Article, Category, Tag
from mdeditor.widgets import MDEditorWidget
# Register your models here.


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title','created_time','modified_time')
    #设置哪些字段可以点击进入编辑界面
    list_display_links = ('title',)
    filter_horizontal = ('tags',)
    formfield_overrides = {
        models.TextField: {'widget': MDEditorWidget}
    }
admin.site.register(Category)
admin.site.register(Tag)
