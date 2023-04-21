from django.contrib import admin

# Register your models here.

from .models import MC_section, Field,CardSectionData,CardData, File, dt_Field,dt_section

class FieldInline(admin.TabularInline):
    model = Field

@admin.register(MC_section)
class SectionAdmin(admin.ModelAdmin):
    inlines = [
        FieldInline,
    ]


class FieldInline(admin.TabularInline):
    model = dt_Field

@admin.register(dt_section)
class SectionAdmin(admin.ModelAdmin):
    inlines = [
        FieldInline,
    ]


#admin.site.register(MC_section)
admin.site.register(Field)
admin.site.register(CardSectionData)
admin.site.register(File)
admin.site.register(dt_Field)
admin.site.register(CardData)
