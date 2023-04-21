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

    def get_info(df,ID):
            index = df.index[df['ID'] == ID].tolist()[0]
            answer = df.at[index,'Answers']
            question = df.at[index,'Questions']
            return question, answer  


    # Create JSON
    # datasheet_dic = {
    #                 "motivation": {
    #                     get_info(datasheet,1)[0] : get_info(datasheet,1)[1],
    #                     get_info(datasheet,2)[0] : get_info(datasheet,2)[1],
    #                     get_info(datasheet,3)[0] : get_info(datasheet,3)[1],
    #                     get_info(datasheet,4)[0] : get_info(datasheet,4)[1]
    #                 }, # Motivation is closed
    #                 "composition" : {
    #                     get_info(datasheet,5)[0] : get_info(datasheet,5)[1],
    #                     get_info(datasheet,6)[0] : get_info(datasheet,6)[1],
    #                     get_info(datasheet,7)[0] : get_info(datasheet,7)[1],
    #                     get_info(datasheet,8)[0] : get_info(datasheet,8)[1],
    #                     get_info(datasheet,9)[0] : get_info(datasheet,9)[1],
    #                     get_info(datasheet,10)[0] : get_info(datasheet,10)[1],
    #                     get_info(datasheet,11)[0] : get_info(datasheet,11)[1],
    #                     get_info(datasheet,12)[0] : get_info(datasheet,12)[1],
    #                     get_info(datasheet,13)[0] : get_info(datasheet,13)[1],
    #                     get_info(datasheet,14)[0] : get_info(datasheet,14)[1],
    #                     get_info(datasheet,15)[0] : get_info(datasheet,15)[1],
    #                     get_info(datasheet,16)[0] : get_info(datasheet,16)[1],
    #                     get_info(datasheet,17)[0] : get_info(datasheet,17)[1],
    #                     get_info(datasheet,18)[0] : get_info(datasheet,18)[1],
    #                     get_info(datasheet,19)[0] : get_info(datasheet,19)[1],
    #                     get_info(datasheet,20)[0] : get_info(datasheet,20)[1],
    #                 }, # Composition is closed ( think that json file is really necessary )
    #                 "collection_process":{
    #                     get_info(datasheet,21)[0] : get_info(datasheet,21)[1],
    #                     get_info(datasheet,22)[0] : get_info(datasheet,22)[1],
    #                     get_info(datasheet,23)[0] : get_info(datasheet,23)[1],
    #                     get_info(datasheet,24)[0] : get_info(datasheet,24)[1],
    #                     get_info(datasheet,25)[0] : get_info(datasheet,25)[1],
    #                     get_info(datasheet,26)[0] : get_info(datasheet,26)[1],
    #                     get_info(datasheet,27)[0] : get_info(datasheet,27)[1],
    #                     get_info(datasheet,28)[0] : get_info(datasheet,28)[1],
    #                     get_info(datasheet,29)[0] : get_info(datasheet,29)[1],
    #                     get_info(datasheet,30)[0] : get_info(datasheet,30)[1],
    #                     get_info(datasheet,31)[0] : get_info(datasheet,31)[1]

    #                 }, # collection process is closed
    #                 "preprocessing_cleaning_labeling":{
                    
    #                     get_info(datasheet,32)[0] : get_info(datasheet,32)[1],
    #                     get_info(datasheet,33)[0] : get_info(datasheet,33)[1],
    #                     get_info(datasheet,34)[0] : get_info(datasheet,34)[1],
    #                     get_info(datasheet,35)[0] : get_info(datasheet,35)[1]
    #                 }, #preprocessing cleaning and labeling closed
    #                 "uses":{

    #                     get_info(datasheet,36)[0] : get_info(datasheet,36)[1],
    #                     get_info(datasheet,37)[0] : get_info(datasheet,37)[1],
    #                     get_info(datasheet,38)[0] : get_info(datasheet,38)[1],
    #                     get_info(datasheet,39)[0] : get_info(datasheet,39)[1],
    #                     get_info(datasheet,40)[0] : get_info(datasheet,40)[1],
    #                     get_info(datasheet,41)[0] : get_info(datasheet,41)[1]
    #                 },
    #                 "distribution":{

    #                     get_info(datasheet,42)[0] : get_info(datasheet,42)[1],
    #                     get_info(datasheet,43)[0] : get_info(datasheet,43)[1],
    #                     get_info(datasheet,44)[0] : get_info(datasheet,44)[1],
    #                     get_info(datasheet,45)[0] : get_info(datasheet,45)[1],
    #                     get_info(datasheet,46)[0] : get_info(datasheet,46)[1],
    #                     get_info(datasheet,47)[0] : get_info(datasheet,47)[1],
    #                     get_info(datasheet,48)[0] : get_info(datasheet,48)[1]
    #                 },
    #                 "maintenance":{
    #                     get_info(datasheet,49)[0] : get_info(datasheet,49)[1],
    #                     get_info(datasheet,50)[0] : get_info(datasheet,50)[1],
    #                     get_info(datasheet,51)[0] : get_info(datasheet,51)[1],
    #                     get_info(datasheet,52)[0] : get_info(datasheet,52)[1],
    #                     get_info(datasheet,53)[0] : get_info(datasheet,53)[1],
    #                     get_info(datasheet,54)[0] : get_info(datasheet,54)[1],
    #                     get_info(datasheet,55)[0] : get_info(datasheet,55)[1],
    #                     get_info(datasheet,56)[0] : get_info(datasheet,56)[1],
    #                 }
    # }
    # datasheet_json = json.dumps(datasheet_dic)
    #  # Write the data
    # with open('data.json','w') as f:
    #         f.write(datasheet_json)


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
    #with open("datasheet.html", "w", encoding="utf-8-sig") as file:
    #    file.write(html_string.format(table=html))
#
    #with open("datasheet.html", "r", encoding="utf-8-sig") as file:
    #    html_string = file.read()

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