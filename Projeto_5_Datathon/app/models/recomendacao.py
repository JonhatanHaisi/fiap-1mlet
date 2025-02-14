from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.pipeline import Pipeline
from sqlalchemy.orm import Session

import pandas as pd
import numpy as np
import datetime
import pickle

from models import models
from models import entities


TEXT_VECTORIZER: TfidfVectorizer = pickle.load(open("models/vectorizer_body.pkl", "rb"))
ACTIVITY_TRANSFORMER: Pipeline = pickle.load(open("models/transformer.pkl", "rb"))

def obter_recomendacao_usuario(usuario_id: str, session: Session):
    atividades = session.query(entities.Atividade).filter_by(usuario=usuario_id).all()
    if len(atividades) == 0:
        return obter_recomendacoes_cold_start()
    return obter_recomendacoes_personalizadas(usuario_id, session)


def obter_recomendacoes_cold_start():
    df = pd.read_csv("models/data/cold_start.csv")
    return [ 
        models.Recomendacao(id=row['page'], titulo=row['title'], descricao=row['caption'])
        for _, row in df.iterrows()
     ]

def obter_recomendacoes_personalizadas(usuario_id: str, session: Session):
    materia_mais_recente = session.query(entities.Materia).order_by(entities.Materia.publicado.desc()).first()
    data_limite = materia_mais_recente.publicado - datetime.timedelta(days=14)

    materias = session.query(entities.Materia).filter(entities.Materia.publicado >= data_limite).all()
    atividades = session.query(entities.Atividade).filter_by(usuario=usuario_id).all()

    materias = [ materia for materia in materias if materia.id not in [atividade.materia_id for atividade in atividades] ]

    X_atividades = TEXT_VECTORIZER.transform([atividade.materia.conteudo for atividade in atividades])
    X_materias = TEXT_VECTORIZER.transform([materia.conteudo for materia in materias])

    similatidades = np.array(cosine_similarity(X_atividades, X_materias))

    pesos_data_publicacao = np.array([1 - (materia.publicado - data_limite).days / 14 for materia in materias]) / 5
    
    features = [ (atividade.tempo_leitura, atividade.porcentagem_scroll) for atividade in atividades]
    pesos_atividade = ACTIVITY_TRANSFORMER.transform(features)
    pesos_atividade = np.mean(pesos_atividade, axis=1)

    similatidades = similatidades + pesos_data_publicacao + pesos_atividade

    indices = np.argsort(similatidades, axis=1)[:, -10:][0]
    return [ materias[ix] for ix in indices]
