import os
import pandas as pd
from utilitarios.funcoes_metricas import adicionar_metricas_derivadas
from dados.carregar_dados import normalizar_posicoes  # ✅ IMPORTAR AQUI

CAMINHO_PADRAO = "dataframes"

def carregar_df(nome_arquivo):
    caminho = os.path.join(CAMINHO_PADRAO, nome_arquivo)
    
    if nome_arquivo.endswith('.pkl'):
        df = pd.read_pickle(caminho)
    elif nome_arquivo.endswith('.csv'):
        df = pd.read_csv(caminho)
    elif nome_arquivo.endswith('.xlsx'):
        df = pd.read_excel(caminho)
    else:
        raise ValueError("Formato de arquivo não suportado.")

    df = normalizar_posicoes(df)  # ✅ APLICAR NORMALIZAÇÃO
    df = adicionar_metricas_derivadas(df)
    return df
