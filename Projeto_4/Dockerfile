# Usar a imagem base do Amazon Linux
FROM amazonlinux:2

# Atualizar os pacotes e instalar as dependências necessárias
RUN yum update -y && \
    yum install -y gcc openssl bzip2 libffi make wget tar gzip

# Baixar o Python 3.12
RUN cd /usr/src && \
    wget https://www.python.org/ftp/python/3.12.0/Python-3.12.0.tgz && \
    tar xzf Python-3.12.0.tgz && \
    cd /usr/src/Python-3.12.0 && \
    ./configure --enable-optimizations && \
    make altinstall && \
    ln -s /usr/local/bin/python3.12 /usr/bin/python3 && \
    ln -s /usr/local/bin/pip3.12 /usr/bin/pip3

# Instalar o pipenv
RUN pip3 install pipenv

EXPOSE 8000
WORKDIR /app
COPY . /app

# Instalar as dependências do projeto
RUN pipenv install --deploy --ignore-pipfile

