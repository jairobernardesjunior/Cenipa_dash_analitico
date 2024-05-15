from haversine import haversine
from datetime import datetime
from PIL import Image
from streamlit_folium import folium_static
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
import plotly.express as px
import folium

#pd.set_option('display.max_rows', None)
#pd.set_option('display.max_columns', None)
#import warnings
#warnings.simplefilter('ignore')

@st.cache_data
def le_arquivo_analise():
    df_aeronaves = pd.read_csv( 'dataset_analise/df_acidentes_analise_aero.csv' )
    df_aeronaves['ocorrencia_dia'] = pd.to_datetime(df_aeronaves['ocorrencia_dia'])
    return df_aeronaves

@st.cache_data
def seleciona_fabricante(dfx):
    return dfx[['aeronave_fabricante', 'qtde_fabric', 'perc_fabric']].\
        drop_duplicates().sort_values('qtde_fabric', ascending=False)

@st.cache_data
def seleciona_ano_fab(dfx):
    return dfx[['aeronave_ano_fabricacao', 'qtde_ano_fab', 'perc_ano_fab']].\
        drop_duplicates().sort_values('aeronave_ano_fabricacao', ascending=True)




@st.cache_data
def seleciona_tipo_ocorrencia(dfx):
    return dfx[['ocorrencia_tipo', 'qtde_tipo_ocorr', 'perc_tipo_ocorr']].\
        drop_duplicates().sort_values('perc_tipo_ocorr', ascending=False)

@st.cache_data
def agrupa_uf_classificacao(dfx):
    # colunas
    cols = ['ocorrencia_uf', 'ocorrencia_classificacao', 'qtde_classif']

    # selecao de linhas
    dfx = df_aeronaves[['ocorrencia_uf', 'ocorrencia_classificacao']]
    dfx['qtde_classif'] = 0

    dfx = dfx.loc[:, cols].groupby( ['ocorrencia_uf', 'ocorrencia_classificacao']).count().reset_index()
    return dfx.sort_values(['ocorrencia_uf'], ascending=False)    

@st.cache_data
def seleciona_saida_pista_aerodromo(dfx):
    dfx = dfx[['ocorrencia_cidade', 'ocorrencia_aerodromo', 'qtde_saip_aerod', 'qtde_saip_total']].\
        sort_values('qtde_saip_aerod', ascending=False)
    dfx = dfx.drop_duplicates().dropna()
    dfx = dfx[(dfx['qtde_saip_aerod'] > 0) & 
              (dfx['ocorrencia_aerodromo'] != '***') &
              (dfx['ocorrencia_aerodromo'] != '****') &
              (dfx['ocorrencia_aerodromo'] != '**NI')]
    dfx['cidade_aerodromo'] = dfx['ocorrencia_cidade'] + ' - ' + dfx['ocorrencia_aerodromo']

    return dfx

#------------------- INÍCIO
df_aeronaves = le_arquivo_analise()

#----------------------------------------------
# Barra lateral sidebar
#----------------------------------------------
#-------- define a cor
st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color: #8390EC;
    }
