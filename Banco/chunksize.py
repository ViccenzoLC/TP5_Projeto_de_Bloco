import pandas as pd
from Banco.conexao_banco import engine_conection

engine = engine_conection()
def chunksize():
    chunk = pd.read_csv('Arquivo_CSV_Professor/credit_card_transactions.csv', chunksize=1000)
    for i, chunk in enumerate(chunk):
        print(f'Processando chunk {i + 1}')
    

def buscar_cartoes(engine):
    try:
        query = """SELECT numero_cartao FROM cartoes_credito"""
        return pd.read_sql(query, engine)

    except Exception as erro:
        print(f"--Erro ao buscar dados: {erro}--")
def join_cartoes_transacoes(engine):
    try:
        if engine is not None:

            cartoes = buscar_cartoes(engine)

            if cartoes is not None:

                cartoes["numero_cartao"] = cartoes["numero_cartao"].astype(str)

                for chunk in pd.read_csv("Arquivo_CSV_Professor/credit_card_transactions.csv", chunksize=1000):
                    
                    chunk["cc_num"] = chunk["cc_num"].astype(str)
                    # cartoes["numero_cartao"] = cartoes["numero_cartao"].astype(str)
                    
                    
                    chunk = pd.merge(
                        chunk,
                        cartoes,
                        left_on="cc_num",
                        right_on="numero_cartao",
                        how="inner"
                    )
    except Exception as erro:
        print(erro)
    else:
        print(f"Resultado do Cruzamento de Dados (Merge): {chunk} registros")
        
def atm_maior_10mil():
    try:
        total = 0

        for chunk in pd.read_csv(
            "Arquivo_CSV_Professor/credit_card_transactions.csv",
            chunksize=1000
        ):
            total += (chunk["amt"] > 10000).sum()

    except Exception as erro:
        print(erro)
    else:
        print(f"Total de transações com ATM acima de 10000: {total}")