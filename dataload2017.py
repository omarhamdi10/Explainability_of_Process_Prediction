import pandas as pd
import pm4py
import os 
from pm4py.objects.conversion.log import converter as log_converter

#Reading the data from the xes file
xes_path = "/Users/omarhamdi/Desktop/BPIChallenge2017.xes"
log = pm4py.read_xes(xes_path)
df = pm4py.convert_to_dataframe(log)


# renaming the columns
df.rename(columns={
    'case:concept:name': 'CaseID',
    'concept:name': 'Activity',
    'time:timestamp': 'Timestamp',
    'case:LoanGoal': 'LoanGoal',
    'case:ApplicationType': 'ApplicationType',
    'case:RequestedAmount': 'RequestedAmount',
    'org:resource': 'Resource',
    'lifecycle:transition': 'Transition'
}, inplace=True)



#sort by CseID and then sort it by timestamp
df.sort_values(by=['CaseID', 'Timestamp'], inplace=True)
print("DataFrame sorted by CaseID and Timestamp.")



#checking the number of cases where the milliseconds may affect the data
df['Timestamp_Sec'] = df['Timestamp'].dt.floor('S')
df['Prev_CaseID'] = df['CaseID'].shift(1)
df['Prev_Timestamp_Sec'] = df['Timestamp_Sec'].shift(1)


same_second_mask = (df['CaseID'] == df['Prev_CaseID']) & \
                   (df['Timestamp_Sec'] == df['Prev_Timestamp_Sec'])

order_critical_mask = same_second_mask & (df['Timestamp'] != df['Timestamp'].shift(1))

# 4. Count the number of unique Case IDs affected
cases_affected_by_milliseconds = df[order_critical_mask]['CaseID'].nunique()

print(f"Total Cases in Log: {df['CaseID'].nunique()}")
print(f"Total Unique Cases where Milliseconds Determine Order: {cases_affected_by_milliseconds}")

# Clean up temporary columns used for shifting
df.drop(columns=['Timestamp_Sec', 'Prev_CaseID', 'Prev_Timestamp_Sec'], inplace=True)

# Time Standrization
df['Timestamp'] = df['Timestamp'].dt.floor('S')
df['Timestamp'] = df['Timestamp'].dt.tz_localize(None)
df.sort_values(by=['CaseID', 'Timestamp'], inplace=True)

# Define all columns being that have missing values
imputation_cols = [
    'OfferedAmount', 'MonthlyCost', 'FirstWithdrawalAmount',
    'NumberOfTerms', 'CreditScore', 'Accepted', 'Selected', 'OfferID'
]
missing_before = df[imputation_cols].isnull().sum()
print(missing_before[missing_before > 0])

# Define columns identified as having high missing percentages
numeric_cols = [
    'OfferedAmount', 'MonthlyCost', 'FirstWithdrawalAmount',
    'NumberOfTerms', 'CreditScore'
]
categorical_cols = [
    'Accepted', 'Selected', 'OfferID'
]

# In numerical columns replace missing values with 0
for col in numeric_cols:
    df[col].fillna(0.0, inplace=True)

# In categorical columns replace with NA
for col in categorical_cols:
    df[col].fillna('N/A', inplace=True)

print("\n--- Missing Value Count AFTER Imputation ---")
missing_after = df[imputation_cols].isnull().sum()
print(missing_after)


# --- Check for Duplicates ---
initial_rows = len(df)
duplicate_rows = df.duplicated().sum()

print(f"\n Looking for duplicates]")
print(f"Total rows before checking: {initial_rows}")
print(f"Total exact duplicate rows found: {duplicate_rows}")

if duplicate_rows > 0:
    df.drop_duplicates(inplace=True) 
    
    final_rows = len(df)
    print(f"Removed {duplicate_rows} duplicate rows.")
    print(f"Total rows after removal: {final_rows}")
else:
    print("No exact duplicate rows found.")


# Saving the data in a CSV file 
output_csv_path = "BPIChallenge2017.csv"
df.to_csv(output_csv_path, index=False)


#Creating a file to save the filtered logs in
output_dir = "split_logs"
os.makedirs(output_dir, exist_ok=True) # Ensure the output folder exists

# Filter and save 'A_' (Application) events
df_A = df[df['Activity'].str.startswith('A_')].copy()
path_A = os.path.join(output_dir, "BPI_2017_Log_A_Application.csv")
df_A.to_csv(path_A, index=False)


# Filter and save 'W_' (Workflow) events
df_W = df[df['Activity'].str.startswith('W_')].copy()
path_W = os.path.join(output_dir, "BPI_2017_Log_W_Workflow.csv")
df_W.to_csv(path_W, index=False)


# Filter and save 'O_' (Offer) events
df_O = df[df['Activity'].str.startswith('O_')].copy()
path_O = os.path.join(output_dir, "BPI_2017_Log_O_Offer.csv")
df_O.to_csv(path_O, index=False)



#printing the data
print(df.shape) 
