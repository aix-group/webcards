from django.shortcuts import get_object_or_404, render, get_list_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import CardSectionData, MC_section, CardData, dt_section, CardDataDatasheet
from django.core.cache import cache
from django.utils import timezone
from django.contrib import messages
from .forms import FileForm, CreateNewSection, RadioButtons
from .models import File
import os
import json
from django.http import JsonResponse

# Import backend libraries
import model_card_lib_v2 as mclib_v2
import datasheet as dt

# Create your views here.

def delete(request, id):

    print('Info: everything is deleted. ')    
    CardSectionData.objects.all().delete()
    if 'delete_section' in request.GET:
        CardData.objects.all().delete()
        File.objects.all().delete()
        url = reverse('mc_and_datasheet:section', args=[id]) # You defined an app name so that should go in as well!

    if 'delete_dt_section' in request.GET:
        CardDataDatasheet.objects.all().delete()
        url = reverse('mc_and_datasheet:dt_section', args=[id]) # You defined an app name so that should go in as well!

    return HttpResponseRedirect(url)

def section(response, id):
    
    section_instance = get_object_or_404(MC_section, id=id) # Actually this is get command you are doing QUERY
    section_list = get_list_or_404(MC_section) # Actually this is get command you are doing QUERY
    #{"save":["save"],"c1":["clicked"]}

        
    if response.method == "POST":
        
        form = FileForm(response.POST, response.FILES)
        if form.is_valid():
            file_instance = File()
            file_objects = File.objects.all()
            file = form.cleaned_data['file']
            file_instance.name = file.name
            file_instance.uploaded_at = timezone.now()
            #print(file_instance.name)
            #print(file_instance.uploaded_at)
            #print(file_objects)
            file_instance.save()
            form.save()
            return render(response, 'mc_and_datasheet/filelist.html', {"section":section_instance,"section_list":section_list,'form': form,'files': file_objects})
        
        #if response.POST.get("form_view"):
        #    print(' I am inside the form view')
        #    return render(response, 'mc_and_datasheet/form_temp.html', {"section":section_instance}) 

        if response.POST.get("upload"):
            print(' I am inside the upload ')
            print(" YOU ARE RETURNED TO FILELIST ")
            return render(response, 'mc_and_datasheet/filelist.html', {"section":section_instance,"section_list":section_list,'form': form,'files': file_objects})
        
        #if response.POST.get("delete"):
#
        #    print(' YOU DELETED EVERYTHING ARE YOU OK?????? ')    
        #    CardData.objects.all().delete()
        #    CardSectionData.objects.all().delete()


        if response.POST.get("save"):

            
            section_answers = []
            
            for field in section_instance.field_set.all():
                
                if section_instance.id != 35:
                    field.field_answers = response.POST.get("a" + str(field.id))
                    section_answers.append(field.field_answers)

                else: 

                    
                    accuracy = response.POST.getlist('accuracy')
                    precision = response.POST.getlist('precision')
                    mean_error = response.POST.getlist('mean-error')
                    selected_metrics = {"selected gmetrics":[accuracy,precision,mean_error]}
                    selected_metrics = json.dumps(selected_metrics)

                    #print(selected_metrics)
                    #field.field_answers = selected_metrics
                    section_answers.append(selected_metrics)
                
                field.save()

            # Send the data in order to be used to create model card   
            section2beadded = retrievedata(section_instance,section_instance.field_set.all(),section_answers)
            #section2beadded = json.loads(section2beadded)

            #previous_saved_sections = []
            if CardData.objects.exists():
                
                print(" IT SEEMS CARD DATA IS POPULATED ALREADY NEW SECTION DATA WILL BE ADDED")
                
                card_instance = CardData.objects.latest('id')
                previous_saved_sections = card_instance.card_data
                psc_dict = json.loads(previous_saved_sections)
                s2a_dict = json.loads(section2beadded)
                combined_dict = {**psc_dict, **s2a_dict}
                combined_json_string = json.dumps(combined_dict) 
                CardData.objects.create(
                card_data = combined_json_string,
                created_at = timezone.now()) 
            else:
                print(" IT SEEMS CARD DATA IS EMPTY POPULATING NOW")
                #print(section2beadded)
                CardData.objects.create(
                card_data = section2beadded,
                created_at = timezone.now())
                
            context = {"section":section_instance,
            "section_list":section_list,
            }
            #'rbform':radiobutton_form}

            return render(response , "mc_and_datasheet/section.html",context)
           # WITH CARDDATA YOU HAVE ALL THE INFORMATION TO CREATE THE MODEL CARD NEXT CREATE A BUTTON TO CREATE THE MODEL CARD 
           # THEN FROM THIS BUTTON A NEW VIEW OPENS WITH OPTIONS ABOUT FORMAT AND SO ON

        elif response.POST.get("newfield"):
             
            txt = response.POST.get("newfieldtext")

            if len(txt) > 2:
                section_instance.field_set.create(field_question = txt)
            else:
                print("invalid")
                
    else:
        form = FileForm()
        #radiobutton_form = RadioButtons()
        print(" Method is not Post ")
        
    print(" YOU ARE RETURNED TO SECTION ")

    context = {"section":section_instance,
    "section_list":section_list,
    'current_section_id': section_instance.id}
    #'rbform':radiobutton_form}

    return render(response , "mc_and_datasheet/section.html",context)# The third attributes are actually variables that you can pass inside the html

