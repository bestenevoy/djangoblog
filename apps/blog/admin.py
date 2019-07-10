from django.contrib import admin
from .models import Article, Category, Tag
# Register your models here.


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title','created_time','modified_time')
    #设置哪些字段可以点击进入编辑界面
    list_display_links = ('title',)
    filter_horizontal = ('tags',)

admin.site.register(Category)
admin.site.register(Tag)
