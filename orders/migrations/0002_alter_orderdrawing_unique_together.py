# Generated by Django 3.2 on 2022-06-18 09:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='orderdrawing',
            unique_together={('order', 'save_slot')},
        ),
    ]
