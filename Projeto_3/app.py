import streamlit as st

import utils.covid_global_utils as cgu

st.set_page_config(page_title="COVID 19 Dashboard", page_icon="🦠", layout="wide")

covid_global_tab, vacinacao_tab = st.tabs(['Covid Global', 'Vacinação'])

with covid_global_tab:
    st.title('Global COVID-19 Dashboard')

    covid_global = cgu.carrega_e_formata_dados_covid_global()

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(cgu.criar_grafico_evolucao(covid_global, 'Cumulative_cases', 'Novos casos de COVID-19 no mundo'))
    with col2:
        st.plotly_chart(cgu.criar_grafico_evolucao(covid_global, 'Cumulative_deaths', 'Novas mortes por COVID-19 no mundo'))

    st.plotly_chart(cgu.criar_grafico_geo(covid_global, 'Cumulative_cases', 'Casos de COVID-19 no mundo'))
    st.plotly_chart(cgu.criar_grafico_geo(covid_global, 'Cumulative_deaths', 'Mortes por COVID-19 no mundo'))