
# Imports
import os
import json
from sklearn.model_selection import train_test_split
import sklearn.metrics 
import pickle
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
import pandas as pd
import logging

from PIL import Image
#import fitz  # For handling PDF files
import matplotlib.pyplot as plt  # For handling SVG files
from io import BytesIO
#import pywmf  # For handling WMF files


logging.basicConfig(filename='app.log', filemode='w', level=logging.INFO)

#os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

import model_card_toolkit as mctlib

def figure_to_base64str(fig):
    # convert figure to a base64 string
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    figdata_png = base64.b64encode(buf.getvalue()).decode('utf-8')

    return figdata_png

def create_model_card(csv_file = None,
                      model_file = None,
                      vis_metric_files = None,
                      vis_dataset_files = None,
                      a_dict= None,
                      section_names = None): # (as of moment only Dataframe)
    
    '''
    This function takes a dataset, a model and a split ratio from the user
    then creates a JSON and HTML file w.r.t given inputs. 
    
    df = DataFrame
    Model = any pickled model
    Split_ratio  = Float (0,1)
    
    '''
    #logging.info(get_answer(a_dict,41))
    #data_type = str(type(df)) # Determine the datatype 
    #split_ratio_per = [int(float(get_answer(a_dict,41))*100),int(1-float(get_answer(a_dict,41))*100)] # Percentages in list

    is_dataset_file = False
    is_model_file = False
    is_both_file = False
    
    print(f'Location of the dataset file: {csv_file}')
    
    #save a_dict to disk as answer.json
    with open('answer.json', 'w') as f:
        json.dump(a_dict, f)   
    
   

    # Check if the files are given
    if model_file and csv_file is not None:
        
        
        df =  pd.read_csv(csv_file)
        X = df.iloc[:,:-1] # Input nodes
        y = np.ravel(df.iloc[:,-1:]) # Output nodes

        # Create train and test set 
        ## TODO : add validation set as well
        X_train, X_test, y_train, y_test = train_test_split (X, y, 
                                                        train_size=float(get_answer(a_dict,44)),
                                                        shuffle=True)
        train_size_X = X_train.shape   
        test_size_X = X_test.shape

        is_dataset_file = True
        
        print('CSV file has been received')
        print('Model file has been received')
        
        with open(model_file,'rb') as file:
            model = pickle.load(file)
        # Fit the data
        
        model.fit(X_train, y_train)

        is_model_file = True
        
        
        y_pred = model.predict(X_test) # Predict using test set

        precision_score = sklearn.metrics.precision_score(y_test,y_pred) # take the precision 

        accuracy_score = model.score(X_test, y_test) # take the accuracy 

        mean_error_Score = sklearn.metrics.mean_squared_error(y_test,y_pred)

        is_both_file = True
    else:
        
        # User wanted to manually input the metrics

        dict_str = get_answer(a_dict,31)

        if len(dict_str)>2: 
            dict_metric = json.loads(dict_str)
            dict_metric = list(dict_metric.values())
            precision_score = float(dict_metric[0][1][0]) if dict_metric[0][1][0] else None
            accuracy_score = float(dict_metric[0][0][0]) if dict_metric[0][0][0] else None
            mean_error_score = float(dict_metric[0][2][0]) if dict_metric[0][2][0] else None

    # Make the HTML file
    model_card_output_path = os.getcwd() 

    mct = mctlib.ModelCardToolkit(model_card_output_path)


    model_card = mct.scaffold_assets() # Create model card object
    
    # Populate the model card

    ## MODEL DETAILS

    # Model name
    model_card.model_details.name = get_answer(a_dict,4)

    # Model Type but is shown as overview
    model_card.model_details.overview = get_answer(a_dict,5)
   
    model_card.model_details.owners = two_entry(mctlib.Owner,get_answer(a_dict,6),get_answer(a_dict,7))

    model_card.model_details.references = one_entry(mctlib.Reference,get_answer(a_dict,8))

    # Citation 
    try:
        style = get_answer(a_dict,9).split(',')[0]
        citation = get_answer(a_dict,9).split(',')[1]
        model_card.model_details.citations = two_entry(mctlib.Citation,style,citation)
    except IndexError:
        print('Citation not correct or entry not found. Please enter in the format: "style, citation"')

    # Version
    try:
        version = get_answer(a_dict,36)
        model_card.model_details.version.name = str(version)
        model_card.model_details.version.date = get_answer(a_dict,36)
    except IndexError:
        print('Version not correct or entry not found ')

    # License
    model_card.model_details.feedbacks = two_entry(mctlib.Feedback,get_answer(a_dict,10),get_answer(a_dict,10))

    #Feedback
    model_card.model_details.feedbacks = one_entry(mctlib.Feedback,get_answer(a_dict,11))

    ## CONSIDERATIONS

    model_card.considerations.sensitive = one_entry(mctlib.Sensitive, get_answer(a_dict,15))

    #print(one_entry(mctlib.Sensitive, get_answer(a_dict,15)))

    model_card.considerations.human_life = one_entry(mctlib.HumanLife, get_answer(a_dict,16))
    
    # Ethical Considerations
    model_card.considerations.ethical_considerations = two_entry(mctlib.Risk,get_answer(a_dict,18),get_answer(a_dict,17))

    model_card.considerations.fraught = one_entry(mctlib.Fraught, get_answer(a_dict,19))

    # Tradeoffs used as Additional ethical considerations
    #model_card.considerations.tradeoffs = one_entry(mctlib.Tradeoff, get_answer(a_dict,6)

    #Use Cases
    model_card.considerations.use_cases = one_entry(mctlib.UseCase, get_answer(a_dict,12))

    #Intented users
    model_card.considerations.users = one_entry(mctlib.User, get_answer(a_dict,13))
    
    # Out of Scope uses
    model_card.considerations.out_of_scope_uses = one_entry(mctlib.OosUses, get_answer(a_dict,14))

    ## FACTORS

    # Salient Factors
    model_card.factors.salient_factors = one_entry(mctlib.SalientFactor, get_answer(a_dict,21))

    # Reported factors
    model_card.factors.reported_factors = one_entry(mctlib.ReportedFactors, get_answer(a_dict,22))

    ## DATASET DETAILS
     
    model_card.dataset_details.used_datasets = two_entry(mctlib.UsedDataset,get_answer(a_dict,23),get_answer(a_dict,24))
    ## TODO What if user inputs one dataset but reasons as list?

    # Preprocessing
    model_card.dataset_details.preprocessing = one_entry(mctlib.Preprocessing, get_answer(a_dict,25))

    ## PERFORMANCE DETAILS

    # Reported Metrics
    model_card.performance_details.reported_metrics = one_entry(mctlib.ReportedMetrics, get_answer(a_dict,26))

    # Thresholds
    model_card.performance_details.thresholds = one_entry(mctlib.Threshold, get_answer(a_dict,27))

    metric_answer = get_answer(a_dict,31)

    #print("the metric answer is here {} ".format(metric_answer))

    ## TODO How are these metrics calculated does not work because logic is disabled. Implement a new logic for this.
    if get_answer(a_dict,31):
    
        if "accuracy" in metric_answer:
            accuracy_exp = "Values are predicted through predict method of the model."
            print(' Accuracy is selected')
        else:
            accuracy = None
        if "precision" in metric_answer:
            precision_exp = " Precision calculated using sklearn metrics precision score method with the predicted values."
            print(' Precision is selected')
        else:
            precision = None
        if "mean-error" in metric_answer:
            mean_error_exp = " Error_rate calculated using sklearn metrics mean squared error method with the predicted values."
            print(' Mean Error is selected')
        else:
            mean_error = None
        
        ## TODO activate this ones the logic is implemented.
        # This is will be automatic filled if the metric is chosen for reporting
        #model_card.performance_details.how_metrics = [mctlib.HowMetrics(accuracy = accuracy_exp,
        #                                                                precision = precision_exp,
        #                                                                error_rate = mean_error_exp)
        #                                                ]
    #
        model_card.performance_details.unitary_results  = one_entry(mctlib.UnitaryResults, get_answer(a_dict,28))
    
        model_card.performance_details.intersectional_results = one_entry(mctlib.IntersectionalResults, get_answer(a_dict,29))


    ## DATASET
    # integer to track dataset graph number
    dataset_graph_number = 0    
    
    if is_dataset_file:
        print('rendering the visualization for dataset taken from the csv file')
        fig, ax = plt.subplots()
        width = 0.75
        ax.bar(0, train_size_X , width, label='training set')
        ax.bar(1, test_size_X, width, label='testing set')
        ax.set_xticks(np.arange(2))
        ax.set_xticklabels(['training set', 'testing set'])
        ax.set_ylabel('Set Size')
        ax.set_xlabel('Sets')
        ax.set_title('Split ratio: %s' %(str(get_answer(a_dict,44))))
        set_size_barchart = figure_to_base64str(fig)
        #print(set_size_barchart)
        plt.close()

        """

        Title: get_answer(a_dict,38)
        Label: get_answer(a_dict,39)
        Description get_answer(a_dict,40)
        Dataset_size : get_answer(a_dict,41) 
        Split_ratio : get_answer(a_dict,44)   

        """
        model_card.model_parameters.data.append(mctlib.Dataset(
            name = get_answer(a_dict,38),
            description = get_answer(a_dict,40),
            ))
        if vis_dataset_files is not None:
            graph_dataset = read_image_as_base64(vis_dataset_files)
            print('rendering the visualization for dataset taken from the image file')
            
            model_card.model_parameters.data[dataset_graph_number].graphics.collection = [
            mctlib.Graphic(image=set_size_barchart),
            mctlib.Graphic(image=graph_dataset),
            ]
            #increment dataset_graph_number
            dataset_graph_number += 1
        else:
            model_card.model_parameters.data[dataset_graph_number].graphics.collection = [
            mctlib.Graphic(image=set_size_barchart),
            ]
            #increment dataset_graph_number
            dataset_graph_number += 1
                                                
    else:
        split_ratio = get_answer(a_dict,44)
        if len(split_ratio) > 2:
            print('rendering the visualization for dataset taken from user input')
            split_ratio = float(split_ratio)
            dataset_size = int(get_answer(a_dict,41))
            train_size_X = dataset_size*split_ratio
            test_size_X = dataset_size*float((1-split_ratio))

            fig, ax = plt.subplots()
            width = 0.75
            ax.bar(0, train_size_X , width, label='training set')
            ax.bar(1, test_size_X, width, label='testing set')
            ax.set_xticks(np.arange(2))
            ax.set_xticklabels(['training set', 'testing set'])
            ax.set_ylabel('Set Size')
            ax.set_xlabel('Sets')
            ax.set_title('Split ratio: %s' %(str(get_answer(a_dict,44))))
            set_size_barchart = figure_to_base64str(fig)
            plt.close()

            model_card.model_parameters.data.append(mctlib.Dataset(
            name = get_answer(a_dict,38),
            description = get_answer(a_dict,40),
            ))  
            
            model_card.model_parameters.data[dataset_graph_number].graphics.description = 'Description of the dataset'   
                    
            if vis_dataset_files is not None:
                graph_dataset = read_image_as_base64(vis_dataset_files)

                print('rendering the visualization for dataset taken from the image file')

                
                model_card.model_parameters.data[dataset_graph_number].graphics.collection = [
                mctlib.Graphic(image=set_size_barchart),
                mctlib.Graphic(image=graph_dataset),
                ]

                #increment dataset_graph_number
                dataset_graph_number += 1
            else:
                model_card.model_parameters.data[dataset_graph_number].graphics.collection = [
                mctlib.Graphic(image=set_size_barchart),
                ]
                #increment dataset_graph_number
                dataset_graph_number += 1

    ##QUANTITATIVE ANALYSIS 
    accuracy = None
    precision = None
    mean_error = None
    if 'accuracy_score' in locals() and accuracy_score is not None:
        accuracy = bytes(str(round(accuracy_score, 4)), 'utf-8')
    if 'precision_score' in locals() and precision_score is not None:
        precision = bytes(str(round(precision_score, 4)), 'utf-8')
    if 'mean_error_score' in locals() and mean_error_score is not None:
        mean_error = bytes(str(round(mean_error_score, 4)), 'utf-8')
    model_card.quantitative_analysis.performance_metrics = [
    mctlib.PerformanceMetric(type='Accuracy', value=accuracy, slice = None),
    mctlib.PerformanceMetric(type='Precision', value=precision, slice = None),
    mctlib.PerformanceMetric(type='Mean error', value=mean_error, slice = None),
    ]
    if vis_metric_files is not None:
        
        graph_metrics = read_image_as_base64(vis_metric_files)
        model_card.quantitative_analysis.graphics.description = (
        get_answer(a_dict,58))
        model_card.quantitative_analysis.graphics.collection = [
        mctlib.Graphic(name = 'Graph name', image=graph_metrics),
        ]

        # Unused model card path field used for description of the performance metrics
        model_card.model_details.path = get_answer(a_dict,57)
   

    ## CAVEATS AND RECOMMENDATIONS
    model_card.recommendations.further_testing = one_entry(mctlib.FurtherTesting, get_answer(a_dict,32))

    model_card.recommendations.relevant_groups = one_entry(mctlib.RelevantGroups, get_answer(a_dict,33))

    model_card.recommendations.additional_recommendations = one_entry(mctlib.AdditionalRecommendations, get_answer(a_dict,34))

    model_card.recommendations.ideal_characteristics = one_entry(mctlib.IdealCharacteristics, get_answer(a_dict,35))

    ## ANY CODE FOR CUSTOMIZED SECTION WILL COME HERE

    # TESTING THE CUSTOMIZED FIELDS

    # Model Details

    # Extract the IDs
    m_ids = customized_fields(0,a_dict)

    if m_ids != None or "":

        model_card.model_details.entry1 = one_entry(mctlib.ModelDetailsExt1,get_both(a_dict,m_ids[0])[1], get_both(a_dict,m_ids[0])[0])
        model_card.model_details.entry2 = one_entry(mctlib.ModelDetailsExt2,get_both(a_dict,m_ids[1])[1], get_both(a_dict,m_ids[1])[0])
        model_card.model_details.entry3 = one_entry(mctlib.ModelDetailsExt3,get_both(a_dict,m_ids[2])[1], get_both(a_dict,m_ids[2])[0])
        model_card.model_details.entry4 = one_entry(mctlib.ModelDetailsExt4,get_both(a_dict,m_ids[3])[1], get_both(a_dict,m_ids[3])[0])
        model_card.model_details.entry5 = one_entry(mctlib.ModelDetailsExt5,get_both(a_dict,m_ids[4])[1], get_both(a_dict,m_ids[4])[0])

    # Considerations

    # Extract the IDs
    c_ids = customized_fields(1,a_dict)

    if c_ids != None:
        if c_ids != []:

            model_card.considerations.entry1 = one_entry(mctlib.ConsiderationsExt1,get_both(a_dict,c_ids[0])[1],get_both(a_dict,c_ids[0])[0])
            model_card.considerations.entry2 = one_entry(mctlib.ConsiderationsExt2,get_both(a_dict,c_ids[1])[1],get_both(a_dict,c_ids[1])[0])
            model_card.considerations.entry3 = one_entry(mctlib.ConsiderationsExt3,get_both(a_dict,c_ids[2])[1],get_both(a_dict,c_ids[2])[0])
            model_card.considerations.entry4 = one_entry(mctlib.ConsiderationsExt4,get_both(a_dict,c_ids[3])[1],get_both(a_dict,c_ids[3])[0])
            model_card.considerations.entry5 = one_entry(mctlib.ConsiderationsExt5,get_both(a_dict,c_ids[4])[1],get_both(a_dict,c_ids[4])[0])

    # Factors

    # Extract the IDs
    f_ids = customized_fields(2,a_dict)

    if f_ids != None:
    
        model_card.factors.entry1 = one_entry(mctlib.FactorsExt1,get_both(a_dict,f_ids[0])[1], get_both(a_dict,f_ids[0])[0])
        model_card.factors.entry2 = one_entry(mctlib.FactorsExt2,get_both(a_dict,f_ids[1])[1], get_both(a_dict,f_ids[1])[0])
        model_card.factors.entry3 = one_entry(mctlib.FactorsExt3,get_both(a_dict,f_ids[2])[1], get_both(a_dict,f_ids[2])[0])
        model_card.factors.entry4 = one_entry(mctlib.FactorsExt4,get_both(a_dict,f_ids[3])[1], get_both(a_dict,f_ids[3])[0])
        model_card.factors.entry5 = one_entry(mctlib.FactorsExt5,get_both(a_dict,f_ids[4])[1], get_both(a_dict,f_ids[4])[0])

    # Dataset Details

    # Extract the IDs
    d_ids = customized_fields(3,a_dict)

    if d_ids != None:

        model_card.dataset_details.entry1 = one_entry(mctlib.DatasetDetailsExt1,get_both(a_dict,d_ids[0])[1], get_both(a_dict,d_ids[0])[0])
        model_card.dataset_details.entry2 = one_entry(mctlib.DatasetDetailsExt2,get_both(a_dict,d_ids[1])[1], get_both(a_dict,d_ids[1])[0])
        model_card.dataset_details.entry3 = one_entry(mctlib.DatasetDetailsExt3,get_both(a_dict,d_ids[2])[1], get_both(a_dict,d_ids[2])[0])
        model_card.dataset_details.entry4 = one_entry(mctlib.DatasetDetailsExt4,get_both(a_dict,d_ids[3])[1], get_both(a_dict,d_ids[3])[0])
        model_card.dataset_details.entry5 = one_entry(mctlib.DatasetDetailsExt5,get_both(a_dict,d_ids[4])[1], get_both(a_dict,d_ids[4])[0])

    # Performance Details

    # Extract the IDs
    p_ids = customized_fields(4,a_dict)

    if p_ids != None:

        model_card.performance_details.entry1 = one_entry(mctlib.PerformanceDetailsExt1,get_both(a_dict,p_ids[0])[1], get_both(a_dict,p_ids[0])[0])
        model_card.performance_details.entry2 = one_entry(mctlib.PerformanceDetailsExt2,get_both(a_dict,p_ids[1])[1], get_both(a_dict,p_ids[1])[0])
        model_card.performance_details.entry3 = one_entry(mctlib.PerformanceDetailsExt3,get_both(a_dict,p_ids[2])[1], get_both(a_dict,p_ids[2])[0])
        model_card.performance_details.entry4 = one_entry(mctlib.PerformanceDetailsExt4,get_both(a_dict,p_ids[3])[1], get_both(a_dict,p_ids[3])[0])
        model_card.performance_details.entry5 = one_entry(mctlib.PerformanceDetailsExt5,get_both(a_dict,p_ids[4])[1], get_both(a_dict,p_ids[4])[0])

    # Caveats and Recommendations

    # Extract the IDs
    r_ids = customized_fields(5,a_dict)

    if r_ids != None:

        model_card.recommendations.entry1 = one_entry(mctlib.RecommendationsExt1,get_both(a_dict,r_ids[0])[1], get_both(a_dict,r_ids[0])[0])
        model_card.recommendations.entry2 = one_entry(mctlib.RecommendationsExt2,get_both(a_dict,r_ids[1])[1], get_both(a_dict,r_ids[1])[0])
        model_card.recommendations.entry3 = one_entry(mctlib.RecommendationsExt3,get_both(a_dict,r_ids[2])[1], get_both(a_dict,r_ids[2])[0])
        model_card.recommendations.entry4 = one_entry(mctlib.RecommendationsExt4,get_both(a_dict,r_ids[3])[1], get_both(a_dict,r_ids[3])[0])
        model_card.recommendations.entry5 = one_entry(mctlib.RecommendationsExt5,get_both(a_dict,r_ids[4])[1], get_both(a_dict,r_ids[4])[0])

    # Extended Sections
    
    sorted_sections = get_section_name(section_names)
    #print(sorted_sections)

    ## Section 1
    ## Section Title
    if len(sorted_sections) > 0:
        section_name_1 = sorted_sections[0][3:]
        section_id_1 = sorted_sections[0][:2]
    else:
        section_name_1 = None
        section_id_1 = None
        
    model_card.extended_section1.extended1_title = [mctlib.Extended1Title(title=section_name_1)]

    ## Section fields
    for key, value in a_dict.items():
        # check if key has the section id 1 in it
        if key.split('_')[2] == str(section_id_1):
            section_list_1 = a_dict[key]

    #print(section_list_1)
    for i in range(10):
        if i < len(section_list_1):
            question = str(list(section_list_1[i].keys())[0]).split('_')[1]
            answer = list(section_list_1[i].values())[0]
            if i == 0:
                model_card.extended_section1.extended1_field1 = [mctlib.Extended1Field1(entry1= answer, question1 = question)]
            elif i == 1:
                model_card.extended_section1.extended1_field2 = [mctlib.Extended1Field2(entry2= answer, question2 = question)]
            elif i == 2:
                model_card.extended_section1.extended1_field3 = [mctlib.Extended1Field3(entry3= answer, question3 = question)]
            elif i == 3:
                model_card.extended_section1.extended1_field4 = [mctlib.Extended1Field4(entry4= answer, question4 = question)]
            elif i == 4:
                model_card.extended_section1.extended1_field5 = [mctlib.Extended1Field5(entry5= answer, question5 = question)]
            elif i == 5:
                model_card.extended_section1.extended1_field6 = [mctlib.Extended1Field6(entry6= answer, question6 = question)]
            elif i == 6:
                model_card.extended_section1.extended1_field7 = [mctlib.Extended1Field7(entry7= answer, question7 = question)]
            elif i == 7:
                model_card.extended_section1.extended1_field8 = [mctlib.Extended1Field8(entry8= answer, question8 = question)]
            elif i == 8:
                model_card.extended_section1.extended1_field9 = [mctlib.Extended1Field9(entry9= answer, question9 = question)]
            elif i == 9:
                model_card.extended_section1.extended1_field10 = [mctlib.Extended1Field10(entry10= answer, question10 = question)]

    ## Section 2
    ## Section Title
    if len(sorted_sections) > 1:
        section_name_2 = sorted_sections[1][3:]
        section_id_2 = sorted_sections[1][:3]
    else:
        section_name_2 = None
        section_id_2 = None
    model_card.extended_section2.extended2_title = [mctlib.Extended2Title(title=section_name_2)]

    ## Section fields
    for key, value in a_dict.items():
        # check if key has the section id 2 in it
        if key.split('_')[2] == str(section_id_1):
            section_list_2 = a_dict[key]

    for i in range(10):
        if i < len(section_list_2):
            question = str(list(section_list_2[i].keys())[0]).split('_')[1]
            answer = list(section_list_2[i].values())[0]
            if i == 0:
                model_card.extended_section2.extended2_field1 = [mctlib.Extended2Field1(entry1= answer, question1 = question)]
            elif i == 1:
                model_card.extended_section2.extended2_field2 = [mctlib.Extended2Field2(entry2= answer, question2 = question)]
            elif i == 2:
                model_card.extended_section2.extended2_field3 = [mctlib.Extended2Field3(entry3= answer, question3 = question)]
            elif i == 3:
                model_card.extended_section2.extended2_field4 = [mctlib.Extended2Field4(entry4= answer, question4 = question)]
            elif i == 4:
                model_card.extended_section2.extended2_field5 = [mctlib.Extended2Field5(entry5= answer, question5 = question)]
            elif i == 5:
                model_card.extended_section2.extended2_field6 = [mctlib.Extended2Field6(entry6= answer, question6 = question)]
            elif i == 6:
                model_card.extended_section2.extended2_field7 = [mctlib.Extended2Field7(entry7= answer, question7 = question)]
            elif i == 7:
                model_card.extended_section2.extended2_field8 = [mctlib.Extended2Field8(entry8= answer, question8 = question)]
            elif i == 8:
                model_card.extended_section2.extended2_field9 = [mctlib.Extended2Field9(entry9= answer, question9 = question)]
            elif i == 9:
                model_card.extended_section2.extended2_field10 = [mctlib.Extended2Field10(entry10= answer, question10 = question)]


    mct.update_model_card(model_card)
    
    # Return the model card document as an HTML page

    html = mct.export_format()

    #print("JSON and HTML files are created.")
    

    return html
    
