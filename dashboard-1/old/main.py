# coding=utf-8
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Dashboard EUII",
                   page_icon="🦈",
                   layout="wide",
                   menu_items={
                       'Get Help': 'https://www.extremelycoolapp.com/help',
                       'Report a bug': "https://www.extremelycoolapp.com/bug",
                       'About': "# This is a header. This is an *extremely* cool app!"
                   }
)
st.title('Projeto de Engenharia Unificada II')

# Função para carregar os dados em cache
@st.cache
def load_metadata():
    metadata = pd.read_csv(r'SP202102.csv')
    return metadata

# Declaração da variável
dados = load_metadata()
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

#Filtros no Sidebar
st.sidebar.header("Estacao")
local=st.sidebar.multiselect(
    "Selecione a estacao:",
    options=dados['Estacao'].unique(),
    default=dados['Estacao'].unique()
)

selecao=dados.query(
    "Estacao==@local",
)

st.markdown('### Base de dados:  Qualidade do ar por estações')
st.dataframe(selecao)
st.markdown('---')

# st.plotly_chart(dados, use_container_width=True)




st.title('Visualização Gráfica')
long_df = px.data.medals_long()


@st.cache
def groupbyData(df):
    data = df.groupby(['Estacao']).mean()
    return data

#groupby(['Data','Estacao','Poluente'])['Valor'].transform('sum')
#long_df

data_marilia = dados.query("Estacao == 'Marília'")
# data_estacao_graph = dados.groupby(['Data','Estacao','Poluente'])['Valor'].mean()

data_estacao_poluente = dados.loc[:,['Estacao', 'Poluente']]
fig2 = px.bar(data_estacao_poluente, x='Estacao', y='Poluente')
st.plotly_chart(fig2)


# data = file.groupby(['Data','Estacao','Poluente'])['Valor'].transform('sum')


# multiselect https://docs.streamlit.io/library/api-reference/widgets/st.multiselect
# usada o ploty https://docs.streamlit.io/library/api-reference/charts/st.plotly_chart
# https://plotly.com/python/plotly-express/
# Tutorial: https://datamarte.com/streamlit-construindo-relatorios-e-dashboard-para-data-science-em-python/