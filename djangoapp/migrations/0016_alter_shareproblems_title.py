# Generated by Django 3.2.25 on 2024-08-23 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangoapp', '0015_alter_shareproblems_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shareproblems',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]