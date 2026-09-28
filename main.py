#c:\Users\vicce\Documents\TP5 DE PROJETO DE BLOCO\venv\Scripts\
import os;
from flask import Flask, jsonify, request;
from flask_sqlalchemy import SQLAlchemy
from Dados.pegar_dados import get_data
from Banco.conexao_banco import engine_conection, to_sql
from Dados.tratamento_csv import tratar_dados
from Banco.chunksize import chunksize
import pandas as pd
from Banco.chunksize import join_cartoes_transacoes,atm_maior_10mil
from Banco.fraudes import gerar_relatorio_fraudes
engine = engine_conection()


opcao = input("qual parte do tp deseja rodar: 1,2,3 ")

df = get_data()
if opcao == "1":
    if df is not None:
        df_tratado = tratar_dados(df)

        if df_tratado is not None:
            engine = engine_conection()

            if engine is not None:
                to_sql(df_tratado, engine)

if opcao == "2":
    chunksize()

    if engine is not None:
        cartoes = join_cartoes_transacoes(engine)

    if cartoes is not None:
        print(cartoes)
    atm_maior_10mil()
    gerar_relatorio_fraudes(engine)