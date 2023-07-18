from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import MC_section, Field, File, CardData  # import your models here
from utils.model_card_lib_v2 import create_model_card
import json
import pandas as pd
import pickle
import os
test_input = './test_input/'

class SectionViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        # setup the other necessary variables here

    def test_model_card_creation(self):
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
        
        _ , is_successful = create_model_card(a_dict=test_dict, 
                                 csv_file= test_df, 
                                 model_file= test_model, 
                                 vis_dataset_files=dataset_png, 
                                 vis_metric_files=metric_png, 
                                 section_names=section_names)   
        
        # Now you can check that the file exists
        self.assertTrue(is_successful)
        
        

       


