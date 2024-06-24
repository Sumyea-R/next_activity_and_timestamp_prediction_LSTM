import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import pandas as pd
from pm4py.objects.conversion.log import converter as xes_converter
from pm4py.algo.filtering.log.attributes import attributes_filter
from pm4py.objects.log.obj import EventLog, Trace, Event
import math
import csv
from bidict import bidict
from datetime import datetime, timedelta
import numpy as np
import networkx as nx
import regex as re
from pre_process import preprocess_graph_attributes
from utility import constants

def encode_routing_features(eid_mapper: bidict, case: Trace, event: Event, network: nx.DiGraph, max_successors: int) -> [int]:
    
    """
    Encode successor equipments with lowest score in the routing network
    """
    # Initialize an empty list to store the encoded routing features
    routing_vector = []
    
    # Initialize an empty list to store the lowest scored successor of the current equipment
    lowest_scored_successors = []
    
    # Get current equipment, src and dest location
    equipment = event[constants.attr_equipment]
    src_loc = case.attributes['Src Loc']
    dest_loc = case.attributes['Dest Loc']
    
    if not network.has_node(equipment):
        return [-1]*max_successors*2
    
    # Traverse the successors of current equipment to get the lowest scored successors
    for n in network.successors(equipment):
        
        # Get the score of the successor
        successor_score = list(network[equipment][n].get('score'))
        
        # Filter the scores that has the same src and dest loc
        successor_score = filter(lambda x: ((x[0] == src_loc) & (x[1] == dest_loc)), successor_score)
        
        # Sort the scores based on routing score
        successor_score = sorted(successor_score, key=lambda score: score[2])
        if successor_score:
            lowest_score = successor_score[0][2]
            # Keep the score that has the lowest score and highest ISN
            successor_score = sorted(successor_score, key=lambda x: (x[2], -x[5]))
            tup = (n, successor_score[0])
            lowest_scored_successors.append(tup)
    
    # Sort the successors based on lowest routing score and highest ISN
    lowest_scored_successors = sorted(lowest_scored_successors, key=lambda x: (x[1][2], -x[1][5]))
    successor = min(len(lowest_scored_successors), max_successors)
    
    # Keep the max_successors number of lowest successors
    for i in range(successor):
        encoded_eid = eid_mapper[lowest_scored_successors[i][0]]
        score_of_encoded_eid = lowest_scored_successors[i][1][2]
        
        # Append the successor with routing score
        routing_vector+= [encoded_eid, score_of_encoded_eid]
    
    # If no or less than max_successors found append -1
    routing_vector+= [-1]*(max_successors*2 - len(routing_vector))
    
    return routing_vector