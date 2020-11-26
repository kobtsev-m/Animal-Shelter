from django.db import models
from django.utils import timezone
from django.urls import reverse


class Pet(models.Model):

    PETS_CH = [(p, p.title()) for p in [
        'cat', 'dog', 'goldfish', 'hamster', 'mouse',
        'parrot', 'rabbit', 'turtle'
    ]]
    GENDERS_CH = [(g, g.title()) for g in [
        'male', 'female'
    ]]

    name = models.CharField(max_length=20)
    category = models.CharField(max_length=10, choices=PETS_CH)
    breed = models.CharField(max_length=30, blank=True)
    gender = models.CharField(max_length=8, choices=GENDERS_CH)
    age = models.SmallIntegerField()
    description = models.CharField(max_length=150)
    uploaded = models.DateTimeField(auto_now_add=True)

    @property
    def get_absolute_url(self):
        return reverse('gallery:pet-detail', args=(self.pk,))

    def __str__(self):
        return self.name


class PetPhoto(models.Model):

    image = models.ImageField(upload_to='pets_photos', blank=True)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
