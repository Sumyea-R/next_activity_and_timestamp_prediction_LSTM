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
import constants
import os
import glob
import sys
import matplotlib.pyplot as plt
import format_logistic as fl


def read_dfs(df_path: str) -> []:
    '''reads all csv files for sampling'''
    
    # Use os.fchdir() method to change the dir
    fd = os.open(df_path, os.O_RDONLY )
    os.fchdir(fd)
    
    # use glob to get all the csv files in the folder
    path = os.getcwd()
    csv_files = glob.glob(os.path.join(path, "*.csv"))
    
    dataframes = []
    
    # loop over the list of csv files
    for f in csv_files:
        
        # get src and dest loc from the file name
        src_dest_loc = f.split('/')[-1].split('_')[1:]
        src_loc = src_dest_loc[0]
        dest_loc = src_dest_loc[1].split('.')[0]
        
        # read the csv file
        df = pd.read_csv(f)
        # add source and destination location
        df['case:Src Loc'] = src_loc
        df['case:Dest Loc'] = dest_loc
        dataframes.append(df)
        
    return dataframes


def convert_to_logs(dataframes: []):
    '''converts the dataframes into event logs and computes the number of cases of each log'''
    
    logs = []
    cases = []
    for dataframe in dataframes:
        log = xes_converter.apply(dataframe, variant=xes_converter.Variants.TO_EVENT_LOG) 
        logs.append(log)
        cases.append(len(log))
    return logs, cases


def sample_cases(dataframes: [], cases_len:[]) -> []:
    '''samples cases from the dataframes'''
    
    sampled_cases = []
    sampled_dfs = [0]*len(dataframes)
    indices = []
    
    # the percentage of cases to sample
    for percentage in [0.10, 0.20, 0.30, 0.40, 0.50]:
        for i, dataframe in zip(range(0, len(cases_len)), dataframes):
            if i not in indices:
                if percentage != 0.50:
                    #the dataframe has only one case, sampling not needed
                    if cases_len[i] == 1:
                        sampled_dfs[i] = dataframe
                        case = [dataframe.iloc[0]['case:concept:name']]
                        sampled_cases.append(case)
                        indices.append(i)
                    # sample cases based on percentage
                    else:
                        n = math.ceil(cases_len[i]*percentage)
                        # use cminsampler to sample
                        sampler = CminSampler(n)
                        sampler.load_df(dataframe, 'case:concept:name', 'concept:name')
                        cases = sampler.sample()
                        sampled_df = dataframe[(dataframe['case:concept:name'].isin(cases))]
                        # check how many unique equipments the sampling method covered
                        equipment = set(dataframe['concept:name'].to_list())
                        sampled_equipments = set(sampled_df['concept:name'].to_list())
                        coverage = len(sampled_equipments)/len(equipments)
                        # equipment coverage less than 80%, increase case percentage to sample
                        if coverage >= 0.80:
                            sampled_dfs[i] = sampled_df
                            sampled_cases.append(cases)
                            indices.append(i)
                else:
                    # case percentage 50%, stop sampling
                    n = math.ceil(cases_len[i]*percentage)
                    sampler = CminSampler(n)
                    sampler.load_df(dataframe, 'case:concept:name', 'concept:name')
                    cases = sampler.sample()
                    sampled_df = dataframe[(dataframe['case:concept:name'].isin(cases))]
                    sampled_dfs[i] = sampled_df
                    sampled_cases.append(cases)
                    indices.append(i)
    
    return sampled_dfs

#helper functions
def get_statistics(dataframes: [], sampled_dfs: []) -> [[]]:
    ''' calculates statistics on the sampled datasets'''
    
    events = []
    sampled_events = []
    
    for dataframe, sampled_df in zip(dataframes, sampled_dfs):
        event = len(set(dataframe['Equipment ID'].to_list()))
        sampled_event = len(set(sampled_df['Equipment ID'].to_list()))
        events.append(event)
        sampled_events.append(sampled_event)
    
    return [events, sampled_events]

def plot_distribution(statistic: [], plt_name: str, figure_name: str)-> None:
    
    x = [i for i in range(len(statistic))]
    y = statistic
    
    plt.plot(x, y)
    plt.xlabel('Dataframe Index')
    plt.ylabel('Number of Cases')
    plt.title(plt_name)
    plt.savefig(figure_name)
    plt.show()


dataframes = read_dfs(constants.df_path)
logs, case_lens = convert_to_logs(dataframes)
sampled_dfs = sample_cases(dataframes, case_lens)
sampled_df = pd.concat(sampled_dfs)
sampled_df = fl.format_dataframe(sampled_df)
sampled_df.to_csv('logistic_sampled.csv')   