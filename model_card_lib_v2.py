
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

def create_model_card(csv_file,model_file,a_dict): # (as of moment only Dataframe)
    
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

    # Read the CSV file
    if not isinstance(csv_file, str):
        df =  pd.read_csv(csv_file)
        X = df.iloc[:,:-1] # Input nodes
        y = np.ravel(df.iloc[:,-1:]) # Output nodes

        # Create train and test set
        X_train, X_test, y_train, y_test = train_test_split (X, y, 
                                                        train_size=float(get_answer(a_dict,44)),
                                                        shuffle=True)

        #X
        train_size_X = X_train.shape   
        test_size_X = X_test.shape

        is_dataset_file = True

    #Unpickle the model
    if not isinstance(model_file, str):
        with open(model_file,'rb') as file:
            model = pickle.load(file)
        # Fit the data
        model.fit(X_train, y_train)

        is_model_file = True
    
    print(a_dict)


               
    # Extract the metrics ( extendable )
    if not isinstance(model_file, str) or not isinstance(csv_file, str):
        y_pred = model.predict(X_test) # Predict using test set

        precision_score = sklearn.metrics.precision_score(y_test,y_pred) # take the precision 

        accuracy_score = model.score(X_test, y_test) # take the accuracy 

        mean_error_Score = sklearn.metrics.mean_squared_error(y_test,y_pred)

        is_both_file = True
    else:

        dict_str = get_answer(a_dict,31)
        dict_metric = json.loads(dict_str)
        dict_metric = list(dict_metric.values())
        precision_score = float(dict_metric[0][1][0])
        accuracy_score = float(dict_metric[0][0][0])
        mean_error_Score = float(dict_metric[0][2][0])

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
        print('Citation not correct or entry not found')

    # Version
    try:
        version = get_answer(a_dict,36)
        model_card.model_details.version.name = str(version)
        model_card.model_details.version.date = get_answer(a_dict,36)
    except IndexError:
        print('Version not correct or entry not found')

    # License
    model_card.model_details.feedbacks = two_entry(mctlib.Feedback,get_answer(a_dict,10),get_answer(a_dict,10))

    #Feedback
    model_card.model_details.feedbacks = one_entry(mctlib.Feedback,get_answer(a_dict,11))

    ## CONSIDERATIONS

    model_card.considerations.sensitive = one_entry(mctlib.Sensitive, get_answer(a_dict,15))

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

    print("the metric answer is here {} ".format(metric_answer))

    if get_answer(a_dict,31):
    
        if "accuracy" in metric_answer:
            accuracy = "Values are predicted through predict method of the model."
            print(' Accuracy is selected')
        else:
            accuracy = None
        if "precision" in metric_answer:
            precision = " Precision calculated using sklearn metrics precision score method with the predicted values."
            print(' Precision is selected')
        else:
            precision = None
        if "mean-error" in metric_answer:
            mean_error = " Error_rate calculated using sklearn metrics mean squared error method with the predicted values."
            print(' Mean Error is selected')
        else:
            mean_error = None
        
        # This is will be automatic filled if the metric is chosen for reporting
        model_card.performance_details.how_metrics = [mctlib.HowMetrics(accuracy = accuracy,
                                                                        precision = precision,
                                                                        error_rate = mean_error)
                                                        ]
    
        model_card.performance_details.unitary_results  = one_entry(mctlib.UnitaryResults, get_answer(a_dict,28))
    
        model_card.performance_details.intersectional_results = one_entry(mctlib.IntersectionalResults, get_answer(a_dict,29))


    ## DATASET
    if 'is_dataset_file' not in locals():

        split_ratio = float(get_answer(a_dict,44))
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

        model_card.model_parameters.data.append(mctlib.Dataset())
        model_card.model_parameters.data[0].graphics.collection = [
        mctlib.Graphic(name='Validation Set Size', image=set_size_barchart),
        ]

    # Set Size Bar Chart

    if 'is_dataset_file' in locals():
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
        print(set_size_barchart)
        plt.close()

        """

        Title: get_answer(a_dict,38)
        Label: get_answer(a_dict,39)
        Description get_answer(a_dict,40)
        Split_ratio : get_answer(a_dict,41)   


        """

        model_card.model_parameters.data.append(mctlib.Dataset())
        model_card.model_parameters.data[0].graphics.collection = [
        mctlib.Graphic(name='Validation Set Size', image=set_size_barchart),
        ]

    ##QUANTITATIVE ANALYSIS 

   
    accuracy =bytes(str(round(accuracy_score, 4)), 'utf-8')
    Precision =bytes(str(round(precision_score, 4)), 'utf-8')
    Mean_error =bytes(str(round(mean_error_Score, 4)), 'utf-8')
    
    model_card.quantitative_analysis.performance_metrics = [
    mctlib.PerformanceMetric(type='Accuracy', value=accuracy, slice = None),
    mctlib.PerformanceMetric(type='Precision', value=Precision, slice = None),
    mctlib.PerformanceMetric(type='Mean error', value=Mean_error, slice = None),
    ]

    ## CAVEATS AND RECOMMENDATIONS
    model_card.recommendations.further_testing = one_entry(mctlib.FurtherTesting, get_answer(a_dict,32))

    model_card.recommendations.relevant_groups = one_entry(mctlib.RelevantGroups, get_answer(a_dict,33))

    model_card.recommendations.additional_recommendations = one_entry(mctlib.AdditionalRecommendations, get_answer(a_dict,34))

    model_card.recommendations.ideal_characteristics = one_entry(mctlib.IdealCharacteristics, get_answer(a_dict,35))

    ## ANY CODE FOR CUSTOMIZED SECTION WILL COME HERE

    # TESTING THE CUSTOMIZED FIELDS

    model_card.model_details.entry1 = [mctlib.ModelDetailsExt1(entry1="BASARILI", question1="BASARI SORU")]

    # Comprehensive Fields
   
    mct.update_model_card(model_card)
    
    # Return the model card document as an HTML page

    html = mct.export_format()

    print("JSON and HTML file are created.")
    

    return html
    
def one_entry(object,entry):
    if entry:
        entries = entry.split('\n')
        len_entries= len(entries)
   
    
        if len_entries == 1:

            return [object(entries[0])]
        elif len_entries == 2:

            return [object(entries[0]),object(entries[1])]
        elif len_entries == 3:

            return [object(entries[0]),object(entries[1]),object(entries[2])]

        elif len_entries == 4:

            return [object(entries[0]),object(entries[1]),object(entries[2]),object(entries[3])]

        elif len_entries == 5:

            return [object(entries[0]),object(entries[1]),object(entries[2]),object(entries[3]),object(entries[4])]

def two_entry(object,entry_1,entry_2):

    if entry_1:
        entries_1 = entry_1.split('\n')
        len_entries= len(entries_1)

    if entry_2:
        entries_2 = entry_2.split('\n')
        len_entries= len(entries_1)

    
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


