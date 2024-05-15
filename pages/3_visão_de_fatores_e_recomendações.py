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
    df_ocorrencias = pd.read_csv( 'dataset_analise/df_acidentes_analise_ocorr.csv' )
    df_ocorrencias['ocorrencia_dia'] = pd.to_datetime(df_ocorrencias['ocorrencia_dia'])
    return df_ocorrencias

@st.cache_data
def seleciona_tipo_ocorrencia(dfx):
    return dfx[['ocorrencia_tipo', 'qtde_tipo_ocorr', 'perc_tipo_ocorr']].\
        drop_duplicates().sort_values('perc_tipo_ocorr', ascending=False)

@st.cache_data
def agrupa_uf_classificacao(dfx):
    # colunas
    cols = ['ocorrencia_uf', 'ocorrencia_classificacao', 'qtde_classif']

    # selecao de linhas
    dfx = df_ocorrencias[['ocorrencia_uf', 'ocorrencia_classificacao']]
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
df_ocorrencias = le_arquivo_analise()

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
image_path = './images/aviao2.jpg'
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
        col1.metric( 'Data Inicial', df_ocorrencias.loc[:, 'ocorrencia_dia'].min().strftime("%d/%m/%Y") )            

    with col2:
        # data final
        col2.metric( 'Data Final', df_ocorrencias.loc[:, 'ocorrencia_dia'].max().strftime("%d/%m/%Y") ) 

with st.container():

    col1, col2, col3 = st.columns( 3, gap='Large')
    with col1:
        # total de ocorrências
        col1.metric( 'Total de Ocorrências', df_ocorrencias.loc[:, 'ocorrencia_classificacao'].count() )            

    with col2:
        # total de aeródromos envolvidos
        col2.metric( 'Qtde Aeródromos', len(pd.unique(df_ocorrencias['ocorrencia_aerodromo'])) )   

    with col3:
        # total de saída de pista
        col3.metric( 'Qtde Saídas da Pista', df_ocorrencias.loc[:, 'qtde_saip_total'].max() ) 

#----------------------------------------------
# gráficos
#----------------------------------------------
#-------- Abas de finalidade dos dados
tab1, tab2, tab3 = st.tabs( ['Visão Estratégica', 'Visão Tática', '-'])

#-------- Visão Estratégica
with tab1:
    with st.container():
        # Classificação de ocorrências por UF
        st.header( 'Classificação de Ocorrências por UF' )

        dfx = agrupa_uf_classificacao(df_ocorrencias)

        # desenhar o gráfico de colunas
        # Plotly  
        fig = px.bar(dfx, x="qtde_classif", y="ocorrencia_uf", color="ocorrencia_classificacao",
                     orientation='h',
                     labels={
                            "qtde_classif": "Ocorrências",
                            "ocorrencia_uf": "UF",
                            "ocorrencia_classificacao": "Classificação"
                            },                     
                     )
        fig.update_traces(width=0.8)
        fig.update_yaxes(tickfont=dict(size=8))
        fig.update_xaxes(tickfont=dict(size=8))
        st.plotly_chart( fig, use_container_width=True)

    with st.container():
        # Percentual de Tipos de ocorrência
        st.header( 'Percentual de Tipos de Ocorrência' )   

        #-------- Controle de dados dupla face
        intervalo = st.slider('Selecione o intervalo de percentual',
                            0.0, 100.0, (1.75, 100.0))
        st.write('Intervalo Selecionado:',intervalo) 

        dfx = seleciona_tipo_ocorrencia(df_ocorrencias)
        df_aux = dfx[(dfx['perc_tipo_ocorr'] >= intervalo[0]) & (dfx['perc_tipo_ocorr'] < intervalo[1])]
        perc_eliminados = \
            dfx[(dfx['perc_tipo_ocorr'] < intervalo[0]) | (dfx['perc_tipo_ocorr'] > intervalo[1])]['perc_tipo_ocorr'].sum()

        df_inclui = {'ocorrencia_tipo':'***** fora do intervalo', 'qtde_tipo_ocorr': 0, 'perc_tipo_ocorr': perc_eliminados}
        df_inclui = pd.DataFrame(df_inclui, index=([1]))
        df_aux = pd.concat([df_aux, df_inclui])

        fig = px.pie( df_aux, values='perc_tipo_ocorr', names='ocorrencia_tipo')
        fig.update_layout(autosize=False)
        st.plotly_chart( fig, use_container_width=True )                                    

#-------- Visão Tática
with tab2:
    with st.container():
        # Quantidade de Saidas da Pista por Aeródromo
        st.header( 'Quantidade de Saidas da Pista por Aeródromo' )   

        dfx = seleciona_saida_pista_aerodromo(df_ocorrencias)

        #-------- Controle de dados dupla face
        intervalo = st.slider('Selecione o intervalo de quantidade',
                            0.0, 100.0, (6.0, 100.0))
        st.write('Intervalo Selecionado:',intervalo)    

        df_aux = dfx[(dfx['qtde_saip_aerod'] >= intervalo[0]) & (dfx['qtde_saip_aerod'] < intervalo[1])]

        fig = px.bar ( df_aux, x='qtde_saip_aerod', y='cidade_aerodromo',                      
                       labels={
                            "qtde_saip_aerod": "Quantidade",
                            "cidade_aerodromo": "Aeródromo",
                              },                     
                     )
        fig.update_traces(width=0.8)
        fig.update_yaxes(tickfont=dict(size=8))
        fig.update_xaxes(tickfont=dict(size=8))

        st.plotly_chart( fig, use_container_width=True)          