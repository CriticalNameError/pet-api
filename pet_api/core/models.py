from django.db import models
from pet_api import settings


class Pets(models.Model):

    """Pet model to access via REST endpoint"""
    GENDER_CHOICES = (
        ('m', 'männlich'),
        ('w', 'weiblich'),
    )
    name = models.CharField(max_length=45, blank=True)
    species = models.CharField(max_length=45, blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=1, blank=True)
    birthday = models.DateField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "pets"

        if settings.IS_TESTING:
            managed = settings.IS_TESTING
            print('Pets model set to "managed = True" for testing!')
        else:
            managed = False
            print('Pets model set to "managed = False" for production!')
