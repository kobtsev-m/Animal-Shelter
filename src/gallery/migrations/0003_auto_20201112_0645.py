# Generated by Django 2.2.6 on 2020-11-11 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0002_auto_20201112_0628'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='description',
            field=models.CharField(max_length=150),
        ),
    ]