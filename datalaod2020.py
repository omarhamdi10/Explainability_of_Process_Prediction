import pandas as pd
import pm4py
import os
from pm4py.objects.conversion.log import converter as log_converter


# file paths
file_paths = [
    "/Users/omarhamdi/Desktop/DomesticDeclarations.xes" ,
   "/Users/omarhamdi/Desktop/InternationalDeclarations.xes",      
    "/Users/omarhamdi/Desktop/PrepaidTravelCost.xes",      
    "/Users/omarhamdi/Desktop/RequestForPayment.xes",      
    "/Users/omarhamdi/Desktop/PermitLog.xes"      
]

renaming_maps = [
    { 
        'case:id': 'CaseID',
        'concept:name': 'Activity',
        'time:timestamp': 'Timestamp',
        'org:resource': 'Resource'
    },
    { 
        'case:id': 'CaseID', 
        'concept:name': 'Activity', 
        'time:timestamp': 'Timestamp',
        'org:resource': 'Resource'
    },
   
    { 
        'case:id': 'CaseID', 
        'concept:name': 'Activity', 
        'time:timestamp': 'Timestamp',
        'org:resource': 'Resource'
    },
    
    { 
        'case:id': 'CaseID', 
        'concept:name': 'Activity', 
        'time:timestamp': 'Timestamp',
        'org:resource': 'Resource'
    },
    
    { 
        'case:id': 'CaseID', 
        'concept:name': 'Activity', 
        'time:timestamp': 'Timestamp',
        'org:resource': 'Resource'
    }
]

# Dictionary to store the 5 cleaned DataFrames
cleaned_logs = {}


