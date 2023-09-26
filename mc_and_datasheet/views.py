# Author: Bahadir Eryilmaz 
# Date: 30/09/2023
# Documentation: https://webcards.readthedocs.io/en/latest/index.html
# Desc: This file contains the views of the application. The views are the functions that are called when a user makes a request to a URL.


# Import python libraries
import os
import json
import uuid

#Django imports
from django.shortcuts import get_object_or_404, render, get_list_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import CardSectionData, MC_section, CardData, dt_section, CardDataDatasheet, Field, dt_Field
from django.core.cache import cache
from django.utils import timezone
from django.contrib import messages
from .forms import FileForm, CreateNewSection
from .models import File
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Sum, Max
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.db.models import Q
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from django.contrib.sessions.models import Session
import model_card_toolkit as mctlib
import datetime

# Import core libraries
import utils.model_card_lib_v2 as mclib_v2
import utils.datasheet as dt



def impressum(response):
    return render(response, "mc_and_datasheet/impressum.html")

def legal(response):
    return render(response, "mc_and_datasheet/legal.html")

def about(response):
    return render(response, "mc_and_datasheet/about.html")

def contact(response):
    return render(response, "mc_and_datasheet/contact.html")

def datacard_section(response, id):
    context = {}
    return render(response, "mc_and_datasheet/datacard_section.html", context=context)

def generate_session_id():
    return str(uuid.uuid4())

def home(request):

    # Session key based on uuid library to trigger to session key creation for django (uuid is not really used in the tool)
    session_uuid = request.session.get('session_uuid')
    if not session_uuid:
        session_uuid = generate_session_id()
        request.session['session_uuid'] = session_uuid

        print(f"New Session uuid  for the user: {session_uuid}")
    print(f"Session uuid for the user: {session_uuid}")
    
    # You can later make use of the uuid session key

    # Get the session key
    session_key = request.session.session_key

    # Print the session key
    print(f"Session key: {session_key}")
    
    return render(request, "mc_and_datasheet/home.html")

def get_session_id(request):
    # Get the user's session key from the request (adjust this part as needed)
    user_session_key = request.session.session_key

    # Query the Session model to get the session object
    session = Session.objects.get(session_key=user_session_key)

    # Get the session ID from the session object
    session_id = session.session_key

    return session_id


def upload_file(response, id):
    
    session_key = response.session.session_key
    
    section_instance = get_object_or_404(MC_section, id=id) # Query the database to get the section instance
    section_list = get_list_or_404(MC_section) # Query the database to get the section list
    
    if response.method == 'POST':
        form = FileForm(response.POST, response.FILES)
        if form.is_valid():
            # Create the file instance
            file_instance = File(file_session=session_key)# From models 
            
            # Get the file from form in front end
            file = form.cleaned_data['file']

            # Create the file instance
            file_instance = File(file=file, name=file.name, uploaded_at=timezone.now(), uploaded_section_id=section_instance.id, file_session=session_key)
            
            # Specify the upload path relative to the media root
            file_path = f'uploads/{session_key}/{file_instance.name}'
       
            # Save the file
            
            fs = FileSystemStorage()
            fs.save(file_path, file)
            # Save the file instance
            file_instance.save()            

            url = reverse('mc_and_datasheet:section', args=[id]) # Don't forget to add the app name as well!
            return HttpResponseRedirect(url)

    else:
        form = FileForm()
    
    
    # PROBABLY PROGRAM NEVER COMES HERE
    context = {"section":section_instance,
    "section_list":section_list,
    'current_section_id': section_instance.id,
    "form":form
    }
    return render(response , "mc_and_datasheet/section.html",context)# The third attributes are actually variables that you can pass inside the html

