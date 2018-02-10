
# Heroes of Pymoli Data Analysis

* The most profitable age group for the company is from 20 to 24 years but the average purchase total is higher among people between 30 and 34 years old
* There are 4.5x more male players than female players but they only outspend them by ~4x
* The most expensive item does not make the cut of 5 most profitable items

Dependencies


```python
import os
import pandas as pd
```

Data &rarr; data frame


```python
purchase_data_path = os.path.join('Resources','purchase_data.json')
purchase_df = pd.read_json(purchase_data_path)
```

#### Get total number of players


```python
#Distinguish players by SN attribute
total_players = len(purchase_df['SN'].unique())
total_players_df = pd.DataFrame({'Total Players':[total_players]})
total_players_df

```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Total Players</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>573</td>
    </tr>
  </tbody>
</table>
</div>



####  Do purchase analysis


```python
total_items = len(purchase_df['Item ID'].unique())
average_item_price = purchase_df['Price'].mean()
total_purchases = purchase_df['Price'].count()
total_revenue = purchase_df['Price'].sum()
#create dataframe with computed values
purchase_analysis_total_df = pd.DataFrame(
    {'Number of Unique Items':[total_items],
     'Average Purchase Price':[average_item_price],
     'Total Number of Purchases':[total_purchases],
     'Total Revenue':[total_revenue]})
#format currency
purchase_analysis_total_df['Average Purchase Price'] = \
purchase_analysis_total_df['Average Purchase Price'].map('${:,.2f}'.format)
purchase_analysis_total_df['Total Revenue'] = \
purchase_analysis_total_df['Total Revenue'].map('${:,.2f}'.format)
#re-arrange columns
purchase_analysis_total_df = purchase_analysis_total_df[['Number of Unique Items',
                                                        'Average Purchase Price',
                                                        'Total Number of Purchases',
                                                        'Total Revenue']]
purchase_analysis_total_df
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Number of Unique Items</th>
      <th>Average Purchase Price</th>
      <th>Total Number of Purchases</th>
      <th>Total Revenue</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>183</td>
      <td>$2.93</td>
      <td>780</td>
      <td>$2,286.33</td>
    </tr>
  </tbody>
</table>
</div>



#### Gender demographics


```python
males_df = purchase_df.loc[purchase_df['Gender'] == 'Male']
females_df = purchase_df.loc[purchase_df['Gender'] == 'Female']
#use SN to distinguish players and avoid double counting
males = len(males_df['SN'].unique())
females = len(females_df['SN'].unique())
others = len(purchase_df['SN'].unique()) - males - females
#create dataframe 
gender_df = pd.DataFrame({'Male':[100*males/total_players, males],
                          'Female':[100*females/total_players, females],
                         'Other / Non-Disclose':[100*others/total_players, others]})
#re-arrange columns
gender_df = gender_df[['Male', 'Female','Other / Non-Disclose']]
gender_df.index = ['Percentage of Players', 'Total Count']
gender_df = gender_df.transpose()
#format percent and integers
gender_df['Percentage of Players'] = gender_df['Percentage of Players'].map('{:,.2f}%'.format)
gender_df['Total Count'] = gender_df['Total Count'].map('{:,.0f}'.format)
gender_df
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Percentage of Players</th>
      <th>Total Count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Male</th>
      <td>81.15%</td>
      <td>465</td>
    </tr>
    <tr>
      <th>Female</th>
      <td>17.45%</td>
      <td>100</td>
    </tr>
    <tr>
      <th>Other / Non-Disclose</th>
      <td>1.40%</td>
      <td>8</td>
    </tr>
  </tbody>
</table>
</div>



#### Do purchase analysis by gender


