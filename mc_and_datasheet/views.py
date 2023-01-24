from django.shortcuts import get_object_or_404, render, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
#from django.template import loader
from .models import MC_section, Field
from django.views import generic
from django.utils import timezone
from .forms import CreateNewSection

# Create your views here.

def section(response, id):
    
    print(id)
    section_instance = get_object_or_404(MC_section, id=id) # Actually this is get command you are doing QUERY
    section_list = get_list_or_404(MC_section) # Actually this is get command you are doing QUERY
    print(section_instance.field_set.all())
    print(section_instance) # search django query commands
    # whatever you input as id will be shown and if you say id=id it is the last one
    #section_instance = MC_section.objects.get(id=id)
    
    #{"save":["save"],"c1":["clicked"]}
    if response.method == "POST":

        print(response.POST)

        if response.POST.get("save"):
            section_answers = []
            for field in section_instance.field_set.all():
                if response.POST.get("c" + str(field.id)) == "clicked":
                    field.complete = True
                    field.field_answers = response.POST.get("a" + str(field.id))
                    section_answers.append(field.field_answers)
                else:
                    field.complete = False
                field.save()
            print(section_answers)
        elif response.POST.get("newfield"):
             
            txt = response.POST.get("newfieldtext")

            if len(txt) > 2:
                section_instance.field_set.create(field_question = txt, complete=False)
            else:
                print("invalid")

    print(section_instance.field_set.all())
    return render(response , "mc_and_datasheet/section.html",{"section":section_instance,"section_list":section_list}) # The third attributes are actually variables that you can pass inside the html

def home(response):
    
    section_list = get_list_or_404(MC_section) # Actually this is get command you are doing QUERY
    
    
    print(type(section_list[0]))
    
    return render(response, "mc_and_datasheet/home.html", {"section_list":section_list})

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


