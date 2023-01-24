from django.shortcuts import get_object_or_404, render
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
    ls = get_object_or_404(MC_section, id=id) # Actually this is get command you are doing QUERY
    print(ls.field_set.all())
    print(ls) # search django query commands
    # whatever you input as id will be shown and if you say id=id it is the last one
    #ls = MC_section.objects.get(id=id)
    
    #{"save":["save"],"c1":["clicked"]}
    if response.method == "POST":

        print(response.POST)

        if response.POST.get("save"):
            for field in ls.field_set.all():
                if response.POST.get("c" + str(field.id)) == "clicked":
                    field.complete = True
                else:
                    field.complete = False
                field.save()

        elif response.POST.get("newfield"):
             
            txt = response.POST.get("newfieldtext")

            if len(txt) > 2:
                ls.field_set.create(field_question = txt, complete=False)
            else:
                print("invalid")


    return render(response , "mc_and_datasheet/section.html",{"ls":ls}) # The third attributes are actually variables that you can pass inside the html

def home(response):

    return render(response, "mc_and_datasheet/home.html", {})

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