def one_entry(object,entry,question=None):
    if entry:
        entries = entry.split('\r\n')
        len_entries= len(entries)

        if len_entries == 1:
            if question != None:
                return [object(entries[0],question)]
            else:
                return [object(entries[0])]
            
        elif len_entries == 2:
            if question != None:
                return [object(entries[0],question),object(entries[1])]
            else:

                return [object(entries[0]),object(entries[1])]
            
        elif len_entries == 3:
            if question != None:
                return [object(entries[0],question),object(entries[1]),object(entries[2])]
            else:

             return [object(entries[0]),object(entries[1]),object(entries[2])]

        elif len_entries == 4:

            if question != None:
                return [object(entries[0],question),object(entries[1]),object(entries[2]),object(entries[3])]
            else:
                return [object(entries[0]),object(entries[1]),object(entries[2]),object(entries[3])]

        elif len_entries == 5:
            if question != None:
                return [object(entries[0],question),object(entries[1]),object(entries[2]),object(entries[3]),object(entries[4])]
            else:

             return [object(entries[0]),object(entries[1]),object(entries[2]),object(entries[3]),object(entries[4])]

def two_entry(object,entry_1,entry_2):

    if entry_1:
        entries_1 = entry_1.split('\r')
        len_entries= len(entries_1)

    if entry_2:
        entries_2 = entry_2.split('\r')
        len_entries= len(entries_2)
    
        if len_entries == 1:

            return [object(entries_1[0],entries_2[0])]
        elif len_entries == 2:

            return [object(entries_1[0],entries_2[0]),object(entries_1[1],entries_2[1])]
        elif len_entries == 3:

            return [object(entries_1[0],entries_2[0]),object(entries_1[1],entries_2[1]),object(entries_1[2],entries_2[2])]

        elif len_entries == 4:

            return [object(entries_1[0],entries_2[0]),object(entries_1[1],entries_2[1]),object(entries_1[2],entries_2[2]),object(entries_1[3],entries_2[3])]

        elif len_entries == 5:

            return [object(entries_1[0],entries_2[0]),object(entries_1[1],entries_2[1]),object(entries_1[2],entries_2[2]),object(entries_1[3],entries_2[3]),object(entries_1[4],entries_2[4])]

