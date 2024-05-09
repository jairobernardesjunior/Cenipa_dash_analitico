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
import numpy as np

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

#--------
st.header('Visão de Fatores Contribuintes e Recomendações de Segurança')

#--------
image_path = './images/aviao4.jpg'
ix = Image.open( image_path ) 
st.sidebar.image( ix, width=240 )

#--------
st.sidebar.markdown( '# i4x.Data' )
st.sidebar.markdown( '## Análise e Predição de Dados')
st.sidebar.markdown( """___""")

#--------
st.sidebar.markdown('## Selecione uma data limite')

date_slider = st.sidebar.slider(
   'Ate qual valor?',
   value=datetime( 2022, 4, 13),
   min_value=datetime(2022, 2, 11),
   max_value=datetime(2022, 4, 6),
   format='DD-MM-YYYY')

#st.dataframe( df1 )

st.header( date_slider )
st.sidebar.markdown("""___""")

#--------
traffic_options = st.sidebar.multiselect(
    'Quais as condições do trânsito',
    ['Low', 'Medium', 'High', 'Jam'],
    default=['Low', 'Medium', 'High', 'Jam']
    )

st.sidebar.markdown("""___""")
st.sidebar.markdown( '### Powered by i4x.Data')

# filtro de data
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]
#st.dataframe( df1 )

# filtro de transito
linhas_selecionadas = df1['Road_traffic_density'].isin( traffic_options)
df1 = df1.loc[linhas_selecionadas, :]
#st.dataframe( df1 )

#----------------------------------------------
# Layout no Streamlit
#----------------------------------------------
tab1, tab2, tab3 = st.tabs( ['Visão Gerencial', '_', '_'])

