import pandas as pd
import numpy as np
"""
                                        Question 1 Description
                                        
Load the energy data from the file `Energy Indicators.xls`, which is a list of indicators of [energy supply and renewable electricity production](Energy%20Indicators.xls) from the [United Nations]and should be put into a DataFrame with the variable name of energy

Keep in mind that this is an Excel file, and not a comma separated values file. Also, make sure to exclude the footer and header information from the datafile. The first two columns are unneccessary, so you should get rid of them, and you should change the column labels so that the columns are:
 ['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']
 
Convert `Energy Supply` to gigajoules (there are 1,000,000 gigajoules in a petajoule). For all countries which have missing data (e.g. data with "...") make sure this is reflected as `np.NaN` values.

 Rename the following list of countries (for use in later questions):

 ```"Republic of Korea": "South Korea",
 "United States of America": "United States",
 "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
 "China, Hong Kong Special Administrative Region": "Hong Kong"```

 There are also several countries with numbers and/or parenthesis in their name. Be sure to remove these, 

e.g. 
`'Bolivia (Plurinational State of)'` should be `'Bolivia'`, 
`'Switzerland17'` should be `'Switzerland'`.

Next, load the GDP data from the file `world_bank.csv`, which is a csv containing countries' GDP from 1960 to 2015 from [World Bank](http://data.worldbank.org/indicator/NY.GDP.MKTP.CD). Call this DataFrame **GDP**. 

Make sure to skip the header, and rename the following list of countries:

```"Korea, Rep.": "South Korea", 
"Iran, Islamic Rep.": "Iran",
"Hong Kong SAR, China": "Hong Kong"```


Finally, load the file `scimagojr-3.xlsx`, which ranks countries based on their journal contributions in the aforementioned area. Call this DataFrame ScimEn.

Join the three datasets: GDP, Energy, and ScimEn into a new dataset (using the intersection of country names). Use only the last 10 years (2006-2015) of GDP data and only the top 15 countries by Scimagojr 'Rank' (Rank 1 through 15). 
 
The index of this DataFrame should be the name of the country, and the columns should be ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations',
       'Citations per document', 'H index', 'Energy Supply',
       'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008',
       '2009', '2010', '2011', '2012', '2013', '2014', '2015'].

"""

countries_off = ['American Samoa', 'Guam', 'Northern Mariana Islands', 'Tuvalu','United States Virgin Islands']
ta = 0
def rename_columns(item):
    if item[-1] == 'y':
        return 'Country'
    elif item[-1] == '3':
        return 'Energy Supply'
    elif item[-1] == '4':
        return 'Energy Supply per Capita'
    return '% Renewable'

#----------------------------------------------------------------------------------------------------------------
def fun(item):
    if item == 'Data Source':
        return ta[0]
    if item == 'World Development Indicators':
        return ta[1]
    if (int(item[-1])) < 10 and (not item[-2].isdigit()):
        if(int(item[-1]) <= 3):
            return ta[int(item[-1])]
        else:
            return str(int(ta[int(item[-1])]))
    else:
        num = int(item[-2]+item[-1])
        return str(int(ta[num]))

#----------------------------------------------------------------------------------------------------------------
def create_energy():
    energy = pd.read_excel('Energy Indicators.xls')
    energy = (energy.drop(range(16))
              .drop(range(243, 281))
              .drop(['Unnamed: 0', 'Unnamed: 1'], axis=1)
              .rename(columns=dict(zip(energy.columns, (rename_columns(i) for i in energy.columns))))
              .reset_index()
              .drop('index', axis=1))
    for item in energy.index:
        for lol in energy.loc[item, 'Country']:
            if lol.isdigit():
                energy.loc[item, 'Country'] = energy.loc[item, 'Country'].replace(lol, '')

        if '(' in energy.loc[item, 'Country']:
            num = energy.loc[item, 'Country'].index('(')
            energy.loc[item, 'Country'] = energy.loc[item, 'Country'][:num].rstrip()
            
        if (energy.loc[item, 'Country'] in countries_off):
            energy.loc[item, 'Energy Supply per Capita'] = np.NAN
            energy.loc[item, 'Energy Supply'] = np.NAN
            
        if energy.loc[item, 'Country'] == 'Republic of Korea':
            energy.at[item, 'Country'] = 'South Korea'
        elif energy.loc[item, 'Country'] == 'United States of America':
            energy.at[item, 'Country'] = 'United States'
        elif energy.loc[item, 'Country'] == 'United Kingdom of Great Britain and Northern Ireland':
            energy.at[item, 'Country'] = 'United Kingdom'
        elif energy.loc[item, 'Country'] == 'China, Hong Kong Special Administrative Region':
            energy.at[item, 'Country'] = 'Hong Kong'
            
    energy['Energy Supply'] = energy['Energy Supply']*1000000
    energy['Energy Supply per Capita'] = pd.to_numeric(energy['Energy Supply per Capita'])
    energy['Energy Supply'] = pd.to_numeric(energy['Energy Supply'])
    energy['% Renewable'] = pd.to_numeric(energy['% Renewable'])
    
    return energy.sort_values(by=['Country'])