```python
#group data into gender categories
purchase_gender_gp = purchase_df.groupby('Gender')
#aggregate to get each category's count, sum, mean, divide sum/count to get norm totals
gender_count_series =  purchase_gender_gp['Price'].count()
gender_mean_series = purchase_gender_gp['Price'].mean().map('${:,.3f}'.format)
gender_total_series = purchase_gender_gp['Price'].sum().map('${:,.3f}'.format)
gender_norm_series = \
purchase_gender_gp['Price'].sum()/purchase_gender_gp['Price'].count()
gender_norm_series = gender_norm_series.map('${:,.3f}'.format)
#merge series to create dataframe
purchase_gender_df = pd.concat([gender_count_series, gender_mean_series,
                                gender_total_series, gender_norm_series], axis=1)
purchase_gender_df.columns = ['Purchase Count', 'Average Purchase Price',
                              'Total Purchase Value', 'Normalized Totals']
purchase_gender_df
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Purchase Count</th>
      <th>Average Purchase Price</th>
      <th>Total Purchase Value</th>
      <th>Normalized Totals</th>
    </tr>
    <tr>
      <th>Gender</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Female</th>
      <td>136</td>
      <td>$2.816</td>
      <td>$382.910</td>
      <td>$2.816</td>
    </tr>
    <tr>
      <th>Male</th>
      <td>633</td>
      <td>$2.951</td>
      <td>$1,867.680</td>
      <td>$2.951</td>
    </tr>
    <tr>
      <th>Other / Non-Disclosed</th>
      <td>11</td>
      <td>$3.249</td>
      <td>$35.740</td>
      <td>$3.249</td>
    </tr>
  </tbody>
</table>
</div>



#### Age Demographics


```python
#define age bins for analysis
age_bins = [0, 10, 15, 20, 25, 30, 35, 40,45]
labels = ['<10','10-14','15-19', '20-24', '25-29', '30-34', '35-39', '>40']
#assign rows to their corresponding age bins generated by cut
purchase_df['Age Range'] = pd.cut(purchase_df['Age'], bins=age_bins, labels=labels)
#group by age bins
purchase_age_range_gp = purchase_df.groupby('Age Range')
#aggregate per bin information
purchase_age_count_series = purchase_age_range_gp['Price'].count()
purchase_age_mean_series = purchase_age_range_gp['Price'].mean().map('${:,.3f}'.format)
purchase_age_total_series = purchase_age_range_gp['Price'].sum().map('${:,.3f}'.format)
purchase_age_norm_series = \
purchase_age_range_gp['Price'].sum()/purchase_age_range_gp['Price'].count()
purchase_age_norm_series = purchase_age_norm_series.map('${:,.3f}'.format)
#merge series to create dataframe
purchase_age_df = pd.concat([purchase_age_count_series, purchase_age_mean_series,
                             purchase_age_total_series, purchase_age_norm_series], axis=1)
purchase_age_df.columns = ['Purchase Count', 'Average Purchase Price', 'Total Purchase Value',
                           'Normalized Totals']
purchase_age_df
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Purchase Count</th>
      <th>Average Purchase Price</th>
      <th>Total Purchase Value</th>
      <th>Normalized Totals</th>
    </tr>
    <tr>
      <th>Age Range</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>&lt;10</th>
      <td>32</td>
      <td>$3.019</td>
      <td>$96.620</td>
      <td>$3.019</td>
    </tr>
    <tr>
      <th>10-14</th>
      <td>78</td>
      <td>$2.874</td>
      <td>$224.150</td>
      <td>$2.874</td>
    </tr>
    <tr>
      <th>15-19</th>
      <td>184</td>
      <td>$2.874</td>
      <td>$528.740</td>
      <td>$2.874</td>
    </tr>
    <tr>
      <th>20-24</th>
      <td>305</td>
      <td>$2.959</td>
      <td>$902.610</td>
      <td>$2.959</td>
    </tr>
    <tr>
      <th>25-29</th>
      <td>76</td>
      <td>$2.892</td>
      <td>$219.820</td>
      <td>$2.892</td>
    </tr>
    <tr>
      <th>30-34</th>
      <td>58</td>
      <td>$3.073</td>
      <td>$178.260</td>
      <td>$3.073</td>
    </tr>
    <tr>
      <th>35-39</th>
      <td>44</td>
      <td>$2.898</td>
      <td>$127.490</td>
      <td>$2.898</td>
    </tr>
    <tr>
      <th>&gt;40</th>
      <td>3</td>
      <td>$2.880</td>
      <td>$8.640</td>
      <td>$2.880</td>
    </tr>
  </tbody>
</table>
</div>



#### Top Spenders