def get_answer(my_dict, id_to_get):
    boolean = False
    for entry in my_dict.values():
        #logging.info(entry)
        for sub_dict in entry:
            key = str(list(sub_dict.keys())[0])
            value = str(list(sub_dict.values())[0])
            
            id_to_get = str(id_to_get)
            
            logging.info(key)
            logging.info(value)
            if key.startswith('{}_'.format(id_to_get)):
                boolean = True
                return value
            
    if boolean == False:
        return ""

def get_section_name(name_list):
    id_dict = {}
    for name in name_list:
        try: 
            id = int(name.split('_')[0])  # split the string by "_" and get the first part
        except ValueError:
            continue  # skip the non-integer IDs
        
        if id > 42: # New section
            id_dict[id] = name  # add the whole name (including ID) to the dict
          
    # Sort the id dict keys from smallest to largest and get their corresponding values
    sorted_sections = [id_dict[key] for key in sorted(id_dict.keys())]
    
    return sorted_sections
    

def get_both(my_dict, id_to_get):
    boolean = False
    for entry in my_dict.values():
        #logging.info(entry)
        for sub_dict in entry:
            key = str(list(sub_dict.keys())[0])
            value = str(list(sub_dict.values())[0])
            
            id_to_get = str(id_to_get)
            
            logging.info(key)
            logging.info(value)
            if key.startswith('{}_'.format(id_to_get)):
                boolean = True
                return [key[3:],value]
            
    if boolean == False:
        return ""

