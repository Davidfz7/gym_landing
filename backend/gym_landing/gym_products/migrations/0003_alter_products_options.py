# Generated by Django 5.0.3 on 2024-03-12 18:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gym_products', '0002_rename_user_products'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='products',
            options={'managed': False},
        ),
    ]