#----------------------------------------------------------------------------------------------------------------
def create_GDP():
    global ta
    GDP = pd.read_csv('world_bank.csv')
    ta = GDP.loc[3].values
    GDP = (GDP.drop(range(4))
           .rename(columns=dict(zip(GDP.columns, (fun(i) for i in GDP.columns))))
           .rename(columns={'Country Name':'Country'})
           .set_index('Country')
           .rename(index={"Korea, Rep.": "South Korea",
                          "Iran, Islamic Rep.": "Iran",
                          "Hong Kong SAR, China": "Hong Kong"})
           .reset_index()
           .sort_values(by=['Country'])
           .loc[:, ['Country', '2006', '2007','2008','2009','2010','2011','2012','2013','2014', '2015']]
           .reset_index()
           .drop('index', axis=1))
    return GDP

#----------------------------------------------------------------------------------------------------------------
def create_ScimEn():
    ScimEn = pd.read_excel('scimagojr-3.xlsx')
    return ScimEn

#----------------------------------------------------------------------------------------------------------------
def answer_one():
    energy = create_energy()
    GDP = create_GDP()
    ScimEn = create_ScimEn()
    result = (pd.merge(energy, ScimEn, how='inner', left_on='Country', right_on='Country')
              .sort_values(by='Rank')
              .set_index('Country'))


    result = (pd.merge(result, GDP, how='inner', left_index=True, right_on='Country')
              .set_index('Country')
              .sort_values(by='Rank'))
    
    res = (result.where(result['Rank'] <= 15)
           .reset_index()
           .drop(range(15, len(result)))
           .sort_values(by='Rank')
           .set_index('Country'))

    return res

#----------------------------------------------------------------------------------------------------------------
def answer_two():
    """this function returns how many entries you lose when you joined the three datasets"""
    energy, GDP, ScimEn = create_energy(),create_GDP(),create_ScimEn()
    tdf_in = pd.merge(energy, GDP, how='inner', on='Country')
    tdf_in = pd.merge(tdf_in, ScimEn, how='inner', on='Country')
    
    tdf_out = pd.merge(energy, GDP, how='outer', on='Country')
    tdf_out = pd.merge(tdf_out, ScimEn, how='outer', on='Country')
    return len(tdf_out) - len(tdf_in)

#----------------------------------------------------------------------------------------------------------------
def avg(row):
    data = row[['2006',
                '2007',
                '2008',
                '2009',
                '2010',
                '2011',
                '2012',
                '2013',
                '2014',
                '2015']].dropna()
    return pd.Series({'Country':row['Country'], 'avg': np.sum(data)/len(data)})

#----------------------------------------------------------------------------------------------------------------
def answer_three():
    """this function returns what is the average GDP over the last 10 years for each country"""
    Top15 = answer_one()
    avgGDP = Top15.reset_index().apply(avg, axis=1)
    avgGDP = pd.Series(avgGDP['avg'].values, avgGDP['Country']).sort_values(ascending=False)
    return avgGDP

