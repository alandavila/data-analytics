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


skin_df = pd.read_csv(os.path.join('resources','BRFSS_2014_Overall_skin_cancer.csv'))
skin_cancer = skin_df[['Locationabbr','Data_value']][skin_df['Response'] == 'Yes']
skin_cancer.reset_index(inplace=True)
#drop US, Puerto Rico, Guam and UW
skin_cancer = skin_cancer.drop(skin_cancer.index[[51,52,53,54]])
skin_cancer['State'] = skin_cancer['Locationabbr']
skin_cancer['cancer_percent'] = skin_cancer['Data_value']
skin_cancer = skin_cancer[['State','cancer_percent']]


rent_df = pd.read_csv(os.path.join('resources','BRFSS_2014_Overall_Own_or_Rent.csv'))
rent_df = rent_df[rent_df['Question'] == 'Do you own or rent your home?']
rent_df = rent_df[rent_df['Response'] == 'Rent']
rent_df.index = range(0,55)
rent_df = rent_df[['Locationabbr','Data_value']]
rent_df = rent_df.drop(rent_df.index[[51,52,53,54]])
rent_df['State'] = rent_df['Locationabbr']
rent_df['rent_percent'] = rent_df['Data_value']
rent_df = rent_df[['State','rent_percent']]

#dictionary of health factors to investigate in form of desired quesiton:answer
health_qa = [('Ever told you had a stroke?','Yes'),
             ('Ever told you had a heart attack (myocardial infarction)?','Yes'),
             ('Ever told you had angina or coronary heart disease?','Yes'),
             ('Ever told you that you have a form of depression?','Yes'),
             ('Ever told you have kidney disease?','Yes'),
             ('Ever told you had skin cancer?','Yes'),
             ('What is your annual household income?','Less than $15,000'),
             ('Do you own or rent your home?','Rent')
             ]
health_df = pd.read_csv(os.path.join('resources','BRFSS_2014_Overall_Own_or_Rent.csv'))
#filter out df data to include desired questions/answers only
health_df = health_df[health_df.Question == health_qa]
#for question, answer in health_qa.items():
#    health_df



#join cancer rate and rent rate in same dataframe
merged_df = pd.merge(skin_cancer, rent_df, how='inner', on='State')


foreign_df = pd.read_csv(os.path.join('resources','ACS_14_1YR_S0502','ACS_14_1YR_S0502_with_ann.csv'))
#State, percent of rented occupied housing units, percent of latinos
foreign_df = foreign_df[['GEO.display-label','HC01_EST_VC169','HC01_EST_VC41']]
foreign_df['State'] = foreign_df['GEO.display-label']
foreign_df['foreign_rent_percent'] = foreign_df['HC01_EST_VC169']
foreign_df['latino_percent'] = foreign_df['HC01_EST_VC41']
foreign_df = foreign_df[['State','foreign_rent_percent','latino_percent']][1:]
foreign_df = foreign_df.replace({'State':us_state_abbrev})

merged_df = pd.merge(merged_df, foreign_df, how='inner', on='State')
merged_df['foreign_rent_percent'] = merged_df['foreign_rent_percent'].apply(lambda x: float(x)) 
merged_df['latino_percent'] = merged_df['latino_percent'].apply(lambda x: float(x)) 

merged_df.plot.scatter(x='rent_percent', y='foreign_rent_percent')
corr = merged_df[['rent_percent','foreign_rent_percent']].corr(method='pearson')
print(corr)

#merged_df.plot.scatter(x='cancer_percent', y='latino_percent')
#corr = merged_df[['cancer_percent','latino_percent']].corr(method='pearson')
#print(corr)

