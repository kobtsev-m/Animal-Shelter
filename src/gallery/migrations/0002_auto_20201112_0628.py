# Generated by Django 2.2.6 on 2020-11-11 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='breed',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
