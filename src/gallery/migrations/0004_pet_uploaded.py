# Generated by Django 2.2.6 on 2020-11-12 02:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0003_auto_20201112_0645'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet',
            name='uploaded',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]