from django.db import models

# Create your models here.
class Review(models.Model):
    name = models.CharField("Name", max_length=240)
    score = models.PositiveIntegerField("Score")
    publication = models.CharField("Publication", max_length=20)
    date = models.DateField("Date",auto_now_add = True)

    def __str__(self):
        return self.name