from django.contrib import admin

from reviews.models import Review, Entity


# Register your models here.
class ReviewAdmin(admin.ModelAdmin):
    search_fields = ['entity_name', 'score', 'publication', 'date']
    list_display = ['entity_name', 'score', 'publication', 'date']

class EntityAdmin(admin.ModelAdmin):
    search_fields = ['name', 'metascore', 'img_src']
    list_display = ['name', 'metascore', 'img_src']



admin.site.register(Review, ReviewAdmin)
admin.site.register(Entity, EntityAdmin)


