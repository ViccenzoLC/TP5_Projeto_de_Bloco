"""Identifica transacoes com numero de cartao acima de 16 digitos."""

from pathlib import Path

import pandas as pd

from Banco.conexao_banco import engine_conection


PASTA_PROJETO = Path(__file__).resolve().parent.parent
ARQUIVO_TRANSACOES = PASTA_PROJETO / "Arquivo_CSV_Professor" / "credit_card_transactions.csv"
ARQUIVO_JSON = Path(__file__).resolve().parent / "fraudes.json"
TABELA_AUDITORIA = "auditoria_fraudes"


def gerar_relatorio_fraudes(
    engine,
    arquivo_csv=ARQUIVO_TRANSACOES,
    arquivo_json=ARQUIVO_JSON,
    tabela=TABELA_AUDITORIA,
    tamanho_bloco=100_000,
):
    
    if engine is None:
        raise ValueError("Uma conexao valida com o banco de dados e necessaria.")
    if tamanho_bloco <= 0:
        raise ValueError("tamanho_bloco deve ser maior que zero.")

    arquivo_csv = Path(arquivo_csv)
    arquivo_json = Path(arquivo_json)
    if not arquivo_csv.is_file():
        raise FileNotFoundError(f"Arquivo de transacoes nao encontrado: {arquivo_csv}")

    blocos_fraude = []
    deslocamento = 0
    colunas_csv = pd.read_csv(arquivo_csv, nrows=0).columns.tolist()

    for bloco in pd.read_csv(
        arquivo_csv,
        chunksize=tamanho_bloco,
        dtype={"cc_num": "string"},
    ):
        if "cc_num" not in bloco.columns:
            raise ValueError("O CSV precisa conter a coluna 'cc_num'.")

        cartoes = bloco["cc_num"].str.strip()
        suspeitos = cartoes.str.fullmatch(r"\d+", na=False) & cartoes.str.len().gt(16)
        fraudes = bloco.loc[suspeitos].copy()

        if not fraudes.empty:
            if "Unnamed: 0" in fraudes.columns:
                fraudes = fraudes.rename(columns={"Unnamed: 0": "fraud_id"})
            elif "fraud_id" not in fraudes.columns:
                if "trans_num" in fraudes.columns:
                    fraudes.insert(0, "fraud_id", fraudes["trans_num"])
                else:
                    fraudes.insert(
                        0,
                        "fraud_id",
                        [
                            deslocamento + indice
                            for indice, eh_fraude in enumerate(suspeitos)
                            if eh_fraude
                        ],
                    )

            fraudes["fraud_reason"] = (
                "numero do cartao ATM possui mais de 16 digitos"
            )
            blocos_fraude.append(fraudes)

        deslocamento += len(bloco)

    if blocos_fraude:
        relatorio = pd.concat(blocos_fraude, ignore_index=True)
    else:
        if "Unnamed: 0" in colunas_csv:
            colunas_csv[colunas_csv.index("Unnamed: 0")] = "fraud_id"
        elif "fraud_id" not in colunas_csv:
            colunas_csv.insert(0, "fraud_id")
        colunas_csv.append("fraud_reason")
        relatorio = pd.DataFrame(columns=colunas_csv)

    relatorio.to_sql(tabela, engine, if_exists="replace", index=False)
    arquivo_json.parent.mkdir(parents=True, exist_ok=True)
    relatorio.to_json(
        arquivo_json,
        orient="records",
        force_ascii=False,
        indent=2,
    )

    print(
        f"Relatorio de {len(relatorio)} fraude(s) salvo na tabela "
        f"'{tabela}' e em {arquivo_json}."
    )
    return relatorio


if __name__ == "__main__":
    conexao = engine_conection()
    if conexao is None:
        raise RuntimeError("Nao foi possivel conectar ao banco de dados.")

    