import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import pandas as pd
import pm4py
from pm4py.objects.conversion.log import converter as xes_converter
from pm4py.algo.filtering.log.attributes import attributes_filter
from pm4py.objects.log.obj import EventLog, Trace, Event
import math
import csv
from CminSampler import CminSampler
from utility import constants


df = pd.read_csv('logistic.csv')[constants.required_attributes+constants.event_attribute_features+constants.case_attribute+ constants.src_dest_attributes]


def create_tuples(df: pd.DataFrame) -> set:
    tuples = []

    for idx, row in df.iterrows():
        tup = (row['case:Src Eqt'], row['case:Dest Eqt'])
        tuples.append(tup)

    return set(tuples)


def create_dataframes(df: pd.DataFrame) -> []:
    dataframes = []
    tuples = create_tuples(df)
    for tup in tuples:
        filtered_df = df[(df['case:Src Eqt'] == tup[0]) & (df['case:Dest Eqt'] == tup[1])]
        dataframes.append(filtered_df)
    return dataframes


def save_dfs_as_csv(dataframes: [], df_path: str) -> None:
    
    #delete empty dataframes
    for i, dataframe in zip(range(len(dataframes)), dataframes):
        if len(dataframe) == 0:
            del dataframes[i]
    count = 0
    for dataframe in dataframes:
        name = 'df_'+str(count)+'.csv'
        dataframe.to_csv(df_path+name)
        count+=1

dataframes = create_dataframes(df)
save_dfs_as_csv(dataframes, constants.df_path)