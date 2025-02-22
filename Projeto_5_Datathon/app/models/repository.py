from infra.database import Session
from models.entities import Atividade

class AtividadeRepository:

    def __init__(self, session:Session):
        self._session = session

    def listar_atividade_usuario(self, usuario_id:str):
        return self._session.query(Atividade).filter_by(usuario=usuario_id).all()

    def salvar_atividade_usuario(self, atividade: Atividade):
        self._session.add(atividade)
        return atividade


