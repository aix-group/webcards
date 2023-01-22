from django.contrib import admin

# Register your models here.

from .models import MC_section

#class ChoiceInline(admin.TabularInline):
#    model = Item
#    extra = 5


#class MC_sectionAdmin(admin.ModelAdmin):
#    fieldsets = [
#        ('Question Entry',   {'fields': ['question_text']}),
#        ('Date information', {'fields': ['pub_date'], 'classes':['collapse']}),
#    ]
#    inlines = [ChoiceInline]
#
#    list_display =  ('question_text', 'pub_date', 'was_published_recently')
#    list_filter = ['pub_date']
#    search_fields = ['question_text']

admin.site.register(MC_section)