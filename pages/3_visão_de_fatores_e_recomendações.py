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
    df_fator_recomendacao = pd.read_csv( 'dataset_analise/df_acidentes_analise_fator_recomendacao.csv' )
    df_fator_recomendacao['ocorrencia_dia'] = pd.to_datetime(df_fator_recomendacao['ocorrencia_dia'])
    return df_fator_recomendacao

@st.cache_data
def seleciona_fator_nome(dfx):
    return dfx[['fator_nome', 'qtde_fator_nome', 'perc_fator_nome']].\
        drop_duplicates().sort_values('qtde_fator_nome', ascending=False)

@st.cache_data
def seleciona_fator_area(dfx):
    return dfx[['fator_area', 'qtde_area', 'perc_area']].\
        drop_duplicates().sort_values('qtde_area', ascending=False)





@st.cache_data
def seleciona_tipo_ocorrencia(dfx):
    return dfx[['ocorrencia_tipo', 'qtde_tipo_ocorr', 'perc_tipo_ocorr']].\
        drop_duplicates().sort_values('perc_tipo_ocorr', ascending=False)

@st.cache_data
def agrupa_uf_classificacao(dfx):
    # colunas
    cols = ['ocorrencia_uf', 'ocorrencia_classificacao', 'qtde_classif']

    # selecao de linhas
    dfx = df_fator_recomendacao[['ocorrencia_uf', 'ocorrencia_classificacao']]
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
df_fator_recomendacao = le_arquivo_analise()

#----------------------------------------------
# Barra lateral sidebar
#----------------------------------------------
#-------- define a cor
st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color: #CBCBC8;
    }
</style>
""", unsafe_allow_html=True)

#-------- Carrega imagem
image_path = './images/aviao4.jpg'
ix = Image.open( image_path ) 
st.sidebar.image( ix, width=240 )

#-------- Empresa
st.sidebar.markdown( '# Análise e Predição')
st.sidebar.markdown( '### Powered by i4x.Data')

#----------------------------------------------
# Layout de dados
#----------------------------------------------
#-------- Dados Gerais
st.title( 'Visão de Fatores e Recomendações' )

with st.container():
    st.header( 'Métricas Gerais' )

    col1, col2 = st.columns( 2, gap='Large')

    with col1:
        #  data inicial
        col1.metric( 'Data Inicial', df_fator_recomendacao.loc[:, 'ocorrencia_dia'].min().strftime("%d/%m/%Y") )            

    with col2:
        # data final
        col2.metric( 'Data Final', df_fator_recomendacao.loc[:, 'ocorrencia_dia'].max().strftime("%d/%m/%Y") ) 

#----------------------------------------------
# gráficos
#----------------------------------------------
#-------- Abas de finalidade dos dados
tab1, tab2, tab3 = st.tabs( ['Visão Estratégica', 'Visão Tática', '-'])

#-------- Visão Estratégica
with tab1:
    with st.container():
        # Percentual de Fatores Contribuintes
        st.header( 'Percentual de Fatores Contribuintes' )   

        df_aux = seleciona_fator_nome(df_fator_recomendacao)

        fig = px.pie( df_aux, values='perc_fator_nome', names='fator_nome', title='Fator Contribuinte')
        fig.update_layout(autosize=False)
        st.plotly_chart( fig, use_container_width=True )                                    

#-------- Visão Tática
with tab2:
    with st.container():
        # Percentual de Fatores por Área
        st.header( 'Percentual de Fatores por Área' )   

        df_aux = seleciona_fator_area(df_fator_recomendacao)

        fig = px.pie( df_aux, values='perc_area', names='fator_area', title='Fator Área')
        fig.update_layout(autosize=False)
        st.plotly_chart( fig, use_container_width=True )          