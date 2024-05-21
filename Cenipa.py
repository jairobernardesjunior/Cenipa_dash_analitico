# Cenipa.py é o módulo principal do site desenvolvido com python-streamlit que apresenta os insights dos
# dados de acidentes aeronáuticos fornecidos publicamente pelo Cenipa da Força Aérea Brasileira.
# O tratamento de dados tem início no projeto Cenipa_limpa_trata gerando um arquivo tratado único, chamado
# df_acidentes_aeronauticos.csv, disponibilizado para os próximos 3 processos: Cenipa_analise_ocorrencias,
# Cenipa_analise_aeronaves e Cenipa_analise_fatores_recomendacoes. Esses 3 projetos faz análise dos dados e
# agrega mais colunas de valores dentro de cada assunto que lhe é pertinente, ocorrências, aeronaves e fatores
# contribuintes e recomendações de segurança, gerando, cada projeto, um arquivo com dados agregados novos que
# é recebido nesse projeto sendo o insumo de dados para a geração dos insights sobre acidentes aeronáuticos.

# importa as bibliotecas
import streamlit as st
from PIL import Image
st.set_page_config( page_title='Cenipa_i4x.Data', page_icon='')

# carrega imagem para o sidebar (barra lateral)
image_path = 'images/aviao5.jpg'
image = Image.open( image_path )
st.sidebar.image( image, width=240 )

# define a cor de fundo do sidebar e exibe frase de finalidade e empresa
st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color: #EAEAE8;
    }           
</style>
""", unsafe_allow_html=True)

st.sidebar.markdown( '# Análise e Predição')
st.sidebar.markdown( '### Powered by i4x.Data')
st.sidebar.markdown( '##### **Site em constante evolução')

# exibe explicação sobre o site Cenipa Dashboard e explica o seu conteúdo
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