def home(response):
    
    return render(response, "mc_and_datasheet/home.html")

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

    section_data, created = CardSectionData.objects.get_or_create(  key=name,   
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
        
        if response.POST.get("save"):

            section_answers = []
            
            for field in dtsection_instance.dt_field_set.all():
                
                field.field_answers = response.POST.get("a" + str(field.id))
                section_answers.append(field.field_answers)
                
                field.save()
            # print(section_answers)
            # Send the data in order to be used to create model card   
            section2beadded = retrievedata(dtsection_instance,dtsection_instance.dt_field_set.all(),section_answers)

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

message_text = str("""
            <!DOCTYPE html>
            <html>
            <head>
            	<title>My Dark Page</title>
            	<style>
            		body {
            			background-color: #282c34;
            			color: #fff;
            			font-family: Arial, sans-serif;
            			font-size: 16px;
            			line-height: 1.5;
            			margin: 0;
            			padding: 0;
            		}

            		.container {
            			display: flex;
            			flex-direction: column;
            			height: 100vh;
            			justify-content: center;
            			align-items: center;
            		}

            		.warning {
            			background-color: #d9534f;
            			border-radius: 4px;
            			box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.3);
            			color: #fff;
            			padding: 20px;
            			text-align: center;
            			width: 50%;
            		}

            		h1 {
            			font-size: 36px;
            			margin-top: 0;
            		}

            		p {
            			font-size: 24px;
            			margin-bottom: 0;
            		}
            	</style>
            </head>
            <body>
            	<div class="container">
            		<div class="warning">
            			<h1>Warning!</h1>
            			<p>An error occured. Do not FORGET to save the answers.</p>
            		</div>
            	</div>
            </body>
            </html>""")
def createoutput(request,id):

    if CardData.objects.exists():
        most_recent_entry = CardData.objects.latest('created_at')
        message_text = ""

        # Code to create model card
        with open("answer.json", "w") as outfile:
            outfile.write(most_recent_entry.get())

        model_card_dict = json.loads(most_recent_entry.get())

        fil_dict = {key: value for key, value in model_card_dict.items() if key.startswith("Section_Data")}
        print(fil_dict)
        files = File.objects.all()

        model_files = []
        dataseet_files = []
        graph_file = []

        for file in files:
            file_name = file.givename()
            if file_name[-3:] == 'pkl':
                model_files.append(file_name)
            if file_name[-3:] == 'csv':
                dataseet_files.append(file_name)
            else: 
                graph_file.append(file_name)

        try:
            model_file = os.getcwd() + '/' +  model_files[-1]   
            dataset_file = os.getcwd() + '/' +  dataseet_files[-1] 
        except:
            model_file = " No model file detected "
            dataset_file = " No dataset file detected "
            pass

        print('model file: {} dataset file: {}'.format(model_file,dataset_file))
        model_card = mclib_v2.create_model_card(dataset_file,model_file,fil_dict)

        # Get the HTML content as a string
        html_content = str(model_card)
        # Create an HttpResponse object with the HTML content
        response = HttpResponse(html_content, content_type="text/html")
        # Set the Content-Disposition header to prompt the user to save the file
        response["Content-Disposition"] = "attachment; filename=filename.html"

    else:
        error_text = message_text
        
        response = HttpResponse(error_text, content_type="text/html")
        
    
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