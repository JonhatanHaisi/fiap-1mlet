from st_aggrid import AgGrid

import streamlit as st

import utils.covid_global_utils as cgu


st.set_page_config(page_title="COVID 19 Dashboard", page_icon="🦠", layout="wide")

covid_global_tab, vacinacao_tab = st.tabs(['Covid Global', 'Vacinação'])

with covid_global_tab:
    '# COVID-19 Global'

    covid_global = cgu.carrega_e_formata_dados_covid_global()

    '## Analise acuulativa de casos de COVID 19'
    st.plotly_chart(cgu.criar_grafico_evolucao(covid_global, 'Casos Acumulados', 'Novos casos de COVID-19 no mundo'))
    st.plotly_chart(cgu.criar_grafico_geo(covid_global, 'Casos Acumulados', 'Casos de COVID-19 no mundo'))
    st.plotly_chart(cgu.criar_grafico_acumulado(covid_global, 'Evolução de casos de COVID-19 no mundo', 'Casos Acumulados', 'Novos Casos'))

    '## Analise acuulativa de mortes por COVID 19'
    st.plotly_chart(cgu.criar_grafico_evolucao(covid_global, 'Mortes Acumuladas', 'Novas mortes por COVID-19 no mundo'))
    st.plotly_chart(cgu.criar_grafico_geo(covid_global, 'Mortes Acumuladas', 'Mortes por COVID-19 no mundo'))
    st.plotly_chart(cgu.criar_grafico_acumulado(covid_global, 'Evolução de mortes por COVID-19 no mundo', 'Mortes Acumuladas', 'Novas Mortes'))

    '## Analise por região OMS'
    st.plotly_chart(cgu.criar_grafico_bar(covid_global, 'Casos de COVID-19 por região OMS', 'Região OMS', 'Casos Acumulados'))
    st.plotly_chart(cgu.criar_grafico_bar(covid_global, 'Mortes por COVID-19 por região OMS', 'Região OMS', 'Mortes Acumuladas'))

    '## Tabela de morte da COVID 19 no mundo'
    AgGrid(covid_global)


with vacinacao_tab:
    '# Vacinação COVID-19 Global'

    vacinacao_global = cgu.carrega_e_formata_dados_vacinacao_covid_global()

    '## Adesão à vacinação por país'
    st.plotly_chart(cgu.criar_grafico_adesao_vacina(vacinacao_global, 'Novos Paises Vacinantes Por Dia'))

    '## Total de vacinações por país'
    st.plotly_chart(cgu.criar_grafico_total_vacinacao(vacinacao_global.query('`Total de Vacinações` > 10000000'), 'Total de vacinações por país'))

    '## Tabela de vacinação da COVID 19 no mundo'
    AgGrid(vacinacao_global)


     