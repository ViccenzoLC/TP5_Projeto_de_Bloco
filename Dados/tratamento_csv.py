
def tratar_dados(df):
    try:
        df = df[['ispb', 'name', 'code']]

        df = df.rename(columns={
            'name': 'nome',
            'code': 'codigo'
        
        })
    except KeyError as erro:
        print(erro)
    else:
        return df