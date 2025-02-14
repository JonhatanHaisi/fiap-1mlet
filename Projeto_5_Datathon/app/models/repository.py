from infra.database import Session
from models import entities

class AtividadeRepository:

    def __init__(self, session:Session):
        self._session = session

    def listar_atividade_usuario(self, usuario_id:str):
        return self._session.query(entities.Atividade).filter_by(usuario=usuario_id).all()

    def salvar_atividade_usuario(self, atividade: entities.Atividade):
        self._session.add(atividade)
        return atividade


