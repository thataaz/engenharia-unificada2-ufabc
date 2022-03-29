#%% 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

plt.rcParams['figure.facecolor'] = 'white'

#%%
databases = [i for i in os.listdir('data') if i.endswith('.csv')]
df = pd.DataFrame()

for database in databases:
    df = pd.concat([df, pd.read_csv('data/' + database, encoding='latin-1')])

# %%
campinas = df[df['Estacao'].apply(lambda x: 'campinas' in x.lower())]

for cidade in df.groupby('Estacao'):
    print(cidade[0])
    fig, axs = plt.subplots(1,1, figsize=(6,6))
    cidade[1].boxplot(by='Poluente', column='Valor', axs=axs)
    axs.title(cidade[0])
    for poluente in cidade[1].groupby('Poluente'):
        print(poluente[0], poluente[1]['Valor'].mean(), poluente[1]['Valor'].std(), poluente[1]['Unidade'].iloc[0])
# %%
for poluente in df.groupby('Poluente'):
    fig, axs = plt.subplots(1,1, figsize=(6+0.5*len(poluente[1].Estacao.unique()),6))
    for n, cidade in enumerate(poluente[1].groupby('Estacao')):
        size = len(cidade[1])
        axs.scatter(np.ones(size)*n+np.random.randn(size)*.05, cidade[1]['Valor'], alpha=.2)
        axs.errorbar(n, cidade[1]['Valor'].mean(), yerr=cidade[1]['Valor'].std()*3, capsize=2, color='k', marker='o', alpha=.7)
    axs.set_xticks(range(len(poluente[1]['Estacao'].unique())))
    axs.set_xticklabels(np.unique(poluente[1]['Estacao']), rotation=45, ha='right')
    axs.set_title(poluente[0])
    axs.set_ylabel(poluente[1]['Unidade'].iloc[0])
    axs.grid(linestyle='dashed', alpha=.3)
    plt.savefig(f'{poluente[0]}.png', bbox_inches='tight', dpi=300)
# %%
medias = {}
for poluente in df.groupby('Poluente'):
    medias[poluente[0]] = []
    for estacao in poluente[1].groupby('Estacao'):
        medias[poluente[0]].append(estacao[1]['Valor'].mean())

stds = {}
for poluente in df.groupby('Poluente'):
    stds[poluente[0]] = []
    for estacao in poluente[1].groupby('Estacao'):
        stds[poluente[0]].append(estacao[1]['Valor'].std())

for k,v in medias.items():
    print(k, np.mean(v)+3*np.mean(stds[k]))