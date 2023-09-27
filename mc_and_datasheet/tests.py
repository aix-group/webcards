# Author: Bahadir Eryilmaz 
# Date: 30/09/2023
# Documentation: https://webcards.readthedocs.io/en/latest/index.html
# Desc: This file contains the tests of the application.


from django.test import TestCase, Client
from django.shortcuts import get_object_or_404, render, get_list_or_404, redirect
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from django.db.models import Q
from .models import MC_section, Field, File, CardData  
from .forms import FileForm
from utils.model_card_lib_v2 import create_model_card
from django.utils import timezone
from django.db.models import Sum, Max
from django.core.files import File as DjangoFile


import json
import pandas as pd
import pickle
import os
test_input = './test_input/'


class SectionViewTest(TestCase):
 
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        self.session = self.client.session
        self.session.expire_date = timezone.now() + timezone.timedelta(days=1)
        self.session.save()

        self.session_key = self.session.session_key


        # Creating initial section
        self.section = MC_section.objects.create(
            name='Test Section', 
            click_count=0, 
            section_desc='Test Section Description', 
            mc_section_session=self.session_key
        )

    def test_model_card_creation(self):

        """
            Tests the core library and backend model card library. 
            After customization if this tests passes, that means customization is successful.
        """
        print('Testing model card creation....')
        
        # open test json file and convert to dict
        with open(test_input + 'answer.json', 'r') as f:
            test_dict = json.load(f)
            
        with open(test_input + 'section_names.json', 'r') as f:
            section_names = json.load(f)
        
        # open the csv file and store it as df
        test_df = test_input + 'blood.csv'
        
        # open LogisticRegression.pkl file and store it as model
        test_model = test_input + 'LogisticRegression.pkl'
           
        # open example pngs
        dataset_png = test_input + 'cifar10_class_distribution.png'
        metric_png = test_input + 'W&B_Chart_05_06_2023_11_08_11.png'
          
        
        # create model card
        
        _ , is_successful, _ , _ = create_model_card(a_dict=test_dict, 
                                 csv_file= test_df, 
                                 model_file= test_model, 
                                 vis_dataset_files=dataset_png, 
                                 vis_metric_files=metric_png, 
                                 section_names=section_names)   
        
        # Now you can check that the file exists
        self.assertTrue(is_successful)
    
    
    def test_section_view_get_request(self):
        # Simulate a GET request to the section view
        response = self.client.get(reverse('mc_and_datasheet:section', args=[self.section.id]))
        
        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        
        # Check that the rendered template is the expected one
        self.assertTemplateUsed(response, 'mc_and_datasheet/section.html')

       
    def test_with_session(self):
            
        # Setting up post data
        post_data = {
            'sectionsubmit': "some value",
            'newsectiontext': 'New Section Text',
            'clear': 'some value',
            'save': 'some value',
            'newfield': 'some value',
            'newfieldtext': 'New Field Text',
        }
        # Making post request
        response = self.client.post(reverse('mc_and_datasheet:section', args=[self.section.id]), data=post_data)

        # Asserting response status code (You should replace 200 with the expected status code)
        self.assertEqual(response.status_code, 302)    

        new_section = MC_section.objects.get(name=post_data['newsectiontext'])
        self.assertIsNotNone(new_section)

        created_new_section = new_section.field_set.create(field_session = self.session_key,
                                                  field_question=post_data['newfieldtext'])
        self.assertIsNotNone(created_new_section)
    
    def test_createoutput(self):

        with open(test_input + 'answer.json', 'r') as f:
            json_string = f.read()
        
        CardData.objects.create(card_data=json_string, carddata_session=self.session_key) # Create a mock datacard
        
        most_recent_entry = CardData.objects.filter(carddata_session = self.session_key).latest('created_at')

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
        
        self.assertIsNotNone(fil_dict, "fil_dict should not be None")
        self.assertIsNotNone(section_names, "section_names should not be None")
        
        # open example pngs
        dataset_png_path = test_input + 'cifar10_class_distribution.png'
        metric_png_path = test_input + 'W&B_Chart_05_06_2023_11_08_11.png'

        # create File objects
        with open(dataset_png_path, 'rb') as f:
            dataset_png = File(file=DjangoFile(f), file_session=self.session_key, uploaded_section_id=34)
            dataset_png.save()

        with open(metric_png_path, 'rb') as f:
            metric_png = File(file=DjangoFile(f), file_session=self.session_key, uploaded_section_id=35)
            metric_png.save()

        # then you can query the File model as you originally did
        files = File.objects.filter(file_session=self.session_key).all()

        custom_metric_files = []
        custom_dataset_files = []
    
        for file in files:
            section_id = file.uploaded_section_id

       
            if section_id == 35:
                # quantitative analysis
                custom_metric_files.append(file.name)
            if section_id == 34:
                # dataset file
                custom_dataset_files.append(file.name)
        
        if len(custom_metric_files) > 0:
            vis_metric_files = 'media/uploads' + f'/{self.session_key}/' + custom_metric_files[-1]
        else:
            vis_metric_files = None
        if len(custom_dataset_files) > 0:
            vis_dataset_files = 'media/uploads' + f'/{self.session_key}/' + custom_dataset_files[-1]
        else:
            vis_dataset_files = None

        self.assertIsNotNone(vis_metric_files, "vis_metric_files should not be None")
        self.assertIsNotNone(vis_dataset_files, "vis_dataset_files should not be None")