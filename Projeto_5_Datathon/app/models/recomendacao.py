from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.pipeline import Pipeline
from sqlalchemy.orm import Session

import pandas as pd
import numpy as np
import datetime
import pickle

from models.models import Recomendacao
from models.entities import Materia, Atividade


TEXT_VECTORIZER: TfidfVectorizer = pickle.load(open("models/vectorizer_body.pkl", "rb"))
ACTIVITY_TRANSFORMER: Pipeline = pickle.load(open("models/transformer.pkl", "rb"))

async def obter_recomendacao_usuario(usuario_id: str, session: Session):
    exists_atividade = session.query(Atividade).filter_by(usuario=usuario_id).first()
    if exists_atividade is None:
        return await obter_recomendacoes_cold_start()
    return await obter_recomendacoes_personalizadas(usuario_id, session)


async def obter_recomendacoes_cold_start():
    df = pd.read_csv("models/data/cold_start.csv")
    return [ 
        Recomendacao(id=row['page'], titulo=row['title'], descricao=row['caption'])
        for _, row in df.iterrows()
     ]

async def obter_recomendacoes_personalizadas(usuario_id: str, session: Session):
    materias = session.query(Materia).order_by(Materia.publicado.desc()).limit(100).all()
    atividades = session.query(Atividade).filter_by(usuario=usuario_id).all()

    materias_lidas = [atividade.materia_id for atividade in atividades]
    materias = [ materia for materia in materias if materia.id not in materias_lidas ]

    X_atividades = TEXT_VECTORIZER.transform([atividade.materia.conteudo for atividade in atividades])
    X_materias = TEXT_VECTORIZER.transform([materia.conteudo for materia in materias])

    similatidades = np.array(cosine_similarity(X_atividades, X_materias))

    datas = np.array([mat.publicado for mat in materias])
    pesos_data_publicacao = (datas - datas.min()) / (datas.max() - datas.min()) / 5
    
    features = [ (atividade.tempo_leitura, atividade.porcentagem_scroll) for atividade in atividades]
    pesos_atividade = ACTIVITY_TRANSFORMER.transform(features)
    pesos_atividade = np.mean(pesos_atividade, axis=1)

    similatidades = similatidades + pesos_data_publicacao + pesos_atividade

    indices = np.argsort(similatidades, axis=1)[:, -10:][0]
    return [ materias[ix] for ix in indices]
