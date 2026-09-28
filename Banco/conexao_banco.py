from sqlalchemy import create_engine;
import pandas as pd;
 
def engine_conection():
    engine_url ={
        'drivername': 'postgresql+psycopg2',
        'username': 'postgres',
        'password': '32243591Vi.',
        'host': 'localhost',
        'port': 5432,
        'database': 'postgres'
    }
    engine = create_engine("{drivername}://{username}:{password}@{host}:{port}/{database}".format(**engine_url))
    try:
        with engine.connect() as conexao:
            print("-- Conexao realizada com sucesso! --")
    except Exception as erro:
        print(f"-- Erro na conexao: {erro} --")
        return None
    else:
        return engine
    
    
def to_sql(df, engine):
    try:
        df.to_sql('bancos_parceiros', engine, if_exists='replace', index=False)
        print('--Dados inseridos com sucesso!--')
    except Exception as erro:
        print(f"--Erro ao inserir dados: {erro}--")
        
