from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import VARCHAR, INTEGER, ForeignKey


# O sqlalchemy requer uma classe base para criar as tabelas no banco de dados.
# A classe Base é uma subclasse de DeclarativeBase, que é uma classe do SQLAlchemy.
# A classe Base é a superclasse de todas as classes que representam as tabelas do banco de dados.
class Base(DeclarativeBase):
    pass


# mapeamento da tabela users
# usando a estrutura declarativa do SQLAlchemy
class User(Base):
    __tablename__ = 'users' # nome da tabela no banco de dados
    
    id: Mapped[int] = mapped_column(INTEGER, primary_key=True) # mapeamento da coluna id
    username: Mapped[str] = mapped_column(VARCHAR(100), nullable=False) # mapeamento da coluna username
    password: Mapped[str] = mapped_column(VARCHAR(100), nullable=False) # mapeamento da coluna password

    def __repr__(self):
        return f'User(id={self.id}, username={self.username})'
    

# mapeamento da tabela produto
# usando a estrutura declarativa do SQLAlchemy
class Produto(Base):
    __tablename__ = 'produto'
    
    id: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    nome: Mapped[str] = mapped_column(VARCHAR(100), nullable=False)

    producao: Mapped[list['Producao']] = relationship('Producao', back_populates='produto')

    def __repr__(self):
        return f'Produto(id={self.id}, nome={self.nome})'


# mapeamento da tabela producao
# usando a estrutura declarativa do SQLAlchemy
class Producao(Base):
    __tablename__ = 'producao'
    
    id: Mapped[int] = mapped_column(INTEGER, autoincrement=True, primary_key=True)
    ano: Mapped[int] = mapped_column(INTEGER, nullable=False)
    quantidade: Mapped[int] = mapped_column(INTEGER, nullable=False)
    produto_id: Mapped[int] = mapped_column(ForeignKey('produto.id'), nullable=False)
    
    produto: Mapped['Produto'] = relationship('Produto', back_populates='producao')

    def __repr__(self):
        return f'Producao(id={self.id}, ano={self.ano}, quantidade={self.quantidade}, produto_id={self.produto_id})'
