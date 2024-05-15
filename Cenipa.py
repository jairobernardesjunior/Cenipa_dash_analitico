import streamlit as st
from PIL import Image
st.set_page_config( page_title='Home', page_icon='')

image_path = 'images/aviao.jpg'
image = Image.open( image_path )
st.sidebar.image( image, width=240 )

st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color: #CFD0DC;
    }
</style>
""", unsafe_allow_html=True)

st.sidebar.markdown( '# Análise e Predição')
st.sidebar.markdown( '### Powered by i4x.Data')

st.markdown(
    """
    Cenipa Dashboard foi construído para acompanhar as ocorrências de acidentes aeronáuticos no Brasil com
    dados públicos do Cenipa da Força Aérea Brasileira.
    ### Como utilizar o Cenipa Dashboard?
    - Visão de ocorrências:
        - Visão Gerencial: Métricas gerais de comportamento.
        - Visão Tática: Indicadores semanais de crescimento.
        - Visão Geográfica: Insights de geolocalização.
    - Visão de aeronaves:
        - Acompanhamento dos indicadores semanis de crescimento
    - Visão de fatores contribuintes e recomendações de segurança:
        - Indicadores semanis de crescimento dos restaurantes
    ### Contato
    - https://www.linkedin.com/in/jairobernardesjunior
    """)