</style>
""", unsafe_allow_html=True)

#-------- Carrega imagem
image_path = './images/aviao3.jpg'
ix = Image.open( image_path ) 
st.sidebar.image( ix, width=240 )

#-------- Empresa
st.sidebar.markdown( '# Análise e Predição')
st.sidebar.markdown( '### Powered by i4x.Data')

#----------------------------------------------
# Layout de dados
#----------------------------------------------
#-------- Dados Gerais
st.title( 'Visão de Aeronaves' )

with st.container():
    st.header( 'Métricas Gerais' )

    col1, col2 = st.columns( 2, gap='Large')

    with col1:
        #  data inicial
        col1.metric( 'Data Inicial', df_aeronaves.loc[:, 'ocorrencia_dia'].min().strftime("%d/%m/%Y") )            

    with col2:
        # data final
        col2.metric( 'Data Final', df_aeronaves.loc[:, 'ocorrencia_dia'].max().strftime("%d/%m/%Y") ) 

with st.container():

    col1, col2, col3 = st.columns( 3, gap='Large')
    with col1:
        # total de aeronaves envolvidas
        col1.metric( 'Total de Aeronaves', len(pd.unique(df_aeronaves['aeronave_matricula'])) )               

    with col2:
        # total de modelos envolvidos
        col2.metric( 'Qtde de Modelos', len(pd.unique(df_aeronaves['aeronave_modelo'])) )   

    with col3:
        # total de tipos de veículo
        col3.metric( 'Qtde de Tipos de Veículos', len(pd.unique(df_aeronaves['aeronave_tipo_veiculo'])) )   

#----------------------------------------------
# gráficos
#----------------------------------------------
#-------- Abas de finalidade dos dados
tab1, tab2, tab3 = st.tabs( ['Visão Estratégica', 'Visão Tática', '-'])

#-------- Visão Estratégica
with tab1:
    with st.container():
        # Quantidade de Aeronaves por Fabricante
        st.header( 'Quantidade de Aeronaves por Fabricante' )   

        dfx = seleciona_fabricante(df_aeronaves)

        #-------- Controle de dados dupla face
        intervalo = st.slider('Selecione o intervalo de quantidade',
                            0.0, 100.0, (6.0, 100.0))
        st.write('Intervalo Selecionado:',intervalo)    

        df_aux = dfx[(dfx['qtde_fabric'] >= intervalo[0]) & (dfx['qtde_fabric'] < intervalo[1])]

        fig = px.bar ( df_aux, x='qtde_fabric', y='aeronave_fabricante', title='Aeronaves/Fabricante',                      
                       labels={
                            "qtde_fabric": "Quantidade",
                            "aeronave_fabricante": "Fabricante",
                              },                     
                     )
        fig.update_traces(width=0.8)
        fig.update_yaxes(tickfont=dict(size=8))
        fig.update_xaxes(tickfont=dict(size=8))

        fig.update_traces(marker_color='red')
        fig.update_layout(width=700, height=500, bargap=0.05)        

        st.plotly_chart( fig, use_container_width=True)                                   

#-------- Visão Tática
with tab2:
    with st.container():
        # Quantidade de Aeronaves por Ano de Fabricação
        st.header( 'Quantidade de Aeronaves por Ano de Fabricação' )   

        dfx = seleciona_ano_fab(df_aeronaves)
        dfx = dfx[(dfx['aeronave_ano_fabricacao'] > 0) & (dfx['aeronave_ano_fabricacao'] < 3000)]

        #-------- Controle de dados dupla face
        min= dfx.loc[:, 'aeronave_ano_fabricacao'].min()/10
        max= dfx.loc[:, 'aeronave_ano_fabricacao'].max()/10
        min= min*10
        max= max*10

        intervalo = st.slider('Selecione o intervalo de ano',
                            min, max, (1980.0, max))
        st.write('Intervalo Selecionado:',intervalo)    

        df_aux = dfx[(dfx['aeronave_ano_fabricacao'] >= intervalo[0]) & (dfx['aeronave_ano_fabricacao'] < intervalo[1])]

        fig = px.bar ( df_aux, x='aeronave_ano_fabricacao', y='qtde_ano_fab', title='Ano/Fabricação',                      
                       labels={
                            "qtde_ano_fab": "Quantidade",
                            "aeronave_ano_fabricacao": "Ano",
                              },                     
                     )
        fig.update_traces(width=0.8)
        fig.update_yaxes(tickfont=dict(size=8))
        fig.update_xaxes(tickfont=dict(size=8))

        fig.update_traces(marker_color='green')
        fig.update_layout(width=700, height=500, bargap=0.05)        

        st.plotly_chart( fig, use_container_width=True)          