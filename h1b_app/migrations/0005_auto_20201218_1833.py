# Generated by Django 3.1.4 on 2020-12-18 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('h1b_app', '0004_auto_20201218_1831'),
    ]

    operations = [
        migrations.AddField(
            model_name='h1b',
            name='hours_per_week',
            field=models.CharField(default=0, max_length=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='h1b',
            name='salary',
            field=models.CharField(default=0, max_length=5),
            preserve_default=False,
        ),
    ]