def customized_fields(ind,dict_a):    
    """
    model details:0
    considerations:1
    factors:2
    dataset details:3
    performance details:4
    caveats and recommendations:5
    
    """
    try:
        indicators = [['Section_Data_28',9],['Section_Data_30',9],['Section_Data_31',3],['Section_Data_32',4],['Section_Data_33',5],['Section_Data_36',5]]
        section_list = (dict_a[indicators[ind][0]])
        len_sec_list = len(section_list) 
        ext_list = section_list[indicators[ind][1]:len_sec_list]
        extracted_numbers = []

        for dict in ext_list:
            ext_question = list(dict.items())[0][0]
            extracted_numbers.append(ext_question[:2])
        
        if extracted_numbers == []:
            extracted_numbers = None
        return extracted_numbers
    except:
        extracted_numbers = None
        return extracted_numbers

def read_image_as_base64(image_path):
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()
        base64str = base64.b64encode(image_data).decode('utf-8')
        return base64str  
             
# UNNECESSARY FUNCTIONS DELETE BEFORE LAST RELEASE
def get_info(df,ID):
    index = df.index[df['ID'] == ID].tolist()[0]
    answer = df.at[index,'Answers']
    question = df.at[index,'Questions']
    return question, answer       

def check_user_input(input):
    try:
        # Convert it into float
        val = float(input)
    except ValueError:
         val = input # it is already string 
    return val           

#def get_answer(my_dict, id_to_get):
#    for sub_list in my_dict.values():
#        #logging.info(sub_list)
#        try:
#            for sub_sub_dict in sub_list:
#                #logging.info(sub_sub_dict)
#                #logging.info(sub_sub_dict.items())
#                for key, value in sub_sub_dict.items():
#                    #if id_to_get == 32:
#                    #logging.info(key)
#                    #logging.info(value)
#                    #logging.info('anan {}'.format(key))
#                    if key.startswith('{}_'.format(id_to_get)):
#                        return value
#                    elif isinstance(value, dict):
#                        result = get_answer(value, id_to_get)
#                        if result is not None:
#                            return result
#        except AttributeError:
#            pass
#    return ''

