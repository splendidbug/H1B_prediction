# Generated by Django 3.1.4 on 2020-12-18 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('h1b_app', '0009_h1b_1_ben_dob'),
    ]

    operations = [
        migrations.AddField(
            model_name='h1b_1',
            name='is_uni',
            field=models.CharField(default=0, max_length=3),
            preserve_default=False,
        ),
    ]
