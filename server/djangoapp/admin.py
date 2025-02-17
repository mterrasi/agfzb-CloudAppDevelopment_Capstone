#path not working
#from server.djangoapp.models import CarMake, CarModel
from .models import CarMake, CarModel
from django.contrib import admin
from .models import CarMake, CarModel


# Register your models here.

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 1

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('model', 'name', 'dealer_id', 'type', 'year',)
    list_filter = ['type']
    search_fields = ['model', 'type']

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    list_display = ['name', 'description']
    list_filter = ['name']
    search_fields = ['name']

# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
