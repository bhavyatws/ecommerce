# Generated by Django 4.0.2 on 2022-02-28 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='user_address',
            field=models.CharField(default='', max_length=50),
        ),
    ]