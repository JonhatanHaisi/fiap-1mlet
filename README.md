# fiap-1mlet

## Preparando o ambiente

1. **Instalar o PIPENV**

Pipenv é o novo gerenciador de pacotes e ambientes virtuais do python, fortemente inspirado no npm. Ele é responsavel por criar o ambiente virtual, instalar os pacotes, gerenciar as verções e é capaz de executar scripts.
[Para saber mais clique aqui!](https://blog.rocketseat.com.br/domine-o-pipenv-otimizando-a-criacao-de-ambientes-virtuais-em-python/)

O pipenv deve ser instalado em contexto global usando o pip conforme o comando a seguir:

`pip install pipenv`

2. **Definindo a pasta em que o ambiente virtual será criada**

Por padrão a pasta com os arquivos do ambiente virtual é criada em *~/.virtualenvs/nome-gerado-pelo-pipenv* (por exemplo: `C:/Users/NomeDoUsuario/.virtualenvs/fiap-1mlet-p9qmZ9_x`).

Para manter os arquivos do ambiente virtual no mesmo diretório do projeto, basta criar uma pasta chamada *.venv* na raiz do projeto (na mesma pasta do arquivo Pipfile).

`mkdir .venv`

3. **Iniciando o ambiente virtual**

Para inicializar o ambiente virtual, basta utilizar o comando `pipenv shell` na mesma pasta do arquivo Pipfile (caso o arquivo pipfile não exista, um nov arquivo será criado).

Após a inicialização do ambiente, o terminal passará a indicar que possui um ambiente virtual ativo (a linha do cursor iniciará com o nome do ambiente virtual: `(.venv) $`).

4. **Instalando as bibliotecas**

Em um ambiente virtual utilizando o pipenv, toda instalação/desinstalação de bibliotecas deve ser feito utilizando o pipenv.

Os comando do pipenv são compativeis com pip, portanto:

`pipenv install -d`: Instala todas as bibliotecas listadas no Pipfile.<br>
`pipenv install [biblioteca]`: Instala uma nova biblioteca e à adiciona ao arquivo Pipfile.<br>
`pipenv uninstall [biblioteca]`: Desinstala uma biblioteca do ambiente e remove do Pipfile.<br>

> Voce deve notar a existencia de um arquivo chamado *Pipfile.lock*, esse é um arquivo usado pelo pipenv na gestão das versões das bibliotecas instaladas e não deve ser alterado manualmente.

# Criando o banco de dados:

Esse projeto utiliza um bando de dados SQLite, com dados de vinicultura importados da Embrapa: http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_01

Para iniciar o script responsável por importar os dados e criar o banco de dados, basta utilizar o comando a seguir:

`pipenv run criar-db`

> O arquivo sqlite do banco de dados é criado na pasta raíz do projeto. Caso você opte por inicializar a api usando comandos do `pipenv run [script]`, a api vai funcionar normalmente. Caso você opte por iniciar a API usando `python [arquivo]` o arquivo database.db deve estar dentro da pasta app.

# Conexão com banco de dados

O ORM SqlAlchemy é usado nesse projeto para conexão com banco de dados, mapeamento das entidades, queries, inserts, updates e deletes.

Para esse projeto, as entidades estão mapeadas utilizando a estrutura declarativa. Nessa estrutura as entidades são modeladas como classes e as colunas como propriedades.

# A API

A API expõe serviços de leitura apenas, todos os serviços podem ser acessados utilizando a documentação do swagger pela url: `http://127.0.0.1:8000/docs`.


# Executando testes unitários

Os testes unitarios foram escritos usando pytest e pytest-mock. Para executar os testes unitários basta executar o comando a seguir na raiz do projeto:

`pipenv run tests`


# Executando a aplicação

A aplicação é inicializada usando a ferramenta uvicorn. Para inicializar a aplicação basta executar o comando a seguir:

`pipenv run app`


# Criando a imagem docker

As especificações da imagem Docker estão definidas no arquivo Dockerfile. Para criar o container localmente basta utilizar o comando a seguir:

`docker build -t 1mlet .`

Para iniciar a imagem docker localmente pode-se utilizar o comando a seguir:

`docker run -it --rm -p 8000:80 1mlet`

> O parâmetro -it inicializa o container em modo iterativo, e você vai ter acesso ao bash do container. O parâmetro exclui o container ao fim da execussão. O parâmetro -p é para o mapeamento da porta e permite o acesso à aplicação utilizando a url [http://localhost:8000](http://localhost:8000)
