# Generated by Django 3.1.4 on 2020-12-18 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='h1b',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ben_name', models.CharField(max_length=30)),
                ('ben_gender', models.CharField(max_length=2)),
                ('ben_addr', models.CharField(max_length=50)),
                ('nationality', models.CharField(max_length=20)),
                ('job_title', models.CharField(max_length=20)),
                ('employer_name', models.CharField(max_length=30)),
                ('occupation', models.CharField(max_length=20)),
                ('full_time_position', models.CharField(max_length=2)),
                ('location', models.CharField(max_length=20)),
                ('status', models.CharField(max_length=15)),
            ],
        ),
    ]