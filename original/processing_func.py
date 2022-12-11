#!/usr/bin/env python
# coding: utf-8

# In[1]:


import itertools


# In[2]:


def score_f(row):
    return (3*row.kills) + (2*row.assists) + (0.02*row['total cs']) + (2*row.firstbloodkill) + (2*(row.triplekills-row.quadrakills)) + (4*(row.quadrakills-row.pentakills)) + (7*row.pentakills) - row.deaths


# In[3]:


def processor(df):
    df.dropna(subset=['playerid'], inplace=True)
    
    df['score'] = df.apply(lambda row: score_f(row), axis=1)
    
    sides = list(df.side.unique())
    positions = list(df.position.unique())
    s_p = list(itertools.product(sides, positions))

    days = df.date.unique()
    days_df = pd.DataFrame(days, columns=['date'])
    days_df.sort_values('date')

    play_cols = []

    for i in s_p:
        temp = df[(df.side == i[0]) & (df.position == i[1])][['date', 'playerid']]
        days_df = pd.merge(days_df, temp, left_on='date', right_on='date', how='left')
        days_df.rename(columns={'playerid':i[0]+i[1]}, inplace=True)
        play_cols.append(i[0]+i[1])
        
    aggs= df.groupby(['playerid', 'date'])[['kills', 'deaths', 'assists', 'total cs', 'score',
                                           'firstbloodkill', 'triplekills', 'quadrakills', 'pentakills']].sum()

    cols = list(aggs.columns)
    renamer = {}
    for col in cols:
        renamer[col] = 'average_'+col
    renamer['total cs'] = 'average_cs'

    games = df.groupby(['playerid', 'date'])[['playerid']].count()
    aggs = pd.merge(aggs, games, left_index=True, right_index=True, how='inner')

    renamer['playerid'] = 'total_games'

    aggs = aggs.groupby(level=0).cumsum().rename(columns=renamer)
    aggs = aggs.groupby(level=0).shift(1)

    for i in renamer.values():
        if i != 'total_games':
            aggs[i] = aggs[i]/aggs['total_games']

    aggs['total_games'].fillna(0, inplace=True)
    aggs.fillna(-1, inplace=True)
    agg_cols = list(aggs.columns)
    aggs.reset_index(inplace=True)
    
    days_df = days_df.reindex(columns = list(days_df.columns)+agg_cols+['score'])
    
    scores = df.groupby(['playerid', 'date'])[['score']].sum().reset_index()

    for col in play_cols:

        days_df = pd.merge(days_df, aggs, left_on=[col, 'date'], right_on=['playerid', 'date'],
                           how='left', suffixes=('','_'+col )).drop(columns='playerid')

        days_df = pd.merge(days_df, scores,
                           left_on=[col, 'date'], right_on=['playerid', 'date'],
                           how='left', suffixes=('','_'+col )).drop(columns='playerid')

    drop_cols = agg_cols + play_cols +['date', 'score']    
    days_df.drop(columns=drop_cols, inplace=True)

    return days_df


# In[ ]:




