# Generated by Django 5.0.3 on 2024-03-12 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym_products', '0004_alter_products_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='products',
            name='pdescription',
            field=models.TextField(blank=True, null=True),
        ),
    ]
