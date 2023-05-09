from django.contrib import admin
from .models import CardSectionData, MC_section, CardData, dt_section, CardDataDatasheet

# Register your models here.

from .models import MC_section, Field,CardSectionData,CardData, File, dt_Field,dt_section


class FieldInline(admin.TabularInline):
    model = Field
    list_display = ('id','field_question','field_answer','field_answer_date')
@admin.register(MC_section)
class SectionAdmin(admin.ModelAdmin):
    inlines = [
        FieldInline,
    ]
    list_display = ('id','name','field_ids')

    def field_ids(self, obj):
        return ', '.join(str(field.id) for field in obj.field_set.all())
    field_ids.short_description = 'Field IDs'

class dtFieldInline(admin.TabularInline):
    model = dt_Field
    list_display = ('id','field_question','field_answer','field_answer_date')

@admin.register(dt_section)
class SectionAdmin(admin.ModelAdmin):
    inlines = [
        dtFieldInline,
    ]
    list_display = ('id','name','field_ids')
    def field_ids(self, obj):
        return ', '.join(str(field.id) for field in obj.dt_field_set.all())
    field_ids.short_description = 'Field IDs'

    



#admin.site.register(MC_section)
admin.site.register(Field)
admin.site.register(CardSectionData)
admin.site.register(File)
admin.site.register(dt_Field)
admin.site.register(CardDataDatasheet)
admin.site.register(CardData)
