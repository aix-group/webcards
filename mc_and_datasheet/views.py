from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
#from django.template import loader
from .models import MC_section, Item
from django.views import generic
from django.utils import timezone
from .forms import CreateNewSection

# Create your views here.

def section(response, section_id):

    ls = get_object_or_404(MC_section, pk=section_id)
    #ls = MC_section.objects.get(id=section_id)

    return render( response , "mc_and_datasheet/section.html",{"ls":ls}) # The third attributes are actually variables that you can pass inside the html

def home(response):

    return render(response, "mc_and_datasheet/home.html", {})

def create(response):

    #if response.method == "POST":
    #    form = CreateNewSection(response.POST)
#
    #    if form.is_valid():
    #        n = form.cleaned_data["name"]
    #        print('n')
    #        t = MC_section(name=n)
    #        t.save()
#
    #    return HttpResponseRedirect("mc_and_datasheet/%i"%t.id)
    #else: # get
    form = CreateNewSection()


    return render(response, "mc_and_datasheet/create.html", {"form":form})


