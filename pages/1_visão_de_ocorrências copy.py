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

#8888888888888888888888888888888888888888888888888888888888888888888888888
df1 = pd.read_csv( 'dataset/train.csv' )

# 1. convertando a coluna Age de texto para numero
linhas_selecionadas = (df1['Delivery_person_Age'] != 'NaN ') 
df1 = df1.loc[linhas_selecionadas, :].copy()

linhas_selecionadas = (df1['Delivery_person_Ratings'] != 'NaN ') 
df1 = df1.loc[linhas_selecionadas, :].copy()

linhas_selecionadas = (df1['Road_traffic_density'] != 'NaN ') 
df1 = df1.loc[linhas_selecionadas, :].copy()

linhas_selecionadas = (df1['City'] != 'NaN ') 
df1 = df1.loc[linhas_selecionadas, :].copy()

linhas_selecionadas = (df1['Festival'] != 'NaN ') 
df1 = df1.loc[linhas_selecionadas, :].copy()

df1.loc[df1.multiple_deliveries.isnull(), 'multiple_deliveries'] = ' '
linhas_selecionadas = (df1['multiple_deliveries'] != ' ') 
df1 = df1.loc[linhas_selecionadas, :].copy()

print(df1.isnull().sum())
#exit()

df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype( int )

# 2. convertando a coluna Ratings de texto para numero decimal ( float )
df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype( float )

# 3. convertando a coluna order_date de texto para data
df1['Order_Date'] = pd.to_datetime( df1['Order_Date'], format='%d-%m-%Y' )

# 4. convertendo multiple_deliveries de texto para numero inteiro ( int )
linhas_selecionadas = (df1['multiple_deliveries'] != 'NaN ')
df1 = df1.loc[linhas_selecionadas, :].copy()
df1['multiple_deliveries'] = df1['multiple_deliveries'].astype( int )

## 5. Removendo os espacos dentro de strings/texto/object
#df1 = df1.reset_index( drop=True )
#for i in range( len( df1 ) ):
#  df1.loc[i, 'ID'] = df1.loc[i, 'ID'].strip()

# 6. Removendo os espacos dentro de strings/texto/object

df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip()
df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()
df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].str.strip()

# 7. Limpando a coluna de time taken
df1['Time_taken(min)'] = df1['Time_taken(min)'].apply( lambda x: x.split( '(min) ')[1] )
df1['Time_taken(min)']  = df1['Time_taken(min)'].astype( int )
#8888888888888888888888888888888888888888888888888888888888888888888888888




df_ocorrencias = pd.read_csv( 'dataset_analise/df_acidentes_analise_ocorr.csv' )

df_ocorrencias['ocorrencia_dia'] = pd.to_datetime(df_ocorrencias['ocorrencia_dia'])

#----------------------------------------------
# Barra lateral sidebar
#----------------------------------------------
st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color: #8390EC;
    }
