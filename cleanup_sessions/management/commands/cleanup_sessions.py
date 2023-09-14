# cleanup_sessions/management/commands/cleanup_sessions.py
from django.core.management.base import BaseCommand
from django.contrib.sessions.models import Session
from mc_and_datasheet.models import CardSectionData, MC_section, CardData, dt_section, CardDataDatasheet, Field, dt_Field, File  # Replace with your actual model imports
from django.utils import timezone
from django.conf import settings
from django.http import HttpRequest
from django.contrib.sessions.backends.db import SessionStore
import shutil
import os

class Command(BaseCommand):
    help = 'Cleanup session-related data'

    def handle(self, *args, **options):
        # Get all active session keys from the database
        active_session_keys = Session.objects.filter(expire_date__gt=timezone.now()).values_list('session_key', flat=True)

        for session_key in active_session_keys:
            try:
                #Clean the temp CardSectionData
                CardSectionData.objects.all().delete()
                
                ##Clean the Model Card data
                
                # Remove 'model_card_json' from the session
                request = HttpRequest()  # Create a new request object
                request.session = SessionStore(session_key=session_key)  # Load the session by session_key
                request.session.pop('model_card_json', None)  # Remove the 'model_card_json' key
                
                CardData.objects.all().delete()
                Field.objects.filter(mc_section__id=28, id__gt=36, field_session=session_key).delete()
                Field.objects.filter(mc_section__id=30, id__gt=19, field_session=session_key).delete()
                Field.objects.filter(mc_section__id=31, id__gt=22, field_session=session_key).delete()
                Field.objects.filter(mc_section__id=32, id__gt=25, field_session=session_key).delete()
                Field.objects.filter(mc_section__id=33, id__gt=29, field_session=session_key).delete()
                Field.objects.filter(mc_section__id=36, id__gt=35, field_session=session_key).delete()

                # Get all sections with id greater than 36
                MC_section.objects.filter(id__gt=36, mc_section_session=session_key).delete()

                # Delete the sections
                #num_deleted, _ = sections_to_delete.delete()

                # Delete the field values
                Field.objects.filter(field_session=session_key).all().update(field_answer="")

                # Reset the click count
                MC_section.objects.filter(mc_section_session=session_key).update(click_count=0)

                #print(f"{num_deleted} section has been deleted.")

                File.objects.all().delete()

                # Delete all the files as well
                session_key_directories = os.path.join(settings.MEDIA_ROOT, 'uploads')
            
                if os.path.exists(session_key_directories):
                    shutil.rmtree(session_key_directories)
                #Clean the Datasheet Card data
                
                CardDataDatasheet.objects.all().delete()
                dt_Field.objects.filter(dt_section__id=1, id__gt=3, field_session = session_key).delete()
                dt_Field.objects.filter(dt_section__id=2, id__gt=19, field_session = session_key).delete()
                dt_Field.objects.filter(dt_section__id=3, id__gt=30,field_session = session_key).delete()
                dt_Field.objects.filter(dt_section__id=4, id__gt=33,field_session = session_key).delete()
                dt_Field.objects.filter(dt_section__id=5, id__gt=38,field_session = session_key).delete()
                dt_Field.objects.filter(dt_section__id=6, id__gt=44,field_session = session_key).delete()
                dt_Field.objects.filter(dt_section__id=7, id__gt=51,field_session = session_key).delete()
            
                dt_Field.objects.filter(field_session=session_key).all().update(field_answer="")
                
                # Laslty clean the session itself
                request.session.flush()

                # Is there any data that is user-related but not get cleaned? Add it here!

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error while cleaning up session {session_key}: {str(e)}"))
            else:
                self.stdout.write(self.style.SUCCESS(f"Session {session_key} cleaned up successfully"))