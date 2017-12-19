from django.db import models

# Create your models here.
genders = (
    ('m', 'männlich'),
    ('w', 'weiblich')
)


def get_default_teacher():
    Teacher.objects.get_or_create(first_name='Nicht zugewiesen', last_name='Nicht zugewiesen', gender='x',
                                  shortcode='XXX')


class Teacher(models.Model):
    title = models.CharField(max_length=10, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=genders)

    shortcode = models.CharField(max_length=3)

    def __str__(self):
        return self.title + ' ' + self.first_name + ' ' + self.last_name