```python
#group by SN to get unique customers
purchase_sn_gp = purchase_df.groupby('SN')
#aggregate per user info
#we will defer formating totals since we need to sort their values
purchase_sn_total_series = purchase_sn_gp['Price'].sum()
purchase_sn_count_series = purchase_sn_gp['SN'].count()
purchase_sn_mean_series = purchase_sn_gp['Price'].mean().map('${:,.3f}'.format)
#merge series to create dataframe
purchase_sn_df = pd.concat([purchase_sn_count_series, purchase_sn_mean_series, purchase_sn_total_series], axis=1)
purchase_sn_df.columns = ['Purchase Count', 'Average Purchase Price', 'Total Purchase Value']
#find top spenders by sorting
top_spenders = purchase_sn_df.sort_values(by='Total Purchase Value', ascending=False).head(5)
top_spenders['Total Purchase Value'] = top_spenders['Total Purchase Value'].map('${:,.3f}'.format)
top_spenders


```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Purchase Count</th>
      <th>Average Purchase Price</th>
      <th>Total Purchase Value</th>
    </tr>
    <tr>
      <th>SN</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Undirrala66</th>
      <td>5</td>
      <td>$3.412</td>
      <td>$17.060</td>
    </tr>
    <tr>
      <th>Saedue76</th>
      <td>4</td>
      <td>$3.390</td>
      <td>$13.560</td>
    </tr>
    <tr>
      <th>Mindimnya67</th>
      <td>4</td>
      <td>$3.185</td>
      <td>$12.740</td>
    </tr>
    <tr>
      <th>Haellysu29</th>
      <td>3</td>
      <td>$4.243</td>
      <td>$12.730</td>
    </tr>
    <tr>
      <th>Eoda93</th>
      <td>3</td>
      <td>$3.860</td>
      <td>$11.580</td>
    </tr>
  </tbody>
</table>
</div>



#### Most Popular Items


```python
#group items by Item ID
purchase_id_gp = purchase_df.groupby(['Item ID','Item Name'])
#aggregate per item info
purchase_id_count = purchase_id_gp['Item ID'].count()
#we will defer formating totals since we need to sort their values
purchase_id_total = purchase_id_gp['Price'].sum()
purchase_id_price = purchase_id_gp['Price'].mean().map('${:,.3f}'.format)
#concatenate series into a datafame
purchase_id_df =pd.concat([purchase_id_count, purchase_id_price, purchase_id_total], axis=1)
purchase_id_df.columns = ['Purchase Count', 'Item Price', 'Total Purchase Value']
most_popular = purchase_id_df.sort_values(by='Purchase Count', ascending=False).head(5)
most_popular
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
      <th>Purchase Count</th>
      <th>Item Price</th>
      <th>Total Purchase Value</th>
    </tr>
    <tr>
      <th>Item ID</th>
      <th>Item Name</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>39</th>
      <th>Betrayal, Whisper of Grieving Widows</th>
      <td>11</td>
      <td>$2.350</td>
      <td>25.85</td>
    </tr>
    <tr>
      <th>84</th>
      <th>Arcane Gem</th>
      <td>11</td>
      <td>$2.230</td>
      <td>24.53</td>
    </tr>
    <tr>
      <th>31</th>
      <th>Trickster</th>
      <td>9</td>
      <td>$2.070</td>
      <td>18.63</td>
    </tr>
    <tr>
      <th>175</th>
      <th>Woeful Adamantite Claymore</th>
      <td>9</td>
      <td>$1.240</td>
      <td>11.16</td>
    </tr>
    <tr>
      <th>13</th>
      <th>Serenity</th>
      <td>9</td>
      <td>$1.490</td>
      <td>13.41</td>
    </tr>
  </tbody>
</table>
</div>



#### Most Profitable Items


```python
most_profitable = purchase_id_df.sort_values(by='Total Purchase Value', ascending=False)
most_profitable['Total Purchase Value'] = most_profitable['Total Purchase Value'].map('${:,.3f}'.format)
most_profitable.head(5)
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
      <th>Purchase Count</th>
      <th>Item Price</th>
      <th>Total Purchase Value</th>
    </tr>
    <tr>
      <th>Item ID</th>
      <th>Item Name</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>34</th>
      <th>Retribution Axe</th>
      <td>9</td>
      <td>$4.140</td>
      <td>$37.260</td>
    </tr>
    <tr>
      <th>115</th>
      <th>Spectral Diamond Doomblade</th>
      <td>7</td>
      <td>$4.250</td>
      <td>$29.750</td>
    </tr>
    <tr>
      <th>32</th>
      <th>Orenmir</th>
      <td>6</td>
      <td>$4.950</td>
      <td>$29.700</td>
    </tr>
    <tr>
      <th>103</th>
      <th>Singed Scalpel</th>
      <td>6</td>
      <td>$4.870</td>
      <td>$29.220</td>
    </tr>
    <tr>
      <th>107</th>
      <th>Splitter, Foe Of Subtlety</th>
      <td>8</td>
      <td>$3.610</td>
      <td>$28.880</td>
    </tr>
  </tbody>
</table>
</div>


