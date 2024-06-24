import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from pm4py.objects.conversion.log import converter as xes_converter
from pm4py.algo.filtering.log.attributes import attributes_filter
from pm4py.objects.log.obj import EventLog, Trace, Event
import os
import glob
import sys
import constants


def format_dataframe(logistic : pd.DataFrame) -> pd.DataFrame:
    
    #format timestamp
    for idx, row in logistic.iterrows():
        logistic.loc[idx, 'time:timestamp'] = row['time:timestamp'].split('+')[0].split('.')[0]
    
    #convert to log
    logistic_log = xes_converter.apply(logistic, variant=xes_converter.Variants.TO_EVENT_LOG)
    
    #rename columns
    logistic = logistic.rename(columns = {'concept:name' : 'Equipment ID', 'time:timestamp' : 'Arrived Timestamp'})

    #create empty columns 
    columns_to_add = ['Departed Timestamp', 'case:Init Datetime', 'case:Complete Datetime', 'EQTYP', 'Zone Name', 'Floor', 'case:Src Eqt', 'case:Dest Eqt']
    for i in columns_to_add:
        logistic[i] = ""

    #get case attributes
    case_attributes = []
    for case in logistic_log:
        attribute = [case[0]['time:timestamp'], case[len(case) - 1]['time:timestamp'], case[0]['concept:name'], case[len(case) - 1]['concept:name']]
        for i in range(len(case)):
            case_attributes.append(attribute)
    
    
    for idx, row in logistic.iterrows():
        #add equipment atrributes
        logistic.loc[idx, 'EQTYP'] = row['Equipment ID'][0:2]
        logistic.loc[idx, 'Zone Name'] = row['Equipment ID'][3:4]
        logistic.loc[idx, 'Floor'] = row['Equipment ID'][2:3]
        #add case attributes
        logistic.loc[idx, 'case:Init Datetime'] = case_attributes[idx][0]
        logistic.loc[idx, 'case:Complete Datetime'] = case_attributes[idx][1]
        logistic.loc[idx, 'case:Src Eqt'] = case_attributes[idx][2]
        logistic.loc[idx, 'case:Dest Eqt'] = case_attributes[idx][3]
        

    #convert to new log
    new_log = xes_converter.apply(logistic, variant=xes_converter.Variants.TO_EVENT_LOG)

    #add departed timestamp
    departed_timestamp = []

    for case in new_log:
        for idx, event in enumerate(case):
            if idx < len(case) - 1:
                departed_timestamp.append(case[idx+1]['Arrived Timestamp'])
            else:
                departed_timestamp.append(case.attributes['Complete Datetime'])

    logistic['Departed Timestamp'] = departed_timestamp
    
    return logistic