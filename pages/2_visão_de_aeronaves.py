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




df_ocorrencia = pd.read_csv( 'dataset_analise/df_acidentes_analise_ocorr.csv' )

df_ocorrencia['ocorrencia_dia'] = pd.to_datetime(df_ocorrencia['ocorrencia_dia'])

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
st.header('Visão de Aeronaves')

#--------
image_path = './images/aviao3.jpg'
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

        col1, col2, col3, col4 = st.columns( 4, gap='large')
        with col1:
            # A maior idade dos entregadores
            maior_idade = df1.loc[:, 'Delivery_person_Age'].max()
            col1.metric( 'Maior de idade', maior_idade )            

        with col2:
            # A menor idade dos entregadores
            menor_idade = df1.loc[:, 'Delivery_person_Age'].min()
            col2.metric( 'Menor idade', menor_idade )            

        with col3:
            # Melhor condicao de veiculos
            melhor_condicao = df1.loc[:, 'Vehicle_condition'].max()
            col3.metric( 'Melhor condicao', melhor_condicao )            

        with col4:
            # Pior condicao de veiculos
            pior_condicao = df1.loc[:, 'Vehicle_condition'].min()
            col4.metric( 'Pior condicao', pior_condicao )            

    with st.container():
        st.markdown( """___""")
        st.title('Avaliacoes')

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('##### Avaliacao media por Entregador')
            df_avg_ratings_per_deliver = ( df1.loc[:, ['Delivery_person_Ratings', 'Delivery_person_ID']]
                                              .groupby( 'Delivery_person_ID' )
                                              .mean()
                                              .reset_index() )
            st.dataframe( df_avg_ratings_per_deliver )            

        with col2:
            st.markdown('##### Avaliacao media por transito')
            df_avg_std_rating_by_traffic = ( df1.loc[:, ['Delivery_person_Ratings', 'Road_traffic_density']]
                                                .groupby( 'Road_traffic_density')
                                                .agg( {'Delivery_person_Ratings': ['mean', 'std' ]} ) )

            # mudanca de nome das colunas
            df_avg_std_rating_by_traffic.columns = ['delivery_mean', 'delivery_std']

            # reset do index
            df_avg_std_rating_by_traffic = df_avg_std_rating_by_traffic.reset_index()
            st.dataframe( df_avg_std_rating_by_traffic )

            st.markdown('##### Avaliacao media por clima')
            df_avg_std_rating_by_weather = ( df1.loc[:, ['Delivery_person_Ratings', 'Weatherconditions']]
                                                .groupby( 'Weatherconditions')
                                                .agg( {'Delivery_person_Ratings': ['mean', 'std']} ) )

            # mudanca de nome das colunas
            df_avg_std_rating_by_weather.columns = ['delivery_mean', 'delivery_std']

            # reset do index
            df_avg_std_rating_by_weather = df_avg_std_rating_by_weather.reset_index()
            st.dataframe( df_avg_std_rating_by_weather )            

    with st.container():
        st.markdown( """___""")
        st.title('Velocidade de Entrega')

        col1, col2 = st.columns(2)

        with col1:
            st.markdown('##### Top Entregadores mais rapidos')
            df2 = ( df1.loc[:, ['Delivery_person_ID', 'City', 'Time_taken(min)']]
                       .groupby( ['City', 'Delivery_person_ID'] )
                       .mean()
                       .sort_values( ['City', 'Time_taken(min)'], ascending=True ).reset_index() )

            df_aux01 = df2.loc[df2['City'] == 'Metropolitian', :].head(10)
            df_aux02 = df2.loc[df2['City'] == 'Urban', :].head(10)
            df_aux03 = df2.loc[df2['City'] == 'Semi-Urban', :].head(10)

            df3 = pd.concat( [df_aux01, df_aux02, df_aux03] ).reset_index( drop=True )
            st.dataframe( df3 )            

        with col2:
            st.markdown('##### Top Entregadores mais lentos')
            df2 = ( df1.loc[:, ['Delivery_person_ID', 'City', 'Time_taken(min)']]
                       .groupby( ['City', 'Delivery_person_ID'] )
                       .mean()
                       .sort_values( ['City', 'Time_taken(min)'], ascending=False ).reset_index() )

            df_aux01 = df2.loc[df2['City'] == 'Metropolitian', :].head(10)
            df_aux02 = df2.loc[df2['City'] == 'Urban', :].head(10)
            df_aux03 = df2.loc[df2['City'] == 'Semi-Urban', :].head(10)

            df3 = pd.concat( [df_aux01, df_aux02, df_aux03] ).reset_index( drop=True )
            st.dataframe( df3 )            





