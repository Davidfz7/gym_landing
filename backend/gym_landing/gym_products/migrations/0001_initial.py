# Generated by Django 5.0.3 on 2024-03-12 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('pname', models.CharField(max_length=255)),
                ('pdescription', models.TextField()),
                ('pprice', models.DecimalField(decimal_places=2, max_digits=10)),
                ('pstock', models.IntegerField()),
            ],
            options={
                'db_table': 'products',
            },
        ),
    ]
