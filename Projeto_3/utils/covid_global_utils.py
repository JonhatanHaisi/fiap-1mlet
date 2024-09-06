import pandas as pd
import plotly.express as px
import streamlit as st

@st.cache_resource
def carrega_e_formata_dados_covid_global():
    arquivo = './data/WHO-COVID-19-global-data.csv'
    covid_global = pd.read_csv(arquivo, sep=';', encoding='utf-8')
    covid_global['Date_reported'] = pd.to_datetime(covid_global['Date_reported'], dayfirst=True)
    covid_global['Country_code'] = covid_global['Country_code'].fillna('?').astype('category')
    covid_global['Country'] = covid_global.Country.astype('category')
    covid_global['WHO_region'] = covid_global['WHO_region'].fillna('?').astype('category')
    covid_global['New_cases'] = covid_global['New_cases'].fillna(0).astype(int)
    covid_global['New_deaths'] = covid_global['New_deaths'].fillna(0).astype(int)

    return covid_global

def criar_grafico_evolucao(df:pd.DataFrame, coluna:str, titulo:str, cor:str='Country', width=10000, height=450):
    return px.line(
        df, 
        x='Date_reported', 
        y=coluna, 
        color=cor, 
        title=titulo,
        width=width,
        height=height,
    )


def criar_grafico_geo(df:pd.DataFrame, coluna:str, titulo:str, width=1500, height=600):
    covid_global_grouped = df.groupby('Country')[coluna].max().sort_values(ascending=False)
    return px.scatter_geo(
        covid_global_grouped, 
        locations=covid_global_grouped.index, 
        size=covid_global_grouped.values, 
        locationmode='country names', 
        title=titulo,
        width=width, 
        height=height,
    )

