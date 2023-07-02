from django.shortcuts import get_object_or_404, render, get_list_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import CardSectionData, MC_section, CardData, dt_section, CardDataDatasheet, Field, dt_Field
from django.core.cache import cache
from django.utils import timezone
from django.contrib import messages
from .forms import FileForm, CreateNewSection
from .models import File
import os
import json
import uuid
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Sum, Max
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.db.models import Q

# Import core libraries
import model_card_lib_v2 as mclib_v2
import datasheet as dt

# Create your views here.

def datacard_section(response, id):
    context = {}
    return render(response, "mc_and_datasheet/datacard_section.html", context)
def index(request):
    context = {}
    return render(request, "mc_and_datasheet/index.html", context)
def about(request):
    context = {}
    return render(request, "mc_and_datasheet/about.html", context)
def contact(request):
    context = {}
    return render(request, "mc_and_datasheet/contact.html", context)
def projects(request):
    context = {}
    return render(request, "mc_and_datasheet/projects.html", context)
def blog_home(request):
    context = {}
    return render(request, "mc_and_datasheet/blog-home.html", context)
def blog_post(request):
    context = {}
    return render(request, "mc_and_datasheet/blog-post.html", context)
def portfolio_overview(request):
    context = {}
    return render(request, "mc_and_datasheet/portfolio-overview.html", context)
def portfolio_item(request):
    context = {}
    return render(request, "mc_and_datasheet/portfolio-item.html", context)
def my_view(request):
    return render(request, 'mc_and_datasheet/my_template.html')

def generate_session_id():
    return str(uuid.uuid4())

    
def home(request):

    # Session key based on uuid library
    session_uuid = request.session.get('session_uuid')
    if not session_uuid:
        session_uuid = generate_session_id()
        request.session['session_uuid'] = session_uuid

        print(f"New Session ID for the user: {session_uuid}")
    print(f"Session ID for the user: {session_uuid}")

    # Get the session key
    session_key = request.session.session_key

    # Print the session key
    print(f"Session key: {session_key}")
    
    return render(request, "mc_and_datasheet/home.html")



def upload_file(response, id):

    fs = FileSystemStorage()

    
    section_instance = get_object_or_404(MC_section, id=id) # Actually this is get command you are doing QUERY
    section_list = get_list_or_404(MC_section) # Actually this is get command you are doing QUERY
    
    if response.method == 'POST':
        form = FileForm(response.POST, response.FILES)
        if form.is_valid():
            # Create the file instance
                file_instance = File() # From models 
                
                # Get the file from form in front end
                file = form.cleaned_data['file']
                print(file)

                # Save it to backend
                file_instance.file = file 
                file_instance.name = file.name
                file_instance.uploaded_at = timezone.now()
                file_instance.uploaded_section_id = section_instance.id
                #print(file_instance.name)
                #print(file_instance.uploaded_at)
                file_instance.save()
                #path = form.save()

                #filename = fs.save(file_instance.name, file_instance)
                
                #print(filename)

                # Get it from backend to use in front end
                file_objects = File.objects.all()
                
                print('You are returned to Filelist')
                
                is_files = True
                context = {
                    "section": section_instance,
                    "section_list": section_list,
                    "form": form,
                    "files": file_objects,
                    "is_files": is_files,
                    "file_instance": file_instance
                }

                return render(response, 'mc_and_datasheet/section.html', context)

    else:
        form = FileForm()
        
    context = {"section":section_instance,
    "section_list":section_list,
    'current_section_id': section_instance.id,
    #"field_answers":section_instance.field_answer
    "form":form
    }
    return render(response , "mc_and_datasheet/section.html",context)# The third attributes are actually variables that you can pass inside the html

