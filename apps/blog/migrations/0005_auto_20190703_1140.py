# Generated by Django 2.1 on 2019-07-03 11:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20190703_1131'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['-created_time'], 'verbose_name': '文章', 'verbose_name_plural': '文章'},
        ),
        migrations.RemoveField(
            model_name='article',
            name='article_order',
        ),
    ]
