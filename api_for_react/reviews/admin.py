from django.contrib import admin

from reviews.models import Review, Entity, Userscore


# Register your models here.
class ReviewAdmin(admin.ModelAdmin):
    search_fields = ['entity_name', 'score', 'publication', 'date']
    list_display = ['entity_name', 'score', 'publication', 'date']

class EntityAdmin(admin.ModelAdmin):
    search_fields = ['name', 'metascore', 'img_src']
    list_display = ['name', 'metascore', 'img_src']


class UserscoreAdmin(admin.ModelAdmin):
    search_fields = ['entity', 'userscore']
    list_display = ['entity', 'userscore']

admin.site.register(Review, ReviewAdmin)
admin.site.register(Entity, EntityAdmin)
admin.site.register(Userscore, UserscoreAdmin)