def delete(request, id):

    session_key = request.session.session_key

    print('Info: everything is deleted. ')    
    CardSectionData.objects.all().delete()
    if 'delete_section' in request.GET:
        CardData.objects.all().delete()
        Field.objects.filter(mc_section__id=28, id__gt=36, field_session=session_key ).delete()
        Field.objects.filter(mc_section__id=30, id__gt=19, field_session=session_key ).delete()
        Field.objects.filter(mc_section__id=31, id__gt=22, field_session=session_key).delete()
        Field.objects.filter(mc_section__id=32, id__gt=25, field_session=session_key).delete()
        Field.objects.filter(mc_section__id=33, id__gt=29, field_session=session_key).delete()
        Field.objects.filter(mc_section__id=36, id__gt=35, field_session=session_key).delete()

        # Get all sections with id greater than 36
        sections_to_delete = MC_section.objects.filter(id__gt=36, mc_section_session=session_key)

        # Delete the field values
        Field.objects.filter(field_session=session_key).all().update(field_answer="")


        # Delete the sections
        num_deleted, _ = sections_to_delete.delete()

        # Reset the click count
        MC_section.objects.filter(session_key=session_key).update(click_count=0)

        print(f"{num_deleted} section has been deleted.")

        File.objects.all().delete()

        # Delete all the files as well

        file_directory = os.path.join(settings.MEDIA_ROOT, 'uploads')

        # Check if the directory exists
        if os.path.exists(file_directory):
            # Iterate over the files in the directory and delete them
            for file_name in os.listdir(file_directory):
                file_path = os.path.join(file_directory, file_name)
                os.remove(file_path)
        url = reverse('mc_and_datasheet:section', args=[28]) # You defined an app name so that should go in as well!

    if 'delete_dt_section' in request.GET:
        CardDataDatasheet.objects.all().delete()
        dt_Field.objects.filter(dt_section__id=1, id__gt=3).delete()
        dt_Field.objects.filter(dt_section__id=2, id__gt=19).delete()
        dt_Field.objects.filter(dt_section__id=3, id__gt=30).delete()
        dt_Field.objects.filter(dt_section__id=4, id__gt=33).delete()
        dt_Field.objects.filter(dt_section__id=5, id__gt=38).delete()
        dt_Field.objects.filter(dt_section__id=6, id__gt=44).delete()
        dt_Field.objects.filter(dt_section__id=7, id__gt=51).delete()
        url = reverse('mc_and_datasheet:dt_section', args=[id]) # You defined an app name so that should go in as well!
        # Delete the field values
        dt_Field.objects.all().update(field_answer="")

    return HttpResponseRedirect(url)


