from django.contrib import admin
from .models import Flock, Chick

@admin.register(Flock)
class FlockAdmin(admin.ModelAdmin):
    list_display = ('batch_number', 'farm', 'breed', 'arrival_date', 'quantity', 'current_stock')
    search_fields = ('batch_number', 'farm__name', 'breed__name')
    list_filter = ('breed', 'arrival_date')
    ordering = ('-arrival_date',)


@admin.register(Chick)
class ChickAdmin(admin.ModelAdmin):
    list_display = ('chicken_tag', 'hatch_date', 'number_of_chicks', 'source_incubation')
    search_fields = ('chicken__tag_number',)
    list_filter = ('hatch_date',)

    def chicken_tag(self, obj):
        return obj.chicken.tag_number
    chicken_tag.short_description = "Chicken Tag"
