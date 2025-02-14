from pydantic import BaseModel, Field

from models import entities


class AtividadeBody(BaseModel):
    '''Modelo de atividade do usuário'''

    usuario: str = Field(...) # id do usuário que realizou a atividade. Provavelmente UUID
    materia: str = Field(...) # id da matéria que o usuário estava lendo. Provavelmente UUID
    tempo_leitura: int = Field(..., alias='tempoLeitura') # tempo que o usuário ficou lendo a matéria em segundos
    porcentagem_scroll: int = Field(..., alias='porcentagemScroll') # porcentagem que o usuário leu da matéria

    def to_entity(self):
        return entities.Atividade(
            usuario=self.usuario,
            materia_id=self.materia,
            tempo_leitura=self.tempo_leitura,
            porcentagem_scroll=self.porcentagem_scroll
        )

    class Config:
        from_attributes = True
        populate_by_name = True


class AtividadeResponse(BaseModel):
    '''Modelo de atividade como response de requisições'''

    materia: 'Materia' = Field(...) # matéria recomendada
    tempo_leitura: int = Field(..., alias='tempoLeitura') # tempo que o usuário ficou lendo a matéria em segundos
    porcentagem_scroll: int = Field(..., alias='porcentagemScroll') # porcentagem que o usuário leu da matéria

    class Config:
        from_attributes = True
        populate_by_name = True


class Materia(BaseModel):
    '''Modelo de matéria'''

    id: str = Field(...) # id da matéria
    titulo: str = Field(...) # título da matéria
    descricao: str = Field(...) # descrição da matéria

    class Config:
        from_attributes = True
        populate_by_name = True


class Recomendacao(BaseModel):
    '''Modelo de recomendação de matéria'''

    id: str = Field(...) # id da matéria
    titulo: str = Field(...) # título da matéria
    descricao: str = Field(...) # descrição da matéria

    class Config:
        from_attributes = True
        populate_by_name = True
