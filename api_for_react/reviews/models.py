from django.db import models

# Create your models here.
class Review(models.Model):
    id = models.AutoField(unique=True, null=False,
                          blank=False, primary_key=True)    
    name = models.CharField("Name", max_length=250)
    score = models.PositiveIntegerField("Score")
    publication = models.CharField("Publication", max_length=250)
    date = models.DateField("Date",auto_now_add = True)
    img_src = models.CharField("Img_src", max_length=250)
    review_text = models.TextField("Review_text", default=' ')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'publication', 'review_text'], name='unique'
            )
        ]

    def __str__(self):
        return self.name