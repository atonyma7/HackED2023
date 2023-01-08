from django.db import models

# Create your models here.
class Review(models.Model):
    id = models.AutoField(unique=True, null=False,
                          blank=False, primary_key=True)    
    name = models.CharField("Name", max_length=240)
    score = models.PositiveIntegerField("Score")
    publication = models.CharField("Publication", max_length=20)
    date = models.DateField("Date",auto_now_add = True)

    def __str__(self):
        return self.name