with tab1:
    with st.container():
        st.title( 'Overall Metrics' )

        col1, col2, col3, col4, col5, col6 = st.columns( 6 )
        with col1:
            delivery_unique = len( df1.loc[:, 'Delivery_person_ID'].unique())
            col1.metric( 'Entregadores únicos', delivery_unique)

        with col2:
            cols = ['Delivery_location_latitude', 'Delivery_location_longitude', 'Restaurant_latitude', 'Restaurant_longitude']
            df1['distance'] = ( df1.loc[:, cols].apply( lambda x:
                                                       haversine ((x['Restaurant_latitude'],
                                                                   x['Restaurant_longitude']),
                                                                  (x['Delivery_location_latitude'],
                                                                   x['Delivery_location_longitude']) ), axis=1))
            avg_distance = np.round( df1['distance'].mean(), 2 )
            col2.metric( 'A distancia media', avg_distance )

        with col3:
            df_aux = ( df1.loc[:, [ 'Time_taken(min)', 'Festival']]
                          .groupby( 'Festival' )
                          .agg( { 'Time_taken(min)': ['mean', 'std']}) )

            df_aux.columns = ['avg_time', 'std_time']
            df_aux = df_aux.reset_index()
            df_aux = df_aux.loc[df_aux['Festival'] == 'Yes', 'avg_time']
            col3.metric( 'Tempo Médio', round(df_aux, 2 ) )

        with col4:
            df_aux = ( df1.loc[:, [ 'Time_taken(min)', 'Festival']]
                          .groupby( 'Festival' )
                          .agg( { 'Time_taken(min)': ['mean', 'std']}) )

            df_aux.columns = ['avg_time', 'std_time']
            df_aux = df_aux.reset_index()
            df_aux = df_aux.loc[df_aux['Festival'] == 'Yes', 'std_time']
            col4.metric( 'STD Médio de Entrega', round(df_aux, 2 ) )

        with col5:
            df_aux = ( df1.loc[:, [ 'Time_taken(min)', 'Festival']]
                          .groupby( 'Festival' )
                          .agg( { 'Time_taken(min)': ['mean', 'std']}) )

            df_aux.columns = ['avg_time', 'std_time']
            df_aux = df_aux.reset_index()
            df_aux = df_aux.loc[df_aux['Festival'] == 'No', 'avg_time']
            col5.metric( 'Tempo Médio de Entrega', round(df_aux, 2 ) )

        with col6:
            df_aux = ( df1.loc[:, [ 'Time_taken(min)', 'Festival']]
                          .groupby( 'Festival' )
                          .agg( { 'Time_taken(min)': ['mean', 'std']}) )

            df_aux.columns = ['avg_time', 'std_time']
            df_aux = df_aux.reset_index()
            df_aux = df_aux.loc[df_aux['Festival'] == 'No', 'std_time']
            col6.metric( 'STD Médio de Entrega', round(df_aux, 2 ) )                                                           

    with st.container():
        st.markdown("""____""")

        col1, col2 = st.columns( 2 )
        with col1:    
            st.title( 'Tempo Médio de Entrega por Cidade' )
            df_aux = df1.loc[:, ['City', 'Time_taken(min)']].groupby( 'City' ).agg( {'Time_taken(min)': ['mean', 'std']})
            df_aux.columns = ['avg_time', 'std_time']
            df_aux = df_aux.reset_index()

            fig=go.Figure()
            fig.add_trace( go.Bar( name='Control', x=df_aux['City'], y=df_aux['avg_time'],
                                    error_y=dict(type='data', array=df_aux['std_time'])))
            fig.update_layout(barmode='group')

            st.plotly_chart( fig )     

        with col2:
            st.title( 'Distribuição da Distância' )
            df_aux = (df1.loc[:, ['City', 'Time_taken(min)', 'Type_of_order']] \
                        .groupby( ['City', 'Type_of_order'] ) \
                        .agg( {'Time_taken(min)': ['mean', 'std']} ) )
            
            df_aux.columns = ['avg_time', 'std_time']
            df_aux = df_aux.reset_index()  
            st.dataframe( df_aux )              

    with st.container():
        st.markdown("""____""")        
        st.title( 'Distribuição do Tempo' )

        col1, col2 = st.columns( 2 )
        with col1:
            cols = ['Delivery_location_latitude', 'Delivery_location_longitude', 'Restaurant_latitude', 'Restaurant_longitude']
            df1['distance'] = ( df1.loc[:, cols].apply( lambda x:
                                                        haversine ((x['Restaurant_latitude'],
                                                                    x['Restaurant_longitude']),
                                                                    (x['Delivery_location_latitude'],
                                                                    x['Delivery_location_longitude']) ), axis=1))
            
            avg_distance = df1.loc[:, ['City', 'distance']].groupby( 'City' ).mean().reset_index()
            fig = go.Figure( data=[ go.Pie( labels=avg_distance['City'], values=avg_distance['distance'], pull=[0.1,0,0])])        
            st.plotly_chart( fig )

        with col2:
            df_aux = (df1.loc[:, ['City', 'Time_taken(min)', 'Road_traffic_density']] \
                        .groupby( ['City', 'Road_traffic_density'] ) \
                        .agg( {'Time_taken(min)': ['mean', 'std']} ) )
            
            df_aux.columns = ['avg_time', 'std_time']
            df_aux = df_aux.reset_index()

            fig= px.sunburst(df_aux, path=['City', 'Road_traffic_density'], values='avg_time',
                             color='std_time', color_continuous_scale='Rdbu',
                             color_continuous_midpoint=np.average(df_aux['std_time']))

            st.plotly_chart( fig )       

    with st.container():
        st.markdown("""____""")        
        st.title( 'Distribuição da Distância' )
        df_aux = (df1.loc[:, ['City', 'Time_taken(min)', 'Type_of_order']] \
                    .groupby( ['City', 'Type_of_order'] ) \
                    .agg( {'Time_taken(min)': ['mean', 'std']} ) )
        
        df_aux.columns = ['avg_time', 'std_time']
        df_aux = df_aux.reset_index()  
        st.dataframe( df_aux )








