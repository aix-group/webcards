import pandas as pd
import matplotlib.pyplot as plp
import numpy as np
import json
import platform
import os


def create_datasheet(dt_dict):
    print("CWD:%s" %(os.getcwd()))

    print("""


    *** Datasheet Program initialized.***

    - Output types: .JSON, .csv, .html


    """)
    id_list = []
    q_list = []
    answer_list = []
    for i in range(60):
         try:
              list_instance = get_answer(dt_dict,i)
              id_number = string_to_int(list_instance[0])
              id_list.append(id_number)
              question = drop_numbers(list_instance[0])
              q_list.append(question[1:])
              answer_list.append(list_instance[1])
         except:
              pass



    data_tuples = list(zip(id_list,q_list,answer_list)) # Make the table from three columns

    datasheet = pd.DataFrame(data_tuples, columns=['ID','Questions','Answers']) # Create the datasheet

    print("""

    Files are created. Please see the folder.


    """)

    datasheet['Answers'].replace('', np.nan, inplace=True) # Replace empty with nan

    datasheet.dropna(subset=['Answers'], inplace=True) #  Drop nan namely skipped questions

    # Export to csv 
    #datasheet.to_csv('datasheet.csv', index=False, encoding='utf-8-sig')


    # Export to html
    html = datasheet.to_html(index=False,classes='mystyle')
    html = html.replace("\\n","<br /><br />") # create the line breaks in html
    html = html.replace('\n','')
    style = '''
    <style>
        body {
          background-color: #2b2b2b;
          color: #e0e0e0;
          font-family: Arial, sans-serif;
        }
        table {
          border-collapse: collapse;
          margin: 20px;
          width: 80%;
        }
        th, td {
          padding: 12px;
          text-align: left;
        }
        th {
          background-color: #555;
        }
        tr:nth-child(even) {
          background-color: #444;
        }
        tr:hover {
          background-color: #666;
        }
       </style>
    
    
    
    '''
    pd.set_option('colheader_justify', 'center')
    html_string = '''
    <html>
      <head>
       <meta charset="UTF-8">
       <title>Datasheet Table</title>
        {}
      </head>
      <body>
        {}
      </body>
    </html>
    '''.format(style,html)

    return html_string

def get_answer(my_dict, id_to_get):
    boolean = False
    for entry in my_dict.values():
        for sub_dict in entry:
            key = str(list(sub_dict.keys())[0])
            value = str(list(sub_dict.values())[0])
            
            id_to_get = str(id_to_get)
            
            if key.startswith('{}_'.format(id_to_get)):
                boolean = True
                return [key,value]
            
    if boolean == False:
        return ""

def string_to_int(input_string):
    """
    Convert a string to an integer by removing all non-numeric characters.
    """
    digits = [char for char in input_string if char.isdigit()]  # Get all digits
    return int(''.join(digits))  # Join digits and convert to integer

def drop_numbers(input_string):
    """
    Remove all numeric characters from a string and return the resulting string.
    """
    return ''.join([char for char in input_string if not char.isdigit()])