# Generated by Django 3.1.4 on 2021-11-05 17:32

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Description',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('long', models.TextField()),
                ('short', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Developer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount', models.CharField(max_length=10)),
                ('original', models.CharField(max_length=10)),
                ('discount_fmt', models.CharField(max_length=15)),
                ('original_fmt', models.CharField(max_length=15)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Specification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('min', models.TextField()),
                ('max', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=300, unique=True)),
                ('thumbnail', models.CharField(max_length=2000)),
                ('release_date', models.DateTimeField()),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('is_deleted', models.BooleanField(default=0)),
                ('store_url', models.TextField()),
                ('locale_code', models.CharField(max_length=20)),
                ('country_code', models.CharField(max_length=20)),
                ('description', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.description')),
                ('developers', models.ManyToManyField(to='core.Developer')),
                ('features', models.ManyToManyField(to='core.Feature')),
                ('genres', models.ManyToManyField(to='core.Genre')),
                ('pictures', models.ManyToManyField(to='core.Picture')),
                ('prices', models.ManyToManyField(to='core.Price')),
                ('publishers', models.ManyToManyField(to='core.Publisher')),
                ('specification', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.specification')),
                ('videos', models.ManyToManyField(to='core.Video')),
            ],
        ),
    ]
