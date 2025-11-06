import pandas as pd
import pm4py
import os
from pm4py.objects.conversion.log import converter as log_converter

xes_path =  "/Users/omarhamdi/Desktop/PermitLog.xes" 

csv_output_name = "fifth.csv" #


try:
    log = pm4py.read_xes(xes_path)
    df = pm4py.convert_to_dataframe(log)
except Exception as e:
    exit()

print(df.columns.tolist())

print(df.head())


df.to_csv(csv_output_name, index=False)
