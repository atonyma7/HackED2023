from django.db import models

# Create your models here.

class Entity(models.Model):
    id = models.AutoField(unique=True, null=False,
                          blank=False, primary_key=True)
    name = models.CharField("Name", max_length=250)
    metascore = models.PositiveIntegerField("Metascore")
    img_src = models.CharField("Img_src", max_length=250)
    
    def __str__(self):
        return self.name

class Review(models.Model):
    id = models.AutoField(unique=True, null=False,
                          blank=False, primary_key=True)    
    entity_name = models.CharField("Entity_name", max_length=250, default="")
    score = models.PositiveIntegerField("Score")
    publication = models.CharField("Publication", max_length=250)
    date = models.DateField("Date",auto_now_add = True)
    review_text = models.TextField("Review_text", default=' ')
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, default=None)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['entity_name', 'publication', 'review_text'], name='unique'
            )
        ]
class Userscore(models.Model):
    id = models.AutoField(unique=True, null=False,
                          blank=False, primary_key=True)
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, default=None)
    userscore = models.PositiveIntegerField("Userscore")

    