#----------------------------------------------------------------------------------------------------------------
def delta(row):
    if row['Country'] == 'United Kingdom':
        data = row[['2006',
                    '2007',
                    '2008',
                    '2009',
                    '2010',
                    '2011',
                    '2012',
                    '2013',
                    '2014',
                    '2015']].dropna()
        return pd.Series({'delta': data['2015'] - data['2006']})

#----------------------------------------------------------------------------------------------------------------
def answer_four():
    """this function returns by how much had the GDP changed over the 10 year span for the country with the 6th largest average GDP"""
    Top15 = answer_one()
    deltaa = Top15.reset_index().apply(delta, axis=1).dropna().reset_index().drop('index', axis=1)
    return np.float64(deltaa.iloc[0, 0])

#----------------------------------------------------------------------------------------------------------------
def answer_five():
    """this function returns what is the mean 'Energy Supply per Capita' """
    Top15 = answer_one()
    Top15 = Top15['Energy Supply per Capita'].values
    return float(np.mean(Top15))

#----------------------------------------------------------------------------------------------------------------
def answer_six():
    """this function returns what country has the maximun %Renewable and what is the percentage"""
    Top15 = answer_one()
    for country in Top15.index:
        if Top15.loc[country, '% Renewable'] == max(Top15['% Renewable']):
            return (country, Top15.loc[country, '% Renewable'])

#----------------------------------------------------------------------------------------------------------------
def answer_seven():
    """this function creates a new column that is the ratio of Self-citations to Total Citations"""
    Top15 = answer_one()
    Top15['Ratio'] = Top15['Self-citations']/Top15['Citations']
    for country in Top15.index:
        if Top15.loc[country, 'Ratio'] == max(Top15['Ratio']):
            return (country, Top15.loc[country, 'Ratio'])

#----------------------------------------------------------------------------------------------------------------
def answer_eight():
    """this function creates a column that estimates the population using Energy Supply and Energy Supply per capita and returns what is the third most populous country according to this estimate"""

    Top15 = answer_one()
    Top15['Population'] = Top15['Energy Supply']/Top15['Energy Supply per Capita']
    Top15 = Top15.sort_values(by=['Population'], ascending=False).reset_index()
    return Top15.loc[2, 'Country']

#----------------------------------------------------------------------------------------------------------------
def answer_nine():
    """this function create a column that estimates the number of citable documents per person and return what is the correlation between the number of citable documents per capita and the energy supply per capita"""

    Top15 = answer_one()
    Top15['Population'] = Top15['Energy Supply']/Top15['Energy Supply per Capita']
    Top15['citable per capita'] = Top15['Citable documents']/Top15['Population']
    Top15 = Top15.loc[:, ['citable per capita', 'Energy Supply per Capita']].corr(method='pearson')
    return Top15.loc['citable per capita', 'Energy Supply per Capita']

#----------------------------------------------------------------------------------------------------------------
def answer_ten():
    """this function create a new column with a 1 if the country's % Renewable value is at or above the median for all countries in the top 15, and a 0 if the country's % Renewable value is below the median"""

    Top15 = answer_one()
    media = Top15['% Renewable'].median()
    for country in Top15.index:
        if Top15.loc[country, '% Renewable'] >= media:
            Top15.loc[country, 'HighRenew'] = 1
        else:
             Top15.loc[country, 'HighRenew'] = 0
    HighRenew = pd.Series(Top15['HighRenew'])
    return HighRenew

#----------------------------------------------------------------------------------------------------------------
ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
def group(item):
    return ContinentDict[item]

#----------------------------------------------------------------------------------------------------------------
def answer_eleven():
    """this function use the continentDict to group the Countries by Continent, then create a dateframe that displays the sample size (the number of countries in each continent bin), and the sum, mean, and std deviation for the estimated population of each country"""

    Top15 = answer_one()
    Top15['estimated population'] = Top15['Energy Supply']/Top15['Energy Supply per Capita']
    new = pd.DataFrame()
    for continent, df in Top15.groupby(group):
        new.loc[continent, 'size'] = len(df.index)
        new.loc[continent, 'sum'] = df['estimated population'].sum()
        new.loc[continent, 'mean'] = df['estimated population'].mean()
        new.loc[continent, 'std'] = df['estimated population'].std()
        
    return new