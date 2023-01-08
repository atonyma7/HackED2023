from django.contrib import admin

from reviews.models import Review


# Register your models here.
class ReviewAdmin(admin.ModelAdmin):
    search_fields = ['name', 'score', 'publication', 'date']
    list_display = ['name', 'score', 'publication', 'date']


admin.site.register(Review, ReviewAdmin)
