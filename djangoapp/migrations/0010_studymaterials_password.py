# Generated by Django 5.0.6 on 2024-07-09 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangoapp', '0009_visitcount'),
    ]

    operations = [
        migrations.AddField(
            model_name='studymaterials',
            name='password',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