def section(response, id):

    session_id = response.session.session_key
    
    print('Session ID in Section:', session_id)
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
    #{"save":["save"],"c1":["clicked"]}

    
        
    if response.method == 'POST':
        
        form = FileForm()
        file_exists = File.objects.exists()
        # Get it from backend to use in front end
        file_objects = File.objects.all()
        
        input_text = response.POST.get('input_text')
        print(input_text)
        
        if 'sectionsubmit' in response.POST:
            
             
            
            print("here")
            text = response.POST['newsectiontext'] # get the input text from the form

            # Get the current click count
            click_count = MC_section.objects.aggregate(Sum('click_count'))['click_count__sum']
            click_count = click_count if click_count is not None else 0

            if len(text) > 1 and click_count < 2: # Only allow creation if the click count is less than 2
                print(f" this is the new section '{text}'")
                t = MC_section(name=text, click_count=1)
                t.save()

                # ID will be automaticly higher than the others
                newly_added_id = MC_section.objects.all().aggregate(Max('id'))['id__max'] or 0

                url = reverse('mc_and_datasheet:section', args=[newly_added_id]) # You defined an app name so that should go in as well!
                return HttpResponseRedirect(url)

            elif click_count == 2:
                print("here")
                
                # Read the HTML content from the file
                with open("mc_and_datasheet\error_text.html", "r") as file:
                    message_text = file.read()

                error_text = message_text.replace('An error occured. Do not FORGET to save the answers.', 'You can only add two new section. You can delete and add a new.')

                return HttpResponse(error_text, content_type="text/html")
        

        if response.POST.get('clear'): # send by the 'value'      
             
            for field in section_instance.field_set.filter(
        Q(field_session = session_id) | Q(field_session='')
        ).all():
                
                field.field_answer = ""
                field.save()
            
            context = {"section":section_instance,
            "section_list":section_list,
            }
            #'rbform':radiobutton_form}

            return render(response , "mc_and_datasheet/section.html",context)
            
            
            
        if response.POST.get("save"):
            section_answers = []
            
            for field in section_instance.field_set.filter(
        Q(field_session = session_id) | Q(field_session='')
        ).all():
                
                if field.field_question != "Select the metrics you want to include:":
                    answer_instance = response.POST.get("a" + str(field.id))
                    field.field_answer = answer_instance # save to database
                    section_answers.append(answer_instance) # also append the list

                    print(answer_instance)
                    field.save()

                else: # This is the 'select the metrics you want to include' field
                    accuracy = response.POST.getlist('accuracy')
                    precision = response.POST.getlist('precision')
                    mean_error = response.POST.getlist('mean-error')
                    selected_metrics = {"selected metrics":[accuracy,precision,mean_error]}
                    selected_metrics = json.dumps(selected_metrics)
                    #print(selected_metrics)
                    #field.field_answers = selected_metrics
                    section_answers.append(selected_metrics)
                
                

            # Send the data in order to be used to create model card   
            section2beadded = retrievedata(section_instance,section_instance.field_set.all(),section_answers)
            section2beadded = json.loads(section2beadded)

            # add session_id to the section2beadded in the beginning
            section2beadded['session_id'] = session_id

            # dump it back to json string
            section2beadded = json.dumps(section2beadded)


            #previous_saved_sections = []
            if CardData.objects.exists():
                
                print(" IT SEEMS CARD DATA IS POPULATED ALREADY NEW SECTION DATA WILL BE ADDED")
                
                card_instance = CardData.objects.latest('id')
                previous_saved_sections = card_instance.card_data
                psc_dict = json.loads(previous_saved_sections)
                s2a_dict = json.loads(section2beadded)
                combined_dict = {**psc_dict, **s2a_dict}
                combined_json_string = json.dumps(combined_dict) 
                CardData.objects.create(carddata_session =  response.session.session_key,
                                        card_data = combined_json_string,
                                        created_at = timezone.now()) 
            else:
                print(" IT SEEMS CARD DATA IS EMPTY POPULATING NOW")
                #print(section2beadded)
                CardData.objects.create(carddata_session = response.session.session_key,
                                        card_data = section2beadded,
                                        created_at = timezone.now())
                
            context = {"section":section_instance,
            "section_list":section_list,
            }
            #'rbform':radiobutton_form}

            return render(response , "mc_and_datasheet/section.html",context)
           # WITH CARDDATA YOU HAVE ALL THE INFORMATION TO CREATE THE MODEL CARD NEXT CREATE A BUTTON TO CREATE THE MODEL CARD 
           # THEN FROM THIS BUTTON A NEW VIEW OPENS WITH OPTIONS ABOUT FORMAT AND SO ON

        if response.POST.get("newfield"):
             
            txt = response.POST.get("newfieldtext")

            print(f"The new field :{txt}")

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
        print(form)
        #radiobutton_form = RadioButtons()
        print(" Method is not Post ")
        
    print(" YOU ARE RETURNED TO SECTION ")

      
    file_exists = File.objects.exists()
    # Get it from backend to use in front end
    file_objects = File.objects.all()
    
    print(f'{file_exists}')
    field_set = section_instance.field_set.filter(
        Q(field_session = session_id) | Q(field_session='')
        ).all()
    
    context = {"section":section_instance,
               "field_set":field_set,
               "section_list":section_list,
               'current_section_id': section_instance.id,
               "files": file_objects,
               "is_files": file_exists,
               "form":form
    }
    return render(response , "mc_and_datasheet/section.html",context)# The third attributes are actually variables that you can pass inside the html

def create(response): 

    if response.method == "POST":
        form = CreateNewSection(response.POST)
        if form.is_valid():
            n = form.cleaned_data["name"]
            print('n')
            t = MC_section(name=n)
            t.save()
        return HttpResponseRedirect("/mc_and_datasheet/%i"%t.id)
    else: # get

        form = CreateNewSection()

    return render(response, "mc_and_datasheet/create.html", {"form":form})

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
        
        #print(T[0]['value'])
        #print(type(T[0]['value']))

        t_return = T[0]['value']
    except TypeError:
        #print(T)
        #print(type(T))

        t_return = T

    # Delete existing CardSectionData object with the same key
    CardSectionData.objects.filter(key=name).delete()
    
    return t_return # json string
        
def file_list(request,id):


    form = FileForm()
    files = File.objects.all()
    file_name = form.file.upload_to
    files.name = file_name
    #print(files)
    section_instance = get_object_or_404(MC_section, id=id) # Actually this is get command you are doing QUERY
    section_list = get_list_or_404(MC_section) # Actually this is get command you are doing QUERY
               
    return render(request, 'mc_and_datasheet/filelist.html', {"section":section_instance,"section_list":section_list,'form': form,'files': files})

