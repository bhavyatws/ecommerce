# Generated by Django 4.0.2 on 2022-03-14 06:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0011_item_image_url_alter_item_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='image_url',
        ),
    ]
