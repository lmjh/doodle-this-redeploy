# Generated by Django 3.2 on 2022-06-29 12:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('prints', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productvariant',
            name='sku',
            field=models.CharField(default=django.utils.timezone.now, max_length=120, unique=True),
            preserve_default=False,
        ),
    ]
