from django.contrib import admin
from . import models

class Head_Tag_Admin(admin.ModelAdmin):
	list_display = ('title','page_view_count','ip','belong_to_city','active','created_date')




# Register your models here.

admin.site.register(models.HeadTag,Head_Tag_Admin)
admin.site.register(models.City)
admin.site.register(models.Country)
admin.site.register(models.ViewRecord)