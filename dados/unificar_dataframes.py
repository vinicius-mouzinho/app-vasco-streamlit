import pandas as pd
import os
import streamlit as st

@st.cache_data
def unificar_dataframes(pasta="dataframes"):
    arquivos = [arq for arq in os.listdir(pasta) if arq.endswith(('.xlsx', '.csv', '.pkl'))]
    lista_df = []

    for arquivo in arquivos:
        caminho = os.path.join(pasta, arquivo)
        nome_liga = os.path.splitext(arquivo)[0]  # Ex: 'Argentina 2025'

        try:
            if arquivo.endswith('.xlsx'):
                df = pd.read_excel(caminho)
            elif arquivo.endswith('.csv'):
                df = pd.read_csv(caminho)
            elif arquivo.endswith('.pkl'):
                df = pd.read_pickle(caminho)
            else:
                continue

            # Adiciona coluna 'Liga' com nome limpo do arquivo
            df['Liga'] = nome_liga

            # Remove coluna antiga se existir
            if 'Arquivo_Origem' in df.columns:
                df.drop(columns=['Arquivo_Origem'], inplace=True)
            if 'Fonte' in df.columns:
                df.drop(columns=['Fonte'], inplace=True)

            # Adiciona à lista
            lista_df.append(df)

        except Exception as e:
            print(f"Erro ao carregar {arquivo}: {e}")

    if lista_df:
        df_unificado = pd.concat(lista_df, ignore_index=True)
        return df_unificado
    else:
        return pd.DataFrame()
