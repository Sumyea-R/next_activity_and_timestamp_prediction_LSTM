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
from bidict import bidict
from datetime import datetime, timedelta
import numpy as np
from utility import constants


def format_input_features(X : [[[]]], max_case_len):
    """
    Fromats the input feature vector X for model training
    """
    X_formatted = np.zeros((len(X), max_case_len, len(X[0][0])), dtype=np.float32)
    
    for idx_state, state in zip(range(len(X)) ,X):
        for idx_row, row in zip(range((max_case_len - len(state)), max_case_len) ,state):
            X_formatted[idx_state][idx_row] = row
            
    return X_formatted

def average_dwell_time(log: EventLog) -> float:
    """
    Compute the average dwell time (from Arrived Timestmap to the next Arrived Timestamp of the next equipment) in log
    """
    dwell_times = []
    for case in log:
        dwell_time = case.attributes['Init Datetime'] - case[0][constants.attr_arrived_time]
        dwell_times.append(dwell_time.total_seconds())
        for idx, event in enumerate(case[1:], 1):
            dwell_time = event[constants.attr_arrived_time] - case[idx-1][constants.attr_arrived_time]
            dwell_times.append(dwell_time.total_seconds())
    average_dwell_time_in_sec = np.mean([dwell_time for dwell_time in dwell_times])
    return average_dwell_time_in_sec

def average_time_since_case_start(log: EventLog) -> float:
    """
    Compute the average of every Arrived Timestamp to the first Arrived Timestamp of a case (since case starts) in log
    """
    times_since_start = []
    for case in log:
        for event in case:
            time_since_start = event[constants.attr_arrived_time] - case.attributes['Init Datetime']
            times_since_start.append(time_since_start.total_seconds())
    average_time_since_start_in_sec = np.mean([time_since_start for time_since_start in times_since_start])
    return average_time_since_start_in_sec

def average_time_till_case_end(log: EventLog) -> float:
    """
    Compute the average of every Arrived Timestamp to the first Arrived Timestamp of a case (since case starts) in log
    """
    times_till_end = []
    for case in log:
        for event in case:
            time_till_end = case.attributes['Complete Datetime'] - event[constants.attr_arrived_time]
            times_till_end.append(time_till_end.total_seconds())
    average_time_till_end_in_sec = np.mean([time_till_end for time_till_end in times_till_end])
    return average_time_till_end_in_sec




