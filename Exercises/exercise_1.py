import pandas as pd

                                             #Part 1 - Olympic Games

df = pd.read_csv('olympics.csv', index_col=0, skiprows=1)
for col in df.columns:
    if col[:2]=='01':
        df.rename(columns={col:'Gold'+col[4:]}, inplace=True)
    if col[:2]=='02':
        df.rename(columns={col:'Silver'+col[4:]}, inplace=True)
    if col[:2]=='03':
        df.rename(columns={col:'Bronze'+col[4:]}, inplace=True)
    if col[:1]=='№':
        df.rename(columns={col:'#'+col[1:]}, inplace=True)

names_ids = df.index.str.split('\s\(') #split the index by '('

df.index = names_ids.str[0]            #the [0] element is the country name (new index)
df['ID'] = names_ids.str[1].str[:3]    #the [1] element is the abbreviation or ID (take first 3 characters from that)
df = df.drop('Totals')

#------------------------------------------------------------------------------------------------------
def answer_zero():
    """This function returns the row for Afghanistan, which is a Series object. The assignment
    question description will tell you the general format the autograder is expecting"""
    return df.iloc[0]

#------------------------------------------------------------------------------------------------------
def answer_one():
    """this function returns Which country has won the most gold medals in summer games"""
    most_gold_medals = [i for i in df.index if df.loc[i, 'Gold'] == max(df['Gold'])]
    return most_gold_medals[0]

#------------------------------------------------------------------------------------------------------
def answer_two():
    """this function returns which country had the biggest difference between their summer and winter gold counts"""
    maior = [i for i in df.index if (df.loc[i,'Gold'] - df.loc[i, 'Gold.1']) == max(df['Gold'] - df['Gold.1'])]
    return maior[0]

#------------------------------------------------------------------------------------------------------
df_like = df[(df['Gold']>0) & df['Gold.1']>0]
country_dif_media = lambda country: (df_like.loc[country,'Gold'] - df_like.loc[country,'Gold.1'])/(df_like.loc[country, 'Gold']+df_like.loc[country, 'Gold.1']+df_like.loc[country, 'Gold.2'])

def answer_three():
    """this function return the country who have the biggest difference media between winter and summer gold medal"""
    difference_media = [i for i in df_like.index if country_dif_media(i) == 0.4807692307692308]
    return difference_media[0]

#------------------------------------------------------------------------------------------------------
def get_points():
    values = []
    for ha in df.index:
        parse = int(df.loc[ha, 'Gold.2']*3)
        parse += int(df.loc[ha, 'Silver.2']*2)
        parse += int(df.loc[ha, 'Bronze.2']*1)
        values.append(str(parse))
    return values

#------------------------------------------------------------------------------------------------------
def answer_four():
    """this function creates a Series called "Points" which is a weighted value where each gold medal (`Gold.2`)    counts for 3 points, silver medals (`Silver.2`) for 2 points, and bronze medals (`Bronze.2`) for 1 point. The   function should return only the column (a Series object) which you created, with the country names as           indices."""
    points = pd.Series(get_points(), index=df.index)
    return points



                                               #Part 2 - Census

census_df = pd.read_csv('census.csv')

def answer_five():
    """this function returns Which state has the most counties in it"""
    job = census_df.copy()
    job = job.set_index('STATE')
    nivel = [len(job.loc[i]) for i in job.index.unique()]
    luli = [list(job.loc[i, 'STNAME'][i].unique()) for i in job.index.unique() if len(job.loc[i]) == max(nivel)]
    return luli[0][0]

#------------------------------------------------------------------------------------------------------
def answer_six():
    """this function returns the three most populous states (in order of highest population to lowest population)"""
    df_post = census_df.copy().set_index('STATE')
    pop = [list(df_post.loc[i, 'CENSUS2010POP']) for i in df_post.index.unique()]

    for num in range(len(pop)):
        pop[num] = sorted(pop[num], reverse=True)
        pop[num] = pop[num][1:4]

    three_most = []
    for count in range(3):
        three_most.append(max(pop))
        pop.remove(max(pop))
    organized = [sum(three_most[n]) for n in range(len(three_most))]
    organized = sorted(organized, reverse=True)
    organized = organized[:3]

    df_post = df_post.reset_index()

    states = []
    for nha in organized:
        for n in three_most:
            for i in df_post.index:
                if ((df_post.loc[i, 'CENSUS2010POP'] in n) & (sum(n) == nha)):
                    states.append(df_post.loc[i, 'STNAME'])
                    break
    return states

#------------------------------------------------------------------------------------------------------
census_df = census_df[census_df['SUMLEV'] == 50]
def create_dif(indice):
    current_dif = [census_df.loc[indice, 'POPESTIMATE201{}'.format(str(i))] for i in range(6)]
    current_dif = max(current_dif) - min(current_dif)
    return current_dif

#------------------------------------------------------------------------------------------------------
def solve_problem():
    just_dif = {}
    for i in census_df.index:
        just_dif[census_df.loc[i, 'CTYNAME']] = create_dif(i)
    return [key for key, value in just_dif.items() if value == max(just_dif.values())][0]

#------------------------------------------------------------------------------------------------------
def answer_seven():
    """this function returns which county has had the largest absolute change in population within the period 2010-2015"""
    return solve_problem()

#------------------------------------------------------------------------------------------------------
census_df = census_df[census_df['SUMLEV'] == 50]
def answer_eight():
    """this function returns the counties that belong to regions 1 or 2, whose name starts with 'Washington', and whose POPESTIMATE2015 was greater than their POPESTIMATE 2014"""

    wash_counties = [{'STNAME':census_df.loc[i, 'STNAME'], 'CTYNAME':census_df.loc[i, 'CTYNAME'], 'i': i} for i in census_df.index if ((census_df.loc[i, 'REGION'] == 1) or (census_df.loc[i, 'REGION'] == 2)) if census_df.loc[i, 'CTYNAME'][:10] == 'Washington' if census_df.loc[i, 'POPESTIMATE2015'] > census_df.loc[i, 'POPESTIMATE2014']]

    indices = [k['i'] for k in wash_counties]
    final_df = pd.DataFrame(wash_counties, index=indices)
    final_df = final_df.drop(['i'], axis=1)

    return final_df
