# Generated by Django 5.0.3 on 2024-03-12 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym_products', '0005_alter_products_id_alter_products_pdescription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]