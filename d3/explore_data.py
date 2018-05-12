# -*- coding: utf-8 -*-
"""
Created on Tue May  8 19:51:02 2018

@author: davil
"""
us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
    'District of Columbia':'DC'
}

import pandas as pd
import os

#################################################################################################
#################### Import Health data into Pandas Dataframe ###################################
#################################################################################################

#list of dictionaries with question and answer I want to filter the data on 
health_qa = [{'question':'Ever told you had a stroke?','answer':'Yes'},
             {'question':'Ever told you had a heart attack (myocardial infarction)?','answer':'Yes'},
             {'question':'Ever told you had angina or coronary heart disease?','answer':'Yes'},
             {'question':'Ever told you that you have a form of depression?','answer':'Yes'},
             {'question':'Ever told you have kidney disease?','answer':'Yes'},
             {'question':'Ever told you had skin cancer?','answer':'Yes'},
             {'question':'What is your annual household income?','answer':'Less than $15,000'},
             {'question':'Do you own or rent your home?','answer':'Rent'}
            ]
qlabel = ['stroke', 'heart attack', 'angina', 'depression', 'kidney', 'skin cancer', 'low income', 'rent'] 
qval_label = [q + '_percent' for q in qlabel]

#read in csv file --> pandas dataframe
health_df_in= pd.read_csv(os.path.join('resources','BRFSS_2014_Overall_Own_or_Rent.csv'))
#filter columns necessary to query data
health_df_in = health_df_in[['Locationabbr','Question', 'Response', 'Data_value']]
#filter the desired rows
df_list = []
for qa, label, qval in zip(health_qa,qlabel, qval_label):
    question, answer = qa['question'], qa['answer']
    temp_df = health_df_in[health_df_in['Question'] ==  question]
    temp_df = temp_df[temp_df['Response'] == answer]
    temp_df[label] = temp_df['Question']
    temp_df[qval] = temp_df['Data_value']
    temp_df['State'] = temp_df['Locationabbr']
    df_list.append(temp_df)

merged_df = df_list[0]
merged_df = merged_df[['State']]
for df in df_list:
    merged_df = pd.merge(merged_df, df, how='inner', on ='State')

cols = qval_label + ['State']
merged_df = merged_df[cols]
merged_df = merged_df.iloc[0:51] #remove us, puerto rico, etc

#################################################################################################
#################### Import Census data into Pandas Dataframe ###################################
#################################################################################################

foreign_df = pd.read_csv(os.path.join('resources','ACS_14_1YR_S0102','ACS_14_1YR_S0102_with_ann.csv'))
#State, percentage of people over 60 with disabilities
foreign_df = foreign_df[['GEO.display-label','HC02_EST_VC63']]
foreign_df['State'] = foreign_df['GEO.display-label']
foreign_df['over_60_disability_percent'] = foreign_df['HC02_EST_VC63']
#foreign_df = foreign_df[['State','foreign_rent_percent','latino_percent']][1:]
foreign_df = foreign_df.replace({'State':us_state_abbrev})

#################################################################################################
#################### Merge Census and Health data into Pandas Dataframe #########################
#################################################################################################

merged_df = pd.merge(merged_df, foreign_df, how='inner', on='State')
merged_df['over_60_disability_percent'] = merged_df['over_60_disability_percent'].apply(lambda x: float(x)) 

#loop over health variables and pick the ones with higher correlation to save to csv file

high_corr_vars = []
for issue in qval_label:
    merged_df.plot.scatter(x=issue, y='over_60_disability_percent')
    corr = merged_df[[issue,'over_60_disability_percent']].corr(method='pearson')
    #print(corr)
    if (corr.loc['over_60_disability_percent', issue] > 0.55):
        high_corr_vars.append(issue)
    #x = input('continue?')

print(f'\nVariables with high( > 0.55) correlation: {high_corr_vars}')

over_60_risks_df = merged_df[high_corr_vars + ['State', 'over_60_disability_percent']]
over_60_risks_df.set_index('State', inplace=True)
over_60_risks_df.to_csv(os.path.join('resources','Over60_wDisabilities_risks.csv'))