def upload_json(response, id):
    
    session_key = response.session.session_key # Trigger it in case user does not have session key 
    
    if response.method == 'POST' and 'json_file' in response.FILES:
        json_file = response.FILES['json_file']
    
        # Save the uploaded file to a specific folder within your project
        storage = FileSystemStorage(location=settings.MEDIA_ROOT) 
        saved_json_file = storage.save(json_file.name, json_file)
        
        # Get the path of the saved file
        saved_file_path = os.path.join(settings.MEDIA_ROOT, saved_json_file)
        
        with open(saved_file_path, 'r') as f:
            model_card_json = json.load(f)
        
        # Store the model_card_json in session
        response.session['model_card_json'] = model_card_json
        os.remove(saved_file_path)
    
    url = reverse('mc_and_datasheet:section', args=[id]) # Don't forget to add the app name as well!
    return HttpResponseRedirect(url)   

# This is the delete command that user activates from the front end
def delete(request,id):

    session_key = request.session.session_key
        
    print('Info: everything is deleted. ')    
    CardSectionData.objects.all().delete()
    if 'delete_section' in request.GET:
        # Delete model_card_json from session after using it
        request.session.pop('model_card_json', None)   
        CardData.objects.all().delete()
        Field.objects.filter(mc_section__id=28, id__gt=36, field_session=session_key).delete()
        Field.objects.filter(mc_section__id=30, id__gt=19, field_session=session_key).delete()
        Field.objects.filter(mc_section__id=31, id__gt=22, field_session=session_key).delete()
        Field.objects.filter(mc_section__id=32, id__gt=25, field_session=session_key).delete()
        Field.objects.filter(mc_section__id=33, id__gt=29, field_session=session_key).delete()
        Field.objects.filter(mc_section__id=36, id__gt=35, field_session=session_key).delete()

        # Get all sections with id greater than 36
        MC_section.objects.filter(id__gt=36, mc_section_session=session_key).delete()

        # Delete the field values
        Field.objects.filter(field_session=session_key).all().update(field_answer="")

        # Reset the click count
        MC_section.objects.filter(mc_section_session=session_key).update(click_count=0)

        # Delete the file objects
        File.objects.all().delete()

        # Delete all the files as well
        file_directory = os.path.join(settings.MEDIA_ROOT, 'uploads', session_key)

        # Check if the directory exists
        if os.path.exists(file_directory):
            # Iterate over the files in the directory and delete them
            for file_name in os.listdir(file_directory):
                file_path = os.path.join(file_directory, file_name)
                os.remove(file_path)
            os.rmdir(file_directory)
                
        url = reverse('mc_and_datasheet:section', args=[28]) # Don't forget to add the app name as well!

    if 'delete_dt_section' in request.GET:
        CardDataDatasheet.objects.all().delete()
        dt_Field.objects.filter(dt_section__id=1, id__gt=3, field_session = session_key).delete()
        dt_Field.objects.filter(dt_section__id=2, id__gt=19,field_session = session_key).delete()
        dt_Field.objects.filter(dt_section__id=3, id__gt=30,field_session = session_key).delete()
        dt_Field.objects.filter(dt_section__id=4, id__gt=33,field_session = session_key).delete()
        dt_Field.objects.filter(dt_section__id=5, id__gt=38,field_session = session_key).delete()
        dt_Field.objects.filter(dt_section__id=6, id__gt=44,field_session = session_key).delete()
        dt_Field.objects.filter(dt_section__id=7, id__gt=51,field_session = session_key).delete()
        url = reverse('mc_and_datasheet:dt_section', args=[1]) # Don't forget to add the app name as well!
        # Delete the field values
        dt_Field.objects.filter(field_session=session_key).all().update(field_answer="")
    
    return HttpResponseRedirect(url)


def section(response, id):
    
     # Session key based on uuid library to trigger to session key creation for django (uuid is not really used in the tool)
    session_uuid = response.session.get('session_uuid')
    if not session_uuid:
        session_uuid = generate_session_id()
        response.session['session_uuid'] = session_uuid

        print(f"New Session uuid  for the user: {session_uuid}")
    print(f"Session uuid for the user: {session_uuid}")
    
    # You can later make use of the uuid session key

    # Get the session key
    session_key = response.session.session_key

    # Print the session key in yellow
    print(f"\033[93mSession key in section view: {session_key}\033[0m")

    model_card_json = response.session.get('model_card_json', None)        
        
    # Query the database with the session id
    section_instance = get_object_or_404(
    MC_section.objects.filter(
        Q(mc_section_session=response.session.session_key) | Q(mc_section_session='')
    ),
    id=id
    )
    section_list = get_list_or_404(
        MC_section.objects.filter(
        Q(mc_section_session=response.session.session_key) | Q(mc_section_session='')
    )
    )

       
    if response.method == 'POST':
        
        form = FileForm()

        # Get it from backend to use in front end
        file_objects = File.objects.filter(file_session = session_key).all()
        
        if 'sectionsubmit' in response.POST:             
            
            text = response.POST['newsectiontext'] # get the input text from the form

            # Get the current click count
            click_count = MC_section.objects.filter(Q(mc_section_session=response.session.session_key) | Q(mc_section_session='')).aggregate(Sum('click_count'))['click_count__sum']
            click_count = click_count if click_count is not None else 0

            if len(text) > 1 and click_count < 2: # Only allow creation if the click count is less than 2
                
                section_desc = "Here you can populate your newly created section with various headers. You can then present the corresponding descriptions. You can start by adding a new header below. Be aware that any text written in the question fields are presented as header for the description."
                new_section = MC_section(name=text, click_count=1, section_desc = section_desc, mc_section_session = session_key )
                new_section.save()

                # ID will be automaticly higher than the others
                newly_added_id = MC_section.objects.filter(
                Q(mc_section_session = session_key) | Q(mc_section_session='')).aggregate(Max('id'))['id__max'] or 0

                url = reverse('mc_and_datasheet:section', args=[newly_added_id]) # Don't forget to add the app name as well!
                return HttpResponseRedirect(url)

            elif click_count == 2:
                
                print(' User wants more than 2 additional section ')
                
                # Read the HTML content from the file
                with open("mc_and_datasheet\error_text.html", "r") as file:
                    message_text = file.read()

                section_error = message_text.replace('An error occurred. Do not FORGET to save the answers.', 'You can only add two new section. You can delete and add a new.')
                
                return HttpResponse(section_error, content_type="text/html")
        

        if response.POST.get('clear'): # send by the 'value'      
             
            for field in section_instance.field_set.all():
                
                field.field_answer = ""
                field.save()

            url = reverse('mc_and_datasheet:section', args=[id]) # Don't forget to add the app name as well!
            return redirect(url)
            
            
            
        if response.POST.get("save"):
            section_answers = []
            
            for field in section_instance.field_set.all():
                
                if field.field_question != "Select the metrics you want to include:":
                    if field.field_session == session_key or field.field_session == "":
                        answer_instance = response.POST.get("a" + str(field.id))
                        field.field_answer = answer_instance # save to database
                        section_answers.append(answer_instance) # also append the list

    

                else: # This is the 'select the metrics you want to include' field
                    accuracy = response.POST.getlist('accuracy')
                    precision = response.POST.getlist('precision')
                    brier_score = response.POST.getlist('brier-score')
                    recall = response.POST.getlist('recall')
                    f1_score = response.POST.getlist('f1-score')
                    auc_score = response.POST.getlist('auc-score')
                    selected_metrics = {"selected metrics":[accuracy,precision,brier_score,recall,f1_score,auc_score]}
                    selected_metrics = json.dumps(selected_metrics)
                    section_answers.append(selected_metrics)
                
                

            # Send the data in order to be used to create model card   
            section2beadded = retrievedata(section_instance,section_instance.field_set.all(),section_answers)
            section2beadded = json.loads(section2beadded)

            # add session_id to the section2beadded in the beginning
            section2beadded['session_id'] = session_key

            # dump it back to json string
            section2beadded = json.dumps(section2beadded)

            if CardData.objects.exists(): # Card data is already populated we add another section data to it
                
                card_instance = CardData.objects.latest('id')
                previous_saved_sections = card_instance.card_data
                psc_dict = json.loads(previous_saved_sections)
                s2a_dict = json.loads(section2beadded)
                combined_dict = {**psc_dict, **s2a_dict}
                combined_json_string = json.dumps(combined_dict) 
                CardData.objects.create(carddata_session =  response.session.session_key,
                                        card_data = combined_json_string,
                                        created_at = timezone.now()) 
            else: # Card data is not populated we create a new one
    
                CardData.objects.create(carddata_session = response.session.session_key,
                                        card_data = section2beadded,
                                        created_at = timezone.now())
                
            # After save answer redirect to the next section
            if id == 28:
               id = 30 # Next section id is 30
            elif id < 36: # If the section id is less than 36 then go to the next section
               id +=1
             
            url = reverse('mc_and_datasheet:section', args=[id]) # # Don't forget to add the app name as well!
            return redirect(url)

        if response.POST.get("newfield"): # Create the new field
             
            txt = response.POST.get("newfieldtext")

            if not txt:
                # Check if newfieldtext is in localStorage
                txt = response.POST.get("newfieldtext")

            if len(txt) > 2:             
                section_instance.field_set.create(field_session = response.session.session_key,
                                                  field_question=txt)
            else:
                print("invalid")
                
    else:
        form = FileForm()        
                
    file_exists = File.objects.exists()

    # Get it from backend to use in front end
    file_objects = File.objects.filter(file_session = session_key).all()
    
    field_set = section_instance.field_set.filter(
        Q(field_session = session_key) | Q(field_session='')
        ).all()
    
    # Handle the user answers automaticly shown in the fields ( this code also handles json upload )
    try:
        most_recent_entry = CardData.objects.filter(carddata_session = session_key).latest('created_at')
        most_recent_entry_data = most_recent_entry.card_data
        # convert the json string to dictionary
        most_recent_entry_data = json.loads(most_recent_entry_data)

        # Second security layer that no user can access other users data
        if most_recent_entry_data["session_id"] == session_key:
            print('The session key is the same')
            try:
                if model_card_json:
                    field_dicts = model_card_json[f'Section_Data_{section_instance.id}']
                else:
                    field_dicts = most_recent_entry_data[f'Section_Data_{section_instance.id}']
                
                print(field_dicts)
                for dict in field_dicts:
                    for key in dict:
                        if key.startswith("36"):
                            version_date = dict[key]

                if version_date:
                    print(version_date)
                else:
                    print("Version date not found.")    
                field_values = [''.join([str(val) if val is not None else "" for val in dict.values()]) for dict in field_dicts]

            except Exception as e_inner:
                print("Error inner:", e_inner)  # Print the inner exception
                if model_card_json:
                    field_dicts = model_card_json[f'Section_Data_{section_instance.id}']
                    field_values = [''.join(dict.values()) for dict in field_dicts]
                else:
                    length = len(field_set)
                    field_values = ["" for _ in range(length)]
                version_date = datetime.datetime.now().strftime("%Y-%m-%d")           
    except Exception as e_outer:
        print("Error outer:", e_outer)  # Print the outer exception
        if model_card_json:
            field_dicts = model_card_json[f'Section_Data_{section_instance.id}']
            field_values = [''.join(dict.values()) for dict in field_dicts]
        else:
            length = len(field_set)
            field_values = ["" for _ in range(length)]
        version_date = datetime.datetime.now().strftime("%Y-%m-%d")

    
    # Match the length of the field_values with the field_set so that loop counter in html would work    
    if len(field_values) != len(field_set):
        while len(field_values) < len(field_set):
            field_values.append("")

    context = {"section":section_instance,
               "field_set":field_set,
               "field_values":field_values,
               "version_date":version_date,
               "section_list":section_list,
               'current_section_id': section_instance.id,
               "files": file_objects,
               "is_files": file_exists,
               "form":form,
               "show_warning": show_warning,
               "warning_message" : "Warning: You did not click 'Save'. Please ensure you save your changes."
                } 
           
    return render(response , "mc_and_datasheet/section.html", context)# The third attributes are actually variables that you can pass inside the html!

# A subroutine the retrieves the data from the database and returns it as a json string
def retrievedata(section_name, field_questions, field_answers):

    name = section_name.givename()

    section_answer = []
        
    for i, entry in enumerate(field_answers):

        question = field_questions[i].givename()

        section_answer.append({question:entry})
    
    section_dict = {"Section_name_%s" %(section_name.id):name,
                    "Section_Data_%s"%(section_name.id):section_answer}
    section_json = json.dumps(section_dict)

    section_data, created = CardSectionData.objects.get_or_create(key=name,   
                                                                  value=section_json)
    
    if created:
        print("A new instance was created.")
    else:
        print("An existing instance was updated. That means same key used again.")

    try:

        T = CardSectionData.objects.get(key=name)
        T = T.value

    except CardSectionData.DoesNotExist:
        print("It does not exist")
    except CardSectionData.MultipleObjectsReturned:
        T = list(CardSectionData.objects.filter(key=name).values())
        T = T[-1:] # Get the most recent section entry

    try:
        t_return = T[0]['value']
    except TypeError:
        t_return = T

    # Delete existing CardSectionData object with the same key
    CardSectionData.objects.filter(key=name).delete()
    
    return t_return # json string       

# Same as the model card section but for datasheet
def datasheet_section(response,id):
    
     # Session key based on uuid library to trigger to session key creation for django (uuid is not really used in the tool)
    session_uuid = response.session.get('session_uuid')
    if not session_uuid:
        session_uuid = generate_session_id()
        response.session['session_uuid'] = session_uuid

        print(f"New Session uuid  for the user: {session_uuid}")
    print(f"Session uuid for the user: {session_uuid}")
    
    # You can later make use of the uuid session key

    # Get the session key
    session_key = response.session.session_key

    # Print the session key
    print(f"Session key: {session_key}")

    dtsection_instance = get_object_or_404(
    dt_section.objects.filter(
        Q(dt_section_session=response.session.session_key) | Q(dt_section_session='')
    ),
    id=id
    )
    dtsection_list = get_list_or_404(
        dt_section.objects.filter(
        Q(dt_section_session=response.session.session_key) | Q(dt_section_session='')
    )
    )

    if response.method == "POST":
        if response.POST.get("save"):
            section_answers = []
            
            for field in dtsection_instance.dt_field_set.all():
                # Iterate over the related dt_field objects

                asnwer_instance = response.POST.get("a" + str(field.id))
                field.field_answer = asnwer_instance # save to database
                section_answers.append(asnwer_instance) # also append the list
                field.save()

            
            # Send the data in order to be used to create model card   
            section2beadded = retrievedata(dtsection_instance,dtsection_instance.dt_field_set.all(),section_answers)

            section2beadded = json.loads(section2beadded)

            # add session_id to the section2beadded in the beginning
            section2beadded['session_id'] = session_key

            # dump it back to json string
            section2beadded = json.dumps(section2beadded)

            if CardDataDatasheet.objects.exists(): # Card data is already populated we add another section data to it
                
                card_instance = CardDataDatasheet.objects.latest('id')
                previous_saved_sections = card_instance.card_data
                psc_dict = json.loads(previous_saved_sections)
                s2a_dict = json.loads(section2beadded)
                combined_dict = {**psc_dict, **s2a_dict}
                combined_json_string = json.dumps(combined_dict) 

                # Save the accumulated data to database 
                CardDataDatasheet.objects.create(carddata_session =  response.session.session_key,
                                                card_data = combined_json_string,
                                                created_at = timezone.now()) 
            else: # Card data is not populated we create a new one

                CardDataDatasheet.objects.create(carddata_session = response.session.session_key,
                card_data = section2beadded,
                created_at = timezone.now())
                                            
        elif response.POST.get("newfield"):
             
            txt = response.POST.get("newfieldtext")

            if len(txt) > 2:
                dtsection_instance.dt_field_set.create(field_session = response.session.session_key,
                                                       field_question = txt)
            else:
                print("invalid")
    
    field_set = dtsection_instance.dt_field_set.filter(
     Q(field_session = session_key) | Q(field_session='')
     ).all()
    
    # Handle the user answers automaticly shown in the fields
    try:
        most_recent_entry = CardDataDatasheet.objects.filter(carddata_session = session_key).latest('created_at')
        
        most_recent_entry_data = most_recent_entry.card_data
        
        # convert the json string to dictionary
        most_recent_entry_data = json.loads(most_recent_entry_data)
    
        # Second security layer that no user can access other users data
        if most_recent_entry_data["session_id"] == session_key:
            try:
                field_dicts = most_recent_entry_data[f'Section_Data_{dtsection_instance.id}']
                field_values = [''.join(dict.values()) for dict in field_dicts]
            except:
                length = len(field_set)
                field_values = ["" for _ in range(length)]
    
    except:
        length = len(field_set)
        field_values = ["" for _ in range(length)]  

    context = {"section_questions": dtsection_instance.dt_field_set.all(),
               "section":dtsection_instance,
               "field_set":field_set,
               "field_values":field_values,
               'current_section_id': dtsection_instance.id,
               "section_list":dtsection_list}
    return render(response , "mc_and_datasheet/dt_section.html",context)# The third attributes are actually variables that you can pass inside the html

