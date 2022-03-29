#%%
import os
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

plt.style.use(['science.mplstyle','scatter.mplstyle'])

#%%
@st.cache(ttl=3600, show_spinner=True)
def load_data():
    databases = [i for i in os.listdir('data') if i.endswith('.csv')]
    df = pd.DataFrame()
    for database in databases:
        df = pd.concat([df, pd.read_csv('data/' + database, encoding='latin-1')])
        df['Data'] = pd.to_datetime(df['Data'])
    return df

dataframe = load_data()


#%%
def plot_poluentes(station, pollutant):
    if len(station)*len(pollutant) > 0:
        if (len(station) > 1) and ('Todas' not in station) and (len(pollutant) == 1) and ('Todos' not in pollutant):
            dataframe_filtered = dataframe[dataframe['Poluente'].apply(lambda x: x in pollutant)]
            dataframe_filtered = dataframe_filtered[dataframe_filtered['Estacao'].apply(lambda x: x in station)]

            fig, axs = plt.subplots(1,1, figsize=(3.5+0.5*len(dataframe_filtered['Estacao'].unique()), 2.625))
            for n, poluente in enumerate(dataframe_filtered.groupby('Estacao')):
                size = len(poluente[1])
                axs.scatter(np.ones(size)*n+np.random.randn(size)*.05, poluente[1]['Valor'], alpha=.2)
                axs.errorbar(n, poluente[1]['Valor'].mean(), yerr=poluente[1]['Valor'].std(), capsize=2, color='k', marker='o', alpha=.7)
            
            axs.set_xticks(range(len(dataframe_filtered['Estacao'].unique())))
            axs.set_xticklabels(np.unique(dataframe_filtered['Estacao']), rotation=45, ha='right')
            axs.set_title(pollutant[0])
            axs.set_ylabel(dataframe_filtered['Unidade'].iloc[0])
            axs.grid(linestyle='dashed', alpha=.3)
            return fig

        elif (len(station) == 1) and ('Todas' not in station) and (len(pollutant) > 1 or 'Todos' in pollutant):
            dataframe_filtered = dataframe[dataframe['Estacao'].apply(lambda x: x in station)]
            if 'Todos' not in pollutant: dataframe_filtered = dataframe_filtered[dataframe_filtered['Poluente'].apply(lambda x: x in pollutant)]

            fig, axs = plt.subplots(1,1, figsize=(3.5+0.5*len(dataframe_filtered['Poluente'].unique()), 2.625))
            for n, poluente in enumerate(dataframe_filtered.groupby('Poluente')):
                size = len(poluente[1])
                axs.scatter(np.ones(size)*n+np.random.randn(size)*.05, poluente[1]['Valor'], alpha=.2)
                axs.errorbar(n, poluente[1]['Valor'].mean(), yerr=poluente[1]['Valor'].std(), capsize=2, color='k', marker='o', alpha=.7)
            
            axs.set_xticks(range(len(dataframe_filtered['Poluente'].unique())))
            axs.set_xticklabels(np.unique(dataframe_filtered['Poluente']), rotation=45, ha='right')
            axs.set_title(station[0])
            axs.set_ylabel(dataframe_filtered['Unidade'].iloc[0])
            axs.grid(linestyle='dashed', alpha=.3)
            return fig

        elif ('Todas' in station) and ('Todos' not in pollutant):
            dataframe_filtered = dataframe[dataframe['Poluente'].apply(lambda x: x in pollutant)]

            fig, axs = plt.subplots(1,1, figsize=(2.625, 3.5+0.15*len(dataframe_filtered['Estacao'].unique())))
            for n, poluente in enumerate(dataframe_filtered.groupby('Estacao')):
                size = len(poluente[1])
                axs.scatter(poluente[1]['Valor'], np.ones(size)*n+np.random.randn(size)*.05, alpha=.2)
                axs.errorbar(poluente[1]['Valor'].mean(), n, xerr=poluente[1]['Valor'].std(), capsize=2, color='k', marker='o', alpha=.7)
            
            axs.set_yticks(range(len(dataframe_filtered['Estacao'].unique())))
            axs.set_yticklabels(np.unique(dataframe_filtered['Estacao']), ha='right')
            axs.set_title(pollutant[0])
            axs.set_xlabel(dataframe_filtered['Unidade'].iloc[0])
            axs.grid(linestyle='dashed', alpha=.3)
            return fig

        elif ('Todas' in station) and ('Todos' in pollutant):
            for poluente in dataframe.groupby('Poluente'):
                dataframe_filtered = poluente[-1]
                fig, axs = plt.subplots(1,1, figsize=(2.625, 3.5+0.15*len(dataframe_filtered['Estacao'].unique())))
                for n, estacao in enumerate(dataframe_filtered.groupby('Estacao')):
                    size = len(estacao[1])
                    axs.scatter(estacao[1]['Valor'], np.ones(size)*n+np.random.randn(size)*.05, alpha=.2)
                    axs.errorbar(estacao[1]['Valor'].mean(), n, xerr=estacao[1]['Valor'].std(), capsize=2, color='k', marker='o', alpha=.7)
                
                axs.set_yticks(range(len(dataframe_filtered['Estacao'].unique())))
                axs.set_yticklabels(np.unique(dataframe_filtered['Estacao']), ha='right')
                axs.set_title(poluente[0])
                axs.set_xlabel(dataframe_filtered['Unidade'].iloc[0])
                axs.grid(linestyle='dashed', alpha=.3)
                st.pyplot(fig)

def plot_time_series(start_date, end_date, pollutant, station):
    dataframe_filtered = dataframe.copy()
    if 'Todos' not in pollutant: dataframe_filtered = dataframe_filtered[dataframe_filtered['Poluente'].apply(lambda x: x in pollutant)]
    if 'Todas' not in pollutant: dataframe_filtered = dataframe_filtered[dataframe_filtered['Estacao'].apply(lambda x: x in station)]
    dataframe_filtered = dataframe_filtered[dataframe_filtered['Data'].apply(lambda x: start_date <= x.date() <= end_date)]
    fig, axs = plt.subplots(1,1, figsize=(7, 2.625))
    for poluente in dataframe_filtered.groupby('Poluente'):
        for estacao in poluente[-1].groupby('Estacao'):
            axs.plot(np.unique(estacao[-1]['Data']), estacao[-1].groupby('Data')['Valor'].mean(), linestyle='-')
    return fig
    

def app():
    st.title("Visulização dos Poluentes")
    st.header("Distribuição de Dados")
    row0_1, row0_2 = st.columns(2)
    with row0_1:
        selected_station = st.multiselect('Selecione as estações de interesse', ['Todas']+list(dataframe['Estacao'].unique()), ['Campinas - Centro'])
    with row0_2:
        selected_pollutant = st.multiselect('Selecione os poluentes de interesse', ['Todos']+list(dataframe['Poluente'].unique()), ['Todos'])
    _, row1, _ = st.columns((.35, 1, .35))
    with row1:
        fig = plot_poluentes(selected_station, selected_pollutant)
        st.pyplot(fig)
    
    st.header("Série Temporal")
    start_date, end_date = st.select_slider(
     'Selecione o período',
     options=[i.date() for i in pd.to_datetime(np.unique(dataframe['Data']))],
     value=(dataframe['Data'].min().date(), dataframe['Data'].max().date()))
    fig = plot_time_series(start_date, end_date, selected_pollutant, selected_station)
    st.pyplot(fig)