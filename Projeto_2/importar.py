# quero criar uma aws lambda para importar dados da b3 e salvar em um bucker

import requests
import pandas as pd
from datetime import datetime, timedelta

def importar():
    url = "https://sistemaswebb3-listados.b3.com.br/indexProxy/indexCall/GetPortfolioDay/eyJsYW5ndWFnZSI6InB0LWJyIiwicGFnZU51bWJlciI6MSwicGFnZVNpemUiOjEyMCwiaW5kZXgiOiJJQk9WIiwic2VnbWVudCI6IjEifQ=="
    response = requests.get(url, verify=False)
    data = response.json()
    data = pd.DataFrame(data['results'])

    hoje = datetime.now() + timedelta(days=1)

    data.drop(columns=['segment', 'partAcum'], inplace=True)
    data = data.assign(
        part=lambda x: x['part'].str.replace('.', '').str.replace(',', '.').astype(float),
        theoricalQty=lambda x: x['theoricalQty'].str.replace('.', '').replace(',', '.').astype(float),
        date=pd.to_datetime(hoje.strftime('%Y-%m-%d')).date(),
    )

    bucket = '1mlet-gp28'
    folder = 'raw'
    key = f'carteira-do-dia-b3.parquet'
    data.to_parquet(f's3://{bucket}/{folder}/{key}', index=False)
    


if __name__ == "__main__":
    importar()
