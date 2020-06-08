import pandas as pd
import datetime
from scipy.stats import ttest_ind
from numpy.core.defchararray import isnumeric

"""
                                            Definitions:
A quarter is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
A recession is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
A recession bottom is the quarter within a recession which had the lowest GDP.
A university town is a city which has a high percentage of university students compared to the total population of the city.

Hypothesis: University towns have their mean housing prices less effected by recessions. Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. (`price_ratio=quarter_before_recession/recession_bottom`)
"""

states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}
state = 'Alabama'
organize = {state:[]}
cities = []

def get_list_of_university_towns():
    global state
    with open('university_towns.txt','r') as file:
        df = pd.read_table(file, sep='\n')

    for name in df['Alabama[edit]']:
        if '[' in name and name[name.index('[') + 1] == 'e':
            state = name[:name.index('[')].rstrip()
            organize[state] = []
        elif '(' in name:
            name = name[:name.index('(')].rstrip()
            organize[state].append(name)
        else:
            organize[state].append(name)
    new = pd.DataFrame([[st, unv] for st in organize.keys() for unv in organize[st]], columns=["State", "RegionName"])

    return new

economic = lambda : pd.read_excel('gdplev.xls')

def fun(item):
    if type(item) == datetime.datetime:
        return 'y'
    else:
        if item == 'Current-Dollar and "Real" Gross Domestic Product':
            return 'year'
        elif item[-1] == '1':
            return 'gdp year'
        elif item[-1] == '2':
            return 'gdp defaut year'
        elif item[-1] == '3':
            return 'x'
        elif item[-1] == '4':
            return 'quarter'
        elif item[-1] == '5':
            return 'bilions_2'
        elif item[-1] == '6':
            return '2009_2'
        

adjust = lambda ec:(ec.rename(columns=dict(zip(ec.columns, (fun(i) for i in ec.columns))))
                      .drop(range(7))
                      .reset_index()
                      .drop(['index', 'x', 'y'], axis=1))

def get_recession_start():
    """this function returns the recession start period"""

    ec = economic()
    ec = adjust(ec)
    starter = [ec.loc[i-1, 'quarter'] for i in ec.index if i>=2 if int(ec.loc[i, 'quarter'][:4]) >=2000 if (ec.loc[i, '2009_2'] < ec.loc[i-1, '2009_2']) and (ec.loc[i-1, '2009_2'] < ec.loc[i-2, '2009_2'])]

    return starter[0]

def get_recession_end():
    """this function returns the recession end period"""

    ec = economic()
    ec = adjust(ec)
    end = ([ec.loc[i, 'quarter'] for i in ec.index
            if i>=2 if int(ec.loc[i, 'quarter'][:4]) > int(get_recession_start()[:4])  
            if (ec.loc[i, '2009_2'] > ec.loc[i-1, '2009_2']) and (ec.loc[i-1, '2009_2'] > ec.loc[i-2, '2009_2'])])
    return end[0]


def get_recession_bottom():
    """this function returns the worst quarter of the recession period"""

    minimum = 0
    quarter = ''
    ec = economic()
    ec = adjust(ec)
    for i in ec.index:
        if int(ec.loc[i, 'quarter'][:4]) >= 2000:
            if (ec.loc[i, '2009_2']< ec.loc[i-1, '2009_2']) and (ec.loc[i-1, '2009_2'] < ec.loc[i-2, '2009_2']):
                new = ec.loc[i, '2009_2']
                if minimum == 0 or new < minimum:
                    quarter = ec.loc[i, 'quarter']
                    minimum = new
    return quarter

#-------------------------------------------------------------------------------------------------------------
job = pd.read_csv('City_Zhvi_AllHomes.csv')
get = lambda : (job.drop([coluna for coluna in job.columns if coluna[:4] < '2000'], axis=1)
                   .drop(['RegionID', 'Metro', 'CountyName', 'SizeRank',], axis=1))

#-------------------------------------------------------------------------------------------------------------
def sep(job):
    for col in job.columns:
        if isnumeric(col[0]):
            if col[-2] == '0':
                if col[-1] == '1':
                    name = col[:4]+'q1'
                    supose = job.loc[:, [col[:4] + '-01', col[:4] + '-02', col[:4] + '-03']]
                    job[name] = supose.mean(axis=1)
                elif col[-1] == '4':
                    name = col[:4]+'q2'
                    supose = job.loc[:, [col[:4] + '-04', col[:4] + '-05', col[:4] + '-06']]
                    job[name] = supose.mean(axis=1)
                elif col[-1] == '7':
                    if col[:4] != '2016':
                        name = col[:4]+'q3'
                        supose = job.loc[:, [col[:4] + '-07', col[:4] + '-08', col[:4] + '-09']]
                        job[name] = supose.mean(axis=1)
                    else:
                        name = col[:4] + 'q3'
                        supose = job.loc[:, [col[:4] + '-07', col[:4] + '-08']]
                        job[name] = supose.mean(axis=1)
            elif col[-2] == '1':
                name = col[:4]+'q4'
                supose = job.loc[:, [col[:4] + '-10', col[:4] + '-11', col[:4] + '-12']]
                job[name] = supose.mean(axis=1)
    return job

#-------------------------------------------------------------------------------------------------------------
def rename_states(job):
    for i in job.index:
        job.loc[i, 'State'] = states[job.loc[i, 'State']]
    return job

#-------------------------------------------------------------------------------------------------------------
def regroup(job):
    job = (job.drop([coluna for coluna in job.columns if isnumeric(coluna[0]) if coluna[-2] != 'q'], axis=1)
              .set_index(["State","RegionName"]))
    return job

#-------------------------------------------------------------------------------------------------------------
def convert_housing_data_to_quarters():
    """this function return a dataframe formated to generate quarters with the months of the job dataframe"""

    job = get()
    job = sep(job)
    job = rename_states(job)
    job = regroup(job)
    
    return job

def run_ttest():
    """this function make a test to observe if the hipotesis is true. return a boolean value (true or false),
    the pvalue (a float), and a string"""

    lista = get_list_of_university_towns().to_records(index=False).tolist()
    
    new = convert_housing_data_to_quarters().loc[:, ['2008q2', '2009q2']]
    
    new['ratio'] = new['2008q2'].div(new['2009q2'])
    
    g1 = new.loc[new.index.isin(lista)]
    g2 = new.loc[~new.index.isin(lista)]
    
    sta, pvalue = ttest_ind(g1['ratio'], g2['ratio'], nan_policy='omit')
    
    dif = pvalue < 0.01

    if dif:
        better = 'university town'
    else:
        better = 'non-university town'

    return  (dif, pvalue, better)
