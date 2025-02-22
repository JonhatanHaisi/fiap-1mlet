from sqlalchemy.orm import Session
from sqlalchemy import create_engine


# Cria uma sessão para interagir com o banco de dados
_engine = create_engine('mysql://root:root@localhost/recomendacao', echo=False)


# Função que cria uma sessão para interagir com o banco de dados
# essa função é um gerador que cria uma sessão e a fecha ao finalizar
def create_session():
    session = Session(_engine)
    try:
        yield session
    finally:
        session.close()
