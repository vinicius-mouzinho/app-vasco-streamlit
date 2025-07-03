import os
import pandas as pd
from utilitarios.funcoes_metricas import adicionar_metricas_derivadas
from dados.carregar_dados import normalizar_posicoes

CAMINHO_PADRAO = "dataframes"

def carregar_df(nome_arquivo):
    caminho = os.path.join(CAMINHO_PADRAO, nome_arquivo)
    
    if nome_arquivo.endswith('.pkl'):
        df = pd.read_pickle(caminho)
        df = df.copy()
        df.reset_index(drop=True, inplace=True)

        for col in df.columns:
            if isinstance(df[col].dtype, pd.CategoricalDtype):
                df[col] = df[col].astype(str)
            elif df[col].dtype == object:
                try:
                    df[col] = pd.to_numeric(df[col], errors='ignore')
                except Exception:
                    pass

    elif nome_arquivo.endswith('.csv'):
        df = pd.read_csv(caminho)
    elif nome_arquivo.endswith('.xlsx'):
        df = pd.read_excel(caminho)
    else:
        raise ValueError("Formato de arquivo não suportado.")

    # Adicionar coluna 'Liga' com base no nome do arquivo (sem extensão)
    if 'Liga' not in df.columns:
        nome_liga = os.path.splitext(nome_arquivo)[0]
        df['Liga'] = nome_liga


    # Remover coluna antiga se existir
    if 'Arquivo_Origem' in df.columns:
        df.drop(columns=['Arquivo_Origem'], inplace=True)

    df = normalizar_posicoes(df)
    df = adicionar_metricas_derivadas(df)
    return df
