# dados/carregar_dados.py

import pandas as pd
import streamlit as st
import numpy as np

def normalizar_posicoes(df):
    def limpar_posicao(pos):
        if pd.isna(pos):
            return pos
        pos = str(pos).strip()
        if "RAMF" in pos:
            return "RW"
        if "LAMF" in pos:
            return "LW"
        if "RDMF" in pos:
            return "DMF"
        if "LDMF" in pos:
            return "DMF"
        if "LCMF" in pos:
            return "CMF"
        if "RCMF" in pos:
            return "CMF"
        if "LWB" in pos:
            return "LB"
        if "RWB" in pos:
            return "RB"
        if "LWF" in pos:
            return "LW"
        if "RWF" in pos:
            return "RW"
        if "RCB" in pos:
            return "CB"
        if "LCB" in pos:
            return "CB"
        return pos.split(",")[0].strip()  # mantém só a primeira posição
    if "Posição" in df.columns:
        df["Posição"] = df["Posição"].apply(limpar_posicao)
    return df

def converter_colunas_numericas(df):
    for coluna in df.columns:
        if df[coluna].dtype == object and coluna != 'Pos.':
            try:
                df[coluna] = pd.to_numeric(df[coluna], errors='coerce')
            except:
                pass
    return df

@st.cache_data
def carregar_e_tratar_dados(path_principal, path_auxiliar=None):
    df = pd.read_excel(path_principal)
    df = converter_colunas_numericas(df)
    df = normalizar_posicoes(df)

    if 'Age' in df.columns:
        df['Age'] = df['Age'].astype(str).str.extract(r'(\d+)').astype(float)

    if '90s' in df.columns and df['90s'].sum() > 0:
        colunas_dividir = [
            "npxG", "xAG", "PrgC", "PrgP",
            "Golos sem ser por penálti", "Assistências"
        ]
        for col in colunas_dividir:
            if col in df.columns:
                df[f"{col}/90"] = df[col] / df['90s']

    if path_auxiliar:
        df_aux = pd.read_excel(path_auxiliar)
        df_aux = converter_colunas_numericas(df_aux)
        df_aux = normalizar_posicoes(df_aux)

        if 'Age' in df_aux.columns:
            df_aux['Age'] = df_aux['Age'].astype(str).str.extract(r'(\d+)').astype(float)
        return df, df_aux
    else:
        return df, None