import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Dashboard EUII",
                   page_icon=":bar_icon:",
                   layout="wide")
# Coleta de dados do .csv
dados = pd.read_csv(r'SP202102.csv')
#print(dados)
#Variáveis primárias
data= dados['Data'].values
hora=dados['Hora'].values
estacao=dados['Estacao'].values
codigo=dados['Codigo'].values
poluente=dados['Poluente'].values
valor=dados['Valor'].values
#Vetor para cada poluente
CO=np.zeros(len(data))
FMC=np.zeros(len(data))
MP10=np.zeros(len(data))
MP25=np.zeros(len(data))
NO2=np.zeros(len(data))
O3=np.zeros(len(data))
PTS=np.zeros(len(data))
SO2=np.zeros(len(data))

for i in range(0, len(data)):
    if poluente[i]=='CO':
        CO[i]=valor[i]
    elif poluente[i]=='FMC':
        FMC[i]=valor[i]
    elif poluente[i]=='MP10':
        MP10[i]=valor[i]
    elif poluente[i]=='MP2.5':
        MP25[i]=valor[i]
    elif poluente[i]=='NO2':
        NO2[i]=valor[i]
    elif poluente[i]=='O3':
        O3[i]=valor[i]
    elif poluente[i]=='PTS':
        PTS[i]=valor[i]
    else:
        SO2[i]=valor[i]

#Caso queira remover os zeros dos vetores de poluentes
#CO = [i for i in CO if i != 0]
#FMC = [i for i in FMC if i != 0]
#MP10 = [i for i in MP10 if i != 0]
#MP25 = [i for i in MP2.5 if i != 0]
#NO2 = [i for i in NO2 if i != 0]
#O3 = [i for i in O3 if i != 0]
#PTS = [i for i in PTS if i != 0]
#SO2 = [i for i in SO2 if i != 0]
#Comentados pois não sei a utilidade disso ainda

#Variáveis estatísticas
desvpad=np.std(valor)
#print(desvpad)

#st.dataframe(dados)

#Filtros
st.sidebar.header("Filtros:")
local=st.sidebar.multiselect(
    "Selecione a estacao:",
    options=dados['Estacao'].unique(),
    default=dados['Estacao'].unique()
)


selecao=dados.query(
    "Estacao==@local"
)

st.dataframe(selecao)