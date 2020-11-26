# Generated by Django 2.2.6 on 2020-11-10 12:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('category', models.CharField(choices=[('cat', 'Cat'), ('dog', 'Dog'), ('goldfish', 'Goldfish'), ('hamster', 'Hamster'), ('mouse', 'Mouse'), ('parrot', 'Parrot'), ('rabbit', 'Rabbit'), ('turtle', 'Turtle')], max_length=10)),
                ('breed', models.CharField(max_length=20)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=8)),
                ('age', models.SmallIntegerField()),
                ('description', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='PetPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='pets_photos')),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gallery.Pet')),
            ],
        ),
    ]