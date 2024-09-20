from st_aggrid import AgGrid

import streamlit as st
import pandas as pd
import joblib

import utils.covid_global_utils as cgu


st.set_page_config(page_title="COVID 19 Dashboard", page_icon="🦠", layout="wide")

covid_global_tab, vacinacao_tab, previsoes = st.tabs(['Covid Global', 'Vacinação', 'Previsões'])

with covid_global_tab:
    '# COVID-19 Global'

    covid_global = cgu.carrega_e_formata_dados_covid_global()

    '## Analise acumulativa de casos de COVID 19'
    st.plotly_chart(cgu.criar_grafico_evolucao(covid_global, 'Casos Acumulados', 'Novos casos de COVID-19 no mundo'))
    st.plotly_chart(cgu.criar_grafico_geo(covid_global, 'Casos Acumulados', 'Casos de COVID-19 no mundo'))
    st.plotly_chart(cgu.criar_grafico_acumulado(covid_global, 'Evolução de casos de COVID-19 no mundo', 'Casos Acumulados', 'Novos Casos'))

    '## Analise acumulativa de mortes por COVID 19'
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
    st.plotly_chart(cgu.criar_grafico_total_vacinacao(vacinacao_global.query('`Total de Vacinações` > 10000000'), 'Total de vacinações por país (10mi ou mais)'))

    '## Comparativo de vacinação por região OMS'
    st.plotly_chart(cgu.criar_grafico_comparativo_1_dose_e_ultima_dose_e_dose_reforco(vacinacao_global, 'Comparativo de vacinação por região OMS'))
    st.plotly_chart(cgu.criar_grafico_100mil_comparativo_1_dose_e_ultima_dose_e_dose_reforco(vacinacao_global, 'Comparativo de vacinação por região OMS (por 100 mil habitantes)'))


    '## Tabela de vacinação da COVID 19 no mundo'
    AgGrid(vacinacao_global)


with previsoes:
    '# Previsões'

    # FORMULARIO DE DADOS PARA ALIMETAÇÃO DO MODELO
    '## Informe os dados para previsão'

    regiao = st.selectbox('Região OMS', covid_global['Região OMS'].unique())
    total_vacicacoes = st.number_input('Total de vacinações', min_value=0, value=0)
    total_ultima_dose = st.number_input('Total de pessoas com ultima dose', min_value=0, value=0)
    total_dose_reforco = st.number_input('Total de pessoas com dose de reforço', min_value=0, value=0)
    prever = st.button('Prever')

    if prever:
        modelo_casos = joblib.load('models/model_covid_casos.pkl')
        modelo_mortes = joblib.load('models/model_covid_mortes.pkl')

        st.divider()

        dados = [[regiao, total_vacicacoes, total_ultima_dose, total_dose_reforco]]
        dados = pd.DataFrame(dados, columns=['Região OMS', 'Total de Vacinações', 'Pessoas com Última Dose', 'Pessoas com Dose de Reforço'])
        previsao_casos = modelo_casos.predict(dados)[0]

        dados = [[regiao, total_vacicacoes, total_ultima_dose, total_dose_reforco]]
        dados = pd.DataFrame(dados, columns=['Região OMS', 'Total de Vacinações', 'Pessoas com Última Dose', 'Pessoas com Dose de Reforço'])
        previsao_mortes = modelo_mortes.predict(dados)[0]

        '## Previsão de casos de COVID 19'
        f'Previsão de casos de COVID 19: {previsao_casos} (Erro Médio Absoluto Aproximado: 174898)'

        '## Previsão de mortes por COVID 19'
        f'Previsão de mortes por COVID 19: {previsao_mortes} (Erro Médio Absoluto Aproximado: 3593)'


     