</style>
""", unsafe_allow_html=True)

#-------- Dados Gerais
st.header('Visão de Ocorrências')

with st.container():
    st.title( 'Métricas Gerais' )

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

#-------- Imagem
image_path = './images/aviao2.jpg'
ix = Image.open( image_path ) 
st.sidebar.image( ix, width=240 )

#-------- Empresa
st.sidebar.markdown( '# i4x.Data' )
st.sidebar.markdown( '## Análise e Predição de Dados')
st.sidebar.markdown( """___""")

#-------- Controle de Data
st.sidebar.markdown('## Selecione uma data limite')

date_slider = st.sidebar.slider(
   'Ate qual valor?',
   value=datetime( 2022, 4, 13),
   min_value=datetime(2022, 2, 11),
   max_value=datetime(2022, 4, 6),
   format='DD-MM-YYYY')

st.sidebar.markdown("""___""")

#-------- Parâmetros de filtragem
traffic_options = st.sidebar.multiselect(
    'Quais as condições do trânsito',
    ['Low', 'Medium', 'High', 'Jam'],
    default=['Low', 'Medium', 'High', 'Jam']
    )

st.sidebar.markdown("""___""")
st.sidebar.markdown( '### Powered by i4x.Data')

#-------- filtro de data
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]
#st.dataframe( df1 )

#-------- filtro de transito
linhas_selecionadas = df1['Road_traffic_density'].isin( traffic_options)
df1 = df1.loc[linhas_selecionadas, :]
#st.dataframe( df1 )

#----------------------------------------------
# Layout no Streamlit
#----------------------------------------------
tab1, tab2, tab3 = st.tabs( ['Visão Estratégica', 'Visão Tática', 'Visão Geográfica'])

with tab1:
    with st.container():
        # Order Metric
        st.markdown( '# Orders by Day')

        # colunas
        cols = ['ID', 'Order_Date']

        # selecao de linhas
        df_aux = df1.loc[:, cols].groupby( 'Order_Date' ).count().reset_index()

        # desenhar o gráfico de linhas
        # Plotly
        fig = px.bar ( df_aux, x='Order_Date', y='ID')    
        st.plotly_chart( fig, use_container_width=True)

    with st.container():
        col1, col2 = st.columns( 2 )
        with col1:
            st.header( 'Traffic Order Share')
            df_aux = df1.loc[:, ['ID', 'Road_traffic_density']].groupby('Road_traffic_density').count().reset_index()
            df_aux = df_aux.loc[df_aux['Road_traffic_density'] != "NaN", :]
            df_aux['entregas_perc'] = df_aux['ID'] / df_aux['ID'].sum()
            fig = px.pie( df_aux, values='entregas_perc', names='Road_traffic_density')
            st.plotly_chart( fig, use_container_width=True )
        
        with col2:
            st.header( 'Traffic Order City')
            df_aux = df1.loc[:, ['ID', 'City', 'Road_traffic_density']].groupby(['City', 'Road_traffic_density']).count().reset_index()
            df_aux = df_aux.loc[df_aux['City'] != 'NaN', :]
            df_aux = df_aux.loc[df_aux['Road_traffic_density'] != 'NaN', :]
            fig = px.scatter( df_aux, x='City', y='Road_traffic_density', size = 'ID', color='City')
            st.plotly_chart( fig, use_container_width=True )

with tab2:
    with st.container():
        st.markdown( '# Order by Week')
        # criar a coluna de semana
        df1['week_of_year'] = df1['Order_Date'].dt.strftime( '%U')
        df_aux = df1.loc[:, ['ID', 'week_of_year']].groupby( 'week_of_year').count().reset_index()
        fig = px.line( df_aux, x='week_of_year', y='ID' )
        st.plotly_chart( fig, use_container_width=True )

    with st.container():
        st.markdown( '# Order Share by Week')
        df_aux01 = df1.loc[:, ['ID', 'week_of_year']].groupby('week_of_year').count().reset_index()
        df_aux02 = df1.loc[:, ['Delivery_person_ID', 'week_of_year']].groupby( 'week_of_year' ).nunique().reset_index()

        df_aux = pd.merge( df_aux01, df_aux02, how='inner', on='week_of_year' )
        df_aux['order_by_deliver'] = df_aux['ID'] / df_aux['Delivery_person_ID']

        fig=px.line( df_aux, x='week_of_year', y='order_by_deliver')
        st.plotly_chart( fig, use_container_width=True )

with tab3:
    st.markdown( '# Country Maps')
    df_aux = df1.loc[:, ['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']].\
                groupby(['City', 'Road_traffic_density']).median().reset_index()
    df_aux = df_aux.loc[df_aux['City'] != 'NaN', :]
    df_aux = df_aux.loc[df_aux['Road_traffic_density'] != 'NaN', :]   

    map = folium.Map()

    for index, location_info in df_aux.iterrows():
        folium.Marker( [location_info['Delivery_location_latitude'],
                        location_info['Delivery_location_longitude']],
                        popup=location_info[['City', 'Road_traffic_density']] ).add_to( map )
        
    folium_static( map, width=1024, height=600 )