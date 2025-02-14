from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Integer, ForeignKey, Column, String, DateTime

import uuid


class Base(DeclarativeBase):
    pass


class Materia(Base):
    __tablename__ = 'materias'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    titulo = Column(String, nullable=False)
    descricao = Column(String, nullable=False)
    conteudo = Column(String, nullable=False)
    publicado = Column(DateTime, nullable=False)

    atividades = relationship("Atividade", back_populates="materia", cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Materia {self.id}, titulo={self.titulo[:10]}..., descricao={self.descricao[:10]}..., ' \
               f'conteudo={self.conteudo[:30]}..., publicado={self.publicado}>'


class Atividade(Base):
    __tablename__ = 'atividades'

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario = Column(String, nullable=False)
    materia_id = Column(String, ForeignKey('materias.id'), nullable=False)
    tempo_leitura = Column(Integer, nullable=False)
    porcentagem_scroll = Column(Integer, nullable=False)

    materia = relationship("Materia", back_populates="atividades")

    def __repr__(self):
        return f'<Atividade {self.id}, usuario={self.usuario}, ' \
               f'materia={self.materia_id}, tempo_leitura={self.tempo_leitura}, ' \
               f'porcentagem_scroll={self.porcentagem_scroll}>'

