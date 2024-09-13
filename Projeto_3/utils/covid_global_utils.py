import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go

from plotly import subplots


@st.cache_resource
def carrega_e_formata_dados_covid_global():
    '''
    Carrega e formata os dados de COVID-19 global
    '''

    arquivo = './data/WHO-COVID-19-global-data.csv'
    covid_global = pd.read_csv(arquivo, sep=';', encoding='utf-8')
    covid_global['Date_reported'] = pd.to_datetime(covid_global['Date_reported'], dayfirst=True)
    covid_global['Country_code'] = covid_global['Country_code'].fillna('?').astype('category')
    covid_global['Country'] = covid_global.Country.astype('category')
    covid_global['WHO_region'] = covid_global['WHO_region'].fillna('?').astype('category')
    covid_global['New_cases'] = covid_global['New_cases'].fillna(0).astype(int)
    covid_global['New_deaths'] = covid_global['New_deaths'].fillna(0).astype(int)

    covid_global = covid_global.rename(columns={
        'Date_reported': 'Data Reportada',
        'Country_code': 'Código do País',
        'Country': 'País',
        'WHO_region': 'Região OMS',
        'New_cases': 'Novos Casos',
        'Cumulative_cases': 'Casos Acumulados',
        'New_deaths': 'Novas Mortes',
        'Cumulative_deaths': 'Mortes Acumuladas',
    })

    return covid_global


@st.cache_resource
def carrega_e_formata_dados_vacinacao_covid_global():
    '''
    Carrega e formata os dados de vacinação global
    '''

    arquivo = './data/vaccination-data.csv'
    vacinacao = pd.read_csv(arquivo, sep=';', encoding='utf-8')
    vacinacao['WHO_REGION'] = vacinacao['WHO_REGION'].fillna('?').astype('category')
    vacinacao['FIRST_VACCINE_DATE'] = pd.to_datetime(vacinacao['FIRST_VACCINE_DATE'], dayfirst=True)
    
    vacinacao = vacinacao.drop(['ISO3', 'DATA_SOURCE', 'VACCINES_USED', 'DATE_UPDATED', 'NUMBER_VACCINES_TYPES_USED', vacinacao.columns[-1]], axis=1)

    vacinacao = vacinacao.rename(columns={
        'COUNTRY': 'País',
        'WHO_REGION': 'Região OMS',
        'FIRST_VACCINE_DATE': 'Data da Primeira Vacina',
        'TOTAL_VACCINATIONS': 'Total de Vacinações',
        'PERSONS_VACCINATED_1PLUS_DOSE': 'Pessoas Vacinadas 1+ Doses',
        'TOTAL_VACCINATIONS_PER100': 'Total de Vacinações por 100 Mil',
        'PERSONS_VACCINATED_1PLUS_DOSE_PER100': 'Pessoas Vacinadas 1+ Doses por 100 Mil',
        'PERSONS_LAST_DOSE': 'Pessoas com Última Dose',
        'PERSONS_LAST_DOSE_PER100': 'Pessoas com Última Dose por 100 Mil',
        'PERSONS_BOOSTER_ADD_DOSE': 'Pessoas com Dose de Reforço',
        'PERSONS_BOOSTER_ADD_DOSE_PER100': 'Pessoas com Dose de Reforço por 100 Mil',
    })

    vacinacao['Total de Vacinações por 100 Mil'] = vacinacao['Total de Vacinações por 100 Mil'] * 1000
    vacinacao['Pessoas Vacinadas 1+ Doses por 100 Mil'] = vacinacao['Pessoas Vacinadas 1+ Doses por 100 Mil'] * 1000
    vacinacao['Pessoas com Última Dose por 100 Mil'] = vacinacao['Pessoas com Última Dose por 100 Mil'] * 1000
    vacinacao['Pessoas com Dose de Reforço por 100 Mil'] = vacinacao['Pessoas com Dose de Reforço por 100 Mil'] * 1000

    vacinacao = vacinacao.dropna()

    return vacinacao


def criar_grafico_evolucao(df:pd.DataFrame, coluna:str, titulo:str, cor:str='País'):
    '''
    Cria um gráfico de linha com a evolução de uma coluna
    '''

    return px.line(
        df, 
        x='Data Reportada', 
        y=coluna, 
        color=cor, 
        title=titulo,
    )


def criar_grafico_geo(df:pd.DataFrame, coluna:str, titulo:str, width=1500, height=800):
    '''
    Cria um gráfico de mapa com a evolução de uma coluna
    '''

    covid_global_grouped = df.groupby('País')[coluna].max().sort_values(ascending=False)
    return px.scatter_geo(
        covid_global_grouped, 
        locations=covid_global_grouped.index, 
        size=coluna, 
        locationmode='country names', 
        title=titulo,
        width=width, 
        height=height,
    )


def criar_grafico_acumulado(df:pd.DataFrame, titulo:str, col_acumulada:str, col_novos:str):
    '''
    Cria um gráfico de barras com a evolução de uma coluna acumulada e uma coluna de novos casos
    '''

    covid_death_cumulative = df.groupby('Data Reportada')[col_acumulada].sum().sort_values(ascending=False)
    covid_new_death_cumulative = df.groupby('Data Reportada')[col_novos].sum().sort_values(ascending=False)

    fig = subplots.make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Bar(x=covid_new_death_cumulative.index, y=covid_new_death_cumulative.values, name=col_novos), secondary_y=False)
    fig.add_trace(go.Scatter(x=covid_death_cumulative.index, y=covid_death_cumulative.values, name=col_acumulada,  mode='markers', marker=dict(color='#c83f22', size=3)), secondary_y=True)

    fig.update_layout(
        title=titulo,
        xaxis_title="Data Reportada",
        yaxis_title=col_novos,
        yaxis2_title=col_acumulada,
    )

    return fig


def criar_grafico_bar(df:pd.DataFrame, titulo:str, group_by:str, coluna:str):
    '''
    Cria um gráfico de barras com a evolução de uma coluna agrupada
    '''
    covid_global_grouped = df.groupby(group_by)[coluna].max().sort_values(ascending=False)    
    return px.bar(covid_global_grouped, y=coluna, title=titulo)


def criar_grafico_adesao_vacina(df: pd.DataFrame, titulo: str):
    '''
    Cria uma figura com dois gráficos: um gráfico de barras com a adesão à vacinação
    e um gráfico de linha com os valores acumulados.
    '''

    fig = subplots.make_subplots(specs=[[{"secondary_y": True}]])

    adesao_vacina = df.groupby('Data da Primeira Vacina')['País'].count().sort_values(ascending=False)
    fig.add_trace(
        go.Bar(x=adesao_vacina.index, y=adesao_vacina.values, name='Adesão à Vacinação'),
        secondary_y=False
    )

    adesao_acumulada = df.sort_values('Data da Primeira Vacina') \
        .set_index('Data da Primeira Vacina') \
        .groupby('Data da Primeira Vacina')['País'].count()+1
    adesao_acumulada = adesao_acumulada.groupby('Data da Primeira Vacina') .count().cumsum()

    fig.add_trace(
        go.Scatter(x=adesao_acumulada.index, y=adesao_acumulada.values, mode='lines', name='Valores Acumulados'),
        secondary_y=True
    )

    fig.update_layout(title_text=titulo, showlegend=False)
    
    return fig

def criar_grafico_total_vacinacao(df:pd.DataFrame, titulo:str):
    '''
    Cria um gráfico de barras com o total de vacinações por país
    '''

    return px.bar(
        df.sort_values('País'), 
        x='País', 
        y='Total de Vacinações', 
        title=titulo,
        height=800,
    )



def criar_grafico_comparativo_1_dose_e_ultima_dose_e_dose_reforco(df:pd.DataFrame, titulo:str):
    fig = go.Figure()

    vacinas_por_regiao = df.groupby('Região OMS')[['Pessoas Vacinadas 1+ Doses', 'Pessoas com Última Dose', 'Pessoas com Dose de Reforço']].sum()
    vacinas_por_regiao = vacinas_por_regiao.query('`Pessoas Vacinadas 1+ Doses` > 0')

    fig.add_trace(go.Bar(
        x=vacinas_por_regiao.index,
        y=vacinas_por_regiao['Pessoas Vacinadas 1+ Doses'],
        name='Pessoas Vacinadas 1+ Doses',
        marker_color='blue'
    ))

    fig.add_trace(go.Bar(
        x=vacinas_por_regiao.index,
        y=vacinas_por_regiao['Pessoas com Última Dose'],
        name='Pessoas com Última Dose',
        marker_color='green'
    ))

    fig.add_trace(go.Bar(
        x=vacinas_por_regiao.index,
        y=vacinas_por_regiao['Pessoas com Dose de Reforço'],
        name='Pessoas com Dose de Reforço',
        marker_color='purple'
    ))

    fig.update_layout(
        title=titulo,
        barmode='group'
    )

    return fig


def criar_grafico_100mil_comparativo_1_dose_e_ultima_dose_e_dose_reforco(df:pd.DataFrame, titulo:str):
    fig = go.Figure()

    vacinas_por_regiao = df.groupby('Região OMS')[['Pessoas Vacinadas 1+ Doses por 100 Mil', 'Pessoas com Última Dose por 100 Mil', 'Pessoas com Dose de Reforço por 100 Mil']].sum()
    vacinas_por_regiao = vacinas_por_regiao.query('`Pessoas Vacinadas 1+ Doses por 100 Mil` > 0')

    fig.add_trace(go.Bar(
        x=vacinas_por_regiao.index,
        y=vacinas_por_regiao['Pessoas Vacinadas 1+ Doses por 100 Mil'],
        name='Pessoas Vacinadas 1+ Doses por 100 Mil',
        marker_color='blue'
    ))

    fig.add_trace(go.Bar(
        x=vacinas_por_regiao.index,
        y=vacinas_por_regiao['Pessoas com Última Dose por 100 Mil'],
        name='Pessoas com Última Dose por 100 Mil',
        marker_color='green'
    ))

    fig.add_trace(go.Bar(
        x=vacinas_por_regiao.index,
        y=vacinas_por_regiao['Pessoas com Dose de Reforço por 100 Mil'],
        name='Pessoas com Dose de Reforço por 100 Mil',
        marker_color='purple'
    ))

    fig.update_layout(
        title=titulo,
        barmode='group'
    )

    return fig
