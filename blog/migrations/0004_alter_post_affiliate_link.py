# Generated by Django 5.0 on 2024-05-09 15:57

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_post_cover'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='affiliate_link',
            field=models.URLField(blank=True, help_text='Enter the URL of the affiliate link for this product', null=True, validators=[django.core.validators.URLValidator(schemes=['https'])], verbose_name='Affiliate Link'),
        ),
    ]
