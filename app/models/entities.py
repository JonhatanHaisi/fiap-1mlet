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
    

class Grupo(Base):
    __tablename__ = 'grupo'
    
    id: Mapped[int] = mapped_column(INTEGER, autoincrement=True, primary_key=True)
    nome: Mapped[str] = mapped_column(VARCHAR(100), nullable=False)

    produtos: Mapped[list['Produto']] = relationship('Produto', back_populates='grupo')
    producao: Mapped[list['Producao']] = relationship('Producao', back_populates='grupo')
    comercializacao: Mapped[list['Comercializacao']] = relationship('Comercializacao', back_populates='grupo')

    def __repr__(self):
        return f'Grupo(id={self.id}, nome={self.nome})'


# mapeamento da tabela produto
# usando a estrutura declarativa do SQLAlchemy
class Produto(Base):
    __tablename__ = 'produto'
    
    id: Mapped[int] = mapped_column(INTEGER, autoincrement=True, primary_key=True)
    nome: Mapped[str] = mapped_column(VARCHAR(100), nullable=False)
    control: Mapped[str] = mapped_column(VARCHAR(100), nullable=False)
    grupo_id: Mapped[int] = mapped_column(ForeignKey('grupo.id'), nullable=False)

    grupo: Mapped['Grupo'] = relationship('Grupo', back_populates='produtos')
    producao: Mapped[list['Producao']] = relationship('Producao', back_populates='produto')
    comercializacao: Mapped[list['Comercializacao']] = relationship('Comercializacao', back_populates='produto')

    def __repr__(self):
        return f'Produto(id={self.id}, nome={self.nome})'


# mapeamento da tabela producao
# usando a estrutura declarativa do SQLAlchemy
class Producao(Base):
    __tablename__ = 'producao'
    
    id: Mapped[int] = mapped_column(INTEGER, autoincrement=True, primary_key=True)
    ano: Mapped[int] = mapped_column(INTEGER, nullable=False)
    quantidade: Mapped[int] = mapped_column(INTEGER, nullable=False)
    produto_id: Mapped[int] = mapped_column(ForeignKey('produto.id'), nullable=True)
    grupo_id: Mapped[int] = mapped_column(ForeignKey('grupo.id'), nullable=True)
    
    produto: Mapped['Produto'] = relationship('Produto', back_populates='producao')
    grupo: Mapped['Grupo'] = relationship('Grupo', back_populates='producao')

    def __repr__(self):
        return f'Producao(id={self.id}, ano={self.ano}, quantidade={self.quantidade}, produto_id={self.produto_id})'


# ==============================================================================
# COMERCIALIZAÇÃO
# ==============================================================================
class Comercializacao(Base):
    __tablename__ = 'comercializacao'

    id: Mapped[int] = mapped_column(
        INTEGER, autoincrement=True, primary_key=True)
    ano: Mapped[int] = mapped_column(INTEGER, nullable=False)
    quantidade: Mapped[int] = mapped_column(INTEGER, nullable=False)
    produto_id: Mapped[int] = mapped_column(
        ForeignKey('produto.id'), nullable=True)
    grupo_id: Mapped[int] = mapped_column(
        ForeignKey('grupo.id'), nullable=True)

    produto: Mapped['Produto'] = relationship(
        'Produto', back_populates='comercializacao')
    grupo: Mapped['Grupo'] = relationship('Grupo', back_populates='comercializacao')

    def __repr__(self):
        return f'Comercializacao(id={self.id}, ano={self.ano}, quantidade={self.quantidade}, produto_id={self.produto_id})'