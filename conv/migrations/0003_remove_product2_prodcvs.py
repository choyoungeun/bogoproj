# Generated by Django 2.2.4 on 2019-08-09 15:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('conv', '0002_product2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product2',
            name='prodCVS',
        ),
    ]
