import os;
import pandas as pd;
import requests;

url = "https://brasilapi.com.br/api/banks/v1"
def get_data():
    try:
        dados_resposta = requests.get(url,timeout=10)
        dados_resposta.raise_for_status() 
        db = dados_resposta.json()
        
    except requests.exceptions.RequestException as erro:
        print(f"--Erro na chamda--: {erro}")
    else:
        df = pd.DataFrame(db)
        print('-- Dados obtidos com sucesso!--')
        return df
    
    