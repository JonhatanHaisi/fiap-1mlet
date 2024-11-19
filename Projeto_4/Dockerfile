# Usar a imagem base do Amazon Linux
FROM amazonlinux:2

# Atualizar os pacotes e instalar as dependências necessárias
RUN yum update -y && \
    yum -y groupinstall "Development Tools" && \
    yum -y install gcc devel libffi-devel openssl11-1.1.1g openssl11-libs-1.1.1g openssl11-devel-1.1.1g sqlite-devel && \
    yum -y install wget && \
    wget https://www.python.org/ftp/python/3.12.0/Python-3.12.0.tgz && \
    tar zxvf Python-3.12.0.tgz && \
    cd Python-3.12.0/ && \
    ./configure --enable-optimizations && \
    make && \
    make altinstall


# Instalar o pipenv
RUN pip3.12 install pipenv

EXPOSE 8000
WORKDIR /app
COPY . /app

# Instalar as dependências do projeto
RUN pipenv install --deploy --ignore-pipfile && \
    pipenv install torch --index pypi

CMD ["pipenv", "run", "app" ]

