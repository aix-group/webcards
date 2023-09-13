from django.contrib import admin
from .models import CardSectionData, MC_section, CardData, dt_section, CardDataDatasheet
from django.contrib.sessions.models import Session
from django.utils.html import format_html
# Register your models here.

from .models import MC_section, Field,CardSectionData,CardData, File, dt_Field,dt_section,UserInput


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

def display_session_keys(modeladmin, request, queryset):
    for session in queryset:
        session_data = session.get_decoded()
        keys = list(session_data.keys())
        session_keys = '<br>'.join(keys)
        modeladmin.message_user(
            request,
            format_html(f"Session keys for session {session.session_key}:<br>{session_keys}"),
        )

display_session_keys.short_description = "Display Session Keys"

class SessionAdmin(admin.ModelAdmin):
    list_display = ('session_key', 'expire_date')
    actions = [display_session_keys]

admin.site.register(Session, SessionAdmin)    



#admin.site.register(MC_section)
admin.site.register(Field)
admin.site.register(CardSectionData)
admin.site.register(File)
admin.site.register(dt_Field)
admin.site.register(CardDataDatasheet)
admin.site.register(UserInput)
admin.site.register(CardData)