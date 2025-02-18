FROM python:3.11

# definir o diretório de trabalho
WORKDIR /app

# copiar o conteúdo do diretório atual para o diretório de trabalho
COPY . /app

# instalar as dependências do projeto
RUN pip install pipenv && pipenv install --deploy --system

# disponibilizar a porta 80
EXPOSE 80

# rodar o servidor uvicorn na porta 80
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--app-dir", "app", "--workers", "4"]

