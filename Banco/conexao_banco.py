import os
from sqlalchemy import create_engine;
import pandas as pd;
from dotenv import load_dotenv
 
load_dotenv()

driver = os.getenv("DB_DRIVE")
usuario = os.getenv("DB_USERNAME")
senha = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
porta = os.getenv("DB_PORT")
banco = os.getenv("DB_NAME")
    
def engine_conection():
    engine_url = f"{driver}://{usuario}:{senha}@{host}:{porta}/{banco}"

    engine = create_engine(engine_url)
    try:
        with engine.connect() as conexao:
            print("-- Conexao realizada com sucesso! --")
    except Exception as erro:
        print(f"-- Erro na conexao: {erro} --")
        return None
    else:
        return engine
 
engine_conection()   
def to_sql(df, engine):
    try:
        df.to_sql('bancos_parceiros', engine, if_exists='replace', index=False)
        print('--Dados inseridos com sucesso!--')
    except Exception as erro:
        print(f"--Erro ao inserir dados: {erro}--")
        
