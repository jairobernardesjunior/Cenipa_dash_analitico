import streamlit as st
from PIL import Image
st.set_page_config( page_title='Home', page_icon='')

image_path = 'images/aviao.jpg'
image = Image.open( image_path )
st.sidebar.image( image, width=240 )

st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color: #F2F1EB;
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
        - Visão Estratégica: Indicadores de Médio e Longo Prazo.
        - Visão Tática: Indicadores de Curto Prazo.
        - Visão Geográfica: Geolocalização.
    - Visão de aeronaves:
        - Visão Estratégica: Indicadores de Médio e Longo Prazo.
        - Visão Tática: Indicadores de Curto Prazo.
    - Visão de fatores contribuintes e recomendações de segurança:
        - Visão Estratégica: Indicadores de Médio e Longo Prazo.
        - Visão Tática: Indicadores de Curto Prazo.
    ### Contato
    - https://www.linkedin.com/in/jairobernardesjunior
    """)