def datasheet_section(response,id):

    dtsection_instance = get_object_or_404(dt_section, id=id) # Actually this is get command you are doing QUERY
    dtsection_list = get_list_or_404(dt_section) # Actually this is get command you are doing QUERY
    #{"save":["save"],"c1":["clicked"]}
    #print(dtsection_instance.dt_field_set.all()) # this logging.infos all the field question as objects
    if response.method == "POST":
        print(" I am here you stooopid")
        
        if response.POST.get("save"):

            print(response.POST)

            section_answers = []
            
            for field in dtsection_instance.dt_field_set.all():
                # Iterate over the related dt_field objects

                asnwer_instance = response.POST.get("a" + str(field.id))
                field.field_answer = asnwer_instance # save to database
                section_answers.append(asnwer_instance) # also append the list
                field.save()

            
            # Send the data in order to be used to create model card   
            section2beadded = retrievedata(dtsection_instance,dtsection_instance.dt_field_set.all(),section_answers)

            print(section2beadded)
            if CardDataDatasheet.objects.exists():
                print(" IT SEEMS CARD DATA IS POPULATED ALREADY NEW SECTION DATA WILL BE ADDED")
                
                card_instance = CardDataDatasheet.objects.latest('id')
                previous_saved_sections = card_instance.card_data
                psc_dict = json.loads(previous_saved_sections)
                s2a_dict = json.loads(section2beadded)
                combined_dict = {**psc_dict, **s2a_dict}
                combined_json_string = json.dumps(combined_dict) 

                # Save the accumulated data to database 
                CardDataDatasheet.objects.create(
                card_data = combined_json_string,
                created_at = timezone.now()) 
            else:
                print(" IT SEEMS CARD DATA IS EMPTY POPULATING NOW")
                #print(section2beadded)

                CardDataDatasheet.objects.create(
                card_data = section2beadded,
                created_at = timezone.now())
                                            
        elif response.POST.get("newfield"):
             
            txt = response.POST.get("newfieldtext")

            if len(txt) > 2:
                dtsection_instance.dt_field_set.create(field_question = txt)
            else:
                print("invalid")
        
    print(" YOU ARE RETURNED TO DATASHEET SECTION ")

    context = {"section_questions": dtsection_instance.dt_field_set.all(),
               "section":dtsection_instance,
               "section_list":dtsection_list}
    return render(response , "mc_and_datasheet/dt_section.html",context)# The third attributes are actually variables that you can pass inside the html


def createoutput(request,id):

    if CardData.objects.exists():
        most_recent_entry = CardData.objects.latest('created_at')
        message_text = ""

        # Code to create model card
        with open("answer.json", "w") as outfile:
            outfile.write(most_recent_entry.get())

        model_card_dict = json.loads(most_recent_entry.get())

        fil_dict = {key: value for key, value in model_card_dict.items() if key.startswith("Section_Data")}
        #print(fil_dict)
        files = File.objects.all()

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
        
        
        try:
            if len(model_files) > 0:
                model_file = 'media/uploads' + '/' + model_files[-1]
            else:
                model_file = None

            if len(dataset_files) > 0:
                dataset_file = 'media/uploads' + '/' + dataset_files[-1]
            else:
                dataset_file = None

            if len(custom_metric_files) > 0:
                vis_metric_files = 'media/uploads' + '/' + custom_metric_files[-1]
            else:
                vis_metric_files = None

            if len(custom_dataset_files) > 0:
                vis_dataset_files = 'media/uploads' + '/' + custom_dataset_files[-1]
            else:
                vis_dataset_files = None

        except Exception as e:
            print(f"An error occurred: {e}")

        #vis_dataset_files = 'media/uploads' + '/' + custom_dataset_files[-1] 
        print('model file: {} dataset file: {} graph file/s {}'.format(model_file, dataset_file, [vis_metric_files,vis_dataset_files]))
        model_card = mclib_v2.create_model_card(csv_file = dataset_file,
                                                model_file = model_file,
                                                vis_metric_files = vis_metric_files,
                                                vis_dataset_files = vis_dataset_files,
                                                a_dict=fil_dict)
                                                

        # Get the HTML content as a string
        html_content = str(model_card)
        # Create an HttpResponse object with the HTML content
        response = HttpResponse(html_content, content_type="text/html")
        # Set the Content-Disposition header to prompt the user to save the file
        response["Content-Disposition"] = "attachment; filename=filename.html"

    else:
        # Read the HTML content from the file
        with open("mc_and_datasheet\error_text.html", "r") as file:
            message_text = file.read()
        
        response = HttpResponse(message_text, content_type="text/html")
        
    
    #print(model_card)

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
        print(fil_dict)

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