# Triggered when exporting the model card
def createoutput(request,id):
    
    session_key = request.session.session_key
    export_format = request.POST.get("format")

    if CardData.objects.exists():
        most_recent_entry = CardData.objects.filter(carddata_session = session_key).latest('created_at')
        message_text = ""

        # Code to create model card
        with open("answer.json", "w") as outfile:
            outfile.write(most_recent_entry.get())

        model_card_dict = json.loads(most_recent_entry.get())

        fil_dict = {}
        section_names = []

        for key, value in model_card_dict.items():
            if key.startswith("Section_Data"):
                fil_dict[key] = value
            else:
                section_names.append(f'{key[-2:]}_' + value)
        
        # save the section names to the current folder
        with open("section_names.json", "w") as outfile:
            json.dump(section_names, outfile)
        
        files = File.objects.filter(file_session = session_key ).all()

        model_files = []
        dataset_files = []
        custom_metric_files = []
        custom_dataset_files = []
    
        for file in files:
            section_id = file.uploaded_section_id

            file_name = file.name
            if file_name[-3:] == 'pkl':
                model_files.append(file_name)
            if file_name[-3:] == 'csv':
                dataset_files.append(file_name)
            else: 
                if section_id == 35:
                    # quantitative analysis
                    custom_metric_files.append(file_name)
                if section_id == 34:
                    # dataset file
                    custom_dataset_files.append(file_name)

        print(f'Custom Datasets : {custom_dataset_files}')
        print(f'Custom metric : {custom_metric_files}')
        
        
        if len(model_files) > 0:
            model_file = 'media/uploads' + f'/{session_key}/' + model_files[-1]
        else:
            model_file = None
        if len(dataset_files) > 0:
            dataset_file = 'media/uploads' + f'/{session_key}/' + dataset_files[-1]
        else:
            dataset_file = None
        if len(custom_metric_files) > 0:
            vis_metric_files = 'media/uploads' + f'/{session_key}/' + custom_metric_files[-1]
        else:
            vis_metric_files = None
        if len(custom_dataset_files) > 0:
            vis_dataset_files = 'media/uploads' + f'/{session_key}/' + custom_dataset_files[-1]
        else:
            vis_dataset_files = None

        # Print the file names
        print('\033[92mmodel file: {}\n'
              'dataset file: {}\n'
              'graph file/s: {}\033[0m'
              .format(model_file, dataset_file, [vis_metric_files, vis_dataset_files]))
        
        html_model_card, _, proto_model_card, json_model_card = mclib_v2.create_model_card(csv_file = dataset_file,
                                                model_file = model_file,
                                                vis_metric_files = vis_metric_files,
                                                vis_dataset_files = vis_dataset_files,
                                                a_dict=fil_dict,
                                                section_names = section_names,
                                                session_key = session_key)
        
        if export_format == "html":
            # Get the HTML content as a string
            html_content = str(html_model_card)
            # Create an HttpResponse object with the HTML content
            response = HttpResponse(html_content, content_type="text/html")

            # Set the Content-Disposition header to prompt the user to save the file
            response["Content-Disposition"] = "attachment; filename=filename.html"
           

        elif export_format == "proto":
            # Code to export as proto
            path_to_proto = os.path.join("model_card_output",session_key,"model_card.proto")
            with open(path_to_proto, "rb") as outfile:
                proto_model_card = outfile.read()
                
            os.remove(os.getcwd() + f'/model_card_output/{session_key}/model_card.proto')
            response = HttpResponse(proto_model_card,content_type="application/octet-stream")
            response["Content-Disposition"] = f"attachment; filename=my_model_card.proto"
          

        elif export_format == "json":
            json_model_card = str(json_model_card)
            # Code to export as JSON
            response = HttpResponse(json_model_card,content_type="application/json")
            response["Content-Disposition"] = f"attachment; filename=my_model_card.json"
           

    else:
        # User has not filled the form

        url = reverse('mc_and_datasheet:section', args=[id]) + "?from_createoutput=true"
        return redirect(url)
        

    
    return response

