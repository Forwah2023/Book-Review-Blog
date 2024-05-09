# Generated by Django 5.0 on 2024-05-08 14:47

import django.core.validators
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bookmark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('genre', models.CharField(choices=[('SF', 'Science-Fiction'), ('NF', 'Non-Fiction'), ('TH', 'Thriller and Action'), ('HO', 'Horror'), ('RO', 'Romance'), ('CO', 'Comedy'), ('OT', 'Other'), ('FE', 'Featured')], max_length=2)),
                ('body', models.TextField()),
                ('summary', models.CharField(max_length=300)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('rating', models.PositiveIntegerField(blank=True, default=1, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('affiliate_link', models.URLField(blank=True, help_text='Enter the URL of the affiliate link for this product', null=True, verbose_name='Affiliate Link')),
            ],
            options={
                'permissions': [('is_blogger', 'Can create, read, update, and their posts')],
            },
        ),
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
    ]
