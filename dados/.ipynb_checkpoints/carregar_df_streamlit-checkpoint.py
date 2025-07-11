# dados/carregar_df_streamlit

import os
import pandas as pd
from utilitarios.funcoes_metricas import adicionar_metricas_derivadas
from dados.carregar_dados import normalizar_posicoes
import streamlit as st

CAMINHO_PADRAO = "dataframes"

@st.cache_data
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

    # Garante que a coluna 'Liga' existe e não sobrescreve se já estiver correta
    if 'Liga' not in df.columns or df['Liga'].isnull().all():
        nome_liga = os.path.splitext(nome_arquivo)[0]
        df['Liga'] = nome_liga

    if 'Equipa na liga analisada' in df.columns:
        pass  # já está com o nome correto
    elif 'Equipa dentro de um período de tempo seleccionado' in df.columns:
        df.rename(columns={'Equipa dentro de um período de tempo seleccionado': 'Equipa na liga analisada'}, inplace=True)

    # Remover coluna antiga se existir
    if 'Arquivo_Origem' in df.columns:
        df.drop(columns=['Arquivo_Origem'], inplace=True)

    df = normalizar_posicoes(df)
    df = adicionar_metricas_derivadas(df)

    # Garante que a coluna 'Idade' está como inteiro (Int64 = permite nulos)
    if "Idade" in df.columns:
        df["Idade"] = pd.to_numeric(df["Idade"], errors="coerce").astype("Int64")

    return df

def listar_arquivos_sem_extensao(pasta=CAMINHO_PADRAO):
    arquivos = sorted([
        arq for arq in os.listdir(pasta)
        if arq.endswith(('.xlsx', '.csv', '.pkl'))
    ])
    return {os.path.splitext(arq)[0]: arq for arq in arquivos}
