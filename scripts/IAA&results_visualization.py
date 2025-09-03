# -*- coding: utf-8 -*-
"""
Created on Wed Jun 25 10:38:44 2025

@author: KeliDu
"""

from statsmodels.stats import inter_rater as irr
import pandas as pd
import os
import seaborn as sns
from matplotlib import pyplot as plt

os.chdir(r'C:\Workstation\Trier\conferences\CHR2025\annotations')

def fleiss_kappa(df): 
    dats, cats = irr.aggregate_raters(df)
    fleiss_kappa = irr.fleiss_kappa(dats, method='fleiss')
    return fleiss_kappa

genres = ['scifi', 'lovestory', 'historical', 'detective']

all_results = []

for genre in genres:
    #df = pd.read_csv(r'combined_LDATopics_' + genre + '.csv', sep='\t')
    #df = pd.read_csv(r'combined_NMFTopics_' + genre + '_50topics.csv', sep='\t')
    df = pd.read_csv(r'combined_BERTopics_' + genre + '_chunk_5000.csv', sep='\t')
    df = df.head(10)
    df = df.fillna('None')
    df_interpretable = df[['interpretable?_BC', 'interpretable?_phi4', 'interpretable?_JR']]#, 'interpretable?_LV']]#, 'interpretable?_phi4']]
    df_category = df[['category_BC', 'category_phi4', 'category_JR']]#, 'category_LV']]#, 'category_phi4']]
    IAA_interpretable = fleiss_kappa(df_interpretable)
    IAA_category = fleiss_kappa(df_category)
    #all_results.append(('LDATopics', genre, IAA_interpretable, IAA_category))
    #all_results.append(('NMFTopics', genre, IAA_interpretable, IAA_category))
    all_results.append(('BERTopics', genre, IAA_interpretable, IAA_category))
    #all_results.append(('LDATopics', genre, 'JR_phi4', IAA_interpretable, IAA_category))
    #all_results.append(('NMFTopics', genre, 'JR_phi4', IAA_interpretable, IAA_category))
    #all_results.append(('BERTopics', genre, 'JR_phi4', IAA_interpretable, IAA_category))

IAA_all = pd.DataFrame(all_results, columns=['topic_model', 'genre', 'IAA_interpretable?', 'IAA_category'])
#IAA_all = pd.DataFrame(all_results, columns=['topic_model', 'genre', 'comparison', 'IAA_interpretable?', 'IAA_category'])

visual = IAA_all.melt(id_vars=['topic_model', 'genre'], value_vars=['IAA_interpretable?', 'IAA_category'], var_name='annotation', value_name='Fleiss_kappa')
#visual = IAA_all.melt(id_vars=['topic_model', 'genre', 'comparison'], value_vars=['IAA_interpretable?', 'IAA_category'], var_name='annotation', value_name='Fleiss_kappa')
visual.to_csv(r'C:\Workstation\Trier\conferences\CHR2025\IAA_results.csv', sep='\t', index=False)

to_visual = visual[visual['annotation'] == 'IAA_category']

g = sns.FacetGrid(visual, col="genre", col_wrap=2, height=4, aspect=1.5)
g.map_dataframe(sns.barplot, x="annotation", y="Fleiss_kappa", hue="topic_model", palette='colorblind')#, dodge=True).set(yscale = 'log')
g.add_legend()
plt.show()



######################################################################################################################
import seaborn.objects as so

df = pd.read_csv(r'C:\Workstation\Trier\conferences\CHR2025\annotation_unified.csv', sep='\t')
df = df.fillna('none')

df_interpretable = df[['interpretable', 'topic_model', 'genre']]


(
    so.Plot(df_interpretable, x="topic_model", alpha="interpretable", color='interpretable')
    .facet("genre", wrap=2)
    .add(so.Bars(), so.Hist(binwidth=50), so.Stack())
    .layout(size=(10, 10))
    .scale(color="colorblind")
)

df_category = df[['category', 'topic_model', 'genre']]
df_category = df_category[df_category['category'] != "none"]


(
    so.Plot(df_category, x="topic_model", alpha="category", color='category')
    .facet("genre", wrap=2)
    .add(so.Bars(), so.Hist(binwidth=50), so.Stack())
    .layout(size=(10, 10))
    .scale(color="colorblind")
)




