def datasheet_export(request,id):

    if CardDataDatasheet.objects.exists():
        most_recent_entry = CardDataDatasheet.objects.latest('created_at')
        message_text = ""

        # Code to create model card
        with open("answer_datasheet.json", "w") as outfile:
            outfile.write(most_recent_entry.get())

        model_card_dict = json.loads(most_recent_entry.get())

        fil_dict = {key: value for key, value in model_card_dict.items() if key.startswith("Section_Data")}
        #print(fil_dict)

        # Get the HTML content as a string
        html_content = dt.create_datasheet(fil_dict)
        # Create an HttpResponse object with the HTML content
        response = HttpResponse(html_content, content_type="text/html")
        # Set the Content-Disposition header to prompt the user to save the file
        response["Content-Disposition"] = "attachment; filename=filename.html"

    else:
        error_text = message_text
        
        response = HttpResponse(error_text, content_type="text/html")
        
    
    #print(model_card)

    return response


def clear_upon_day_end():
        
    print('Info: everything is deleted. ')    
    CardSectionData.objects.all().delete()
    
    CardData.objects.all().delete()
    Field.objects.filter(mc_section__id=28, id__gt=36).delete()
    Field.objects.filter(mc_section__id=30, id__gt=19).delete()
    Field.objects.filter(mc_section__id=31, id__gt=22).delete()
    Field.objects.filter(mc_section__id=32, id__gt=25).delete()
    Field.objects.filter(mc_section__id=33, id__gt=29).delete()
    Field.objects.filter(mc_section__id=36, id__gt=35).delete()
    # Get all sections with id greater than 36
    MC_section.objects.filter(id__gt=36).delete()
    
    # Delete the sections
    #num_deleted, _ = sections_to_delete.delete()
    # Delete the field values
    Field.objects.all().update(field_answer="")
    # Reset the click count
    MC_section.objects.update(click_count=0)
    #print(f"{num_deleted} section has been deleted.")
    File.objects.all().delete()
    # Delete all the files as well
    file_directory = os.path.join(settings.MEDIA_ROOT, 'uploads')
    # Check if the directory exists
    if os.path.exists(file_directory):
        # Iterate over the files in the directory and delete them
        for file_name in os.listdir(file_directory):
            file_path = os.path.join(file_directory, file_name)
            os.remove(file_path)
        os.remove(file_directory)
    
    CardDataDatasheet.objects.all().delete()
    dt_Field.objects.filter(dt_section__id=1, id__gt=3).delete()
    dt_Field.objects.filter(dt_section__id=2, id__gt=19).delete()
    dt_Field.objects.filter(dt_section__id=3, id__gt=30).delete()
    dt_Field.objects.filter(dt_section__id=4, id__gt=33).delete()
    dt_Field.objects.filter(dt_section__id=5, id__gt=38).delete()
    dt_Field.objects.filter(dt_section__id=6, id__gt=44).delete()
    dt_Field.objects.filter(dt_section__id=7, id__gt=51).delete()
    # Delete the field values
    dt_Field.objects.all().update(field_answer="")
    