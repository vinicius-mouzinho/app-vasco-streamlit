# utilitarios/funcoes_metricas.py

import pandas as pd
from scipy.stats import zscore

def adicionar_metricas_derivadas(df):
    df['Ações com a bola/90'] = df['Passes/90'] + df['Cruzamentos/90'] + df['Dribles/90'] + df['Remates/90']
    df['Possession Adjustment'] = df['Interceções ajust. à posse'] / df['Interseções/90']
    df['Ações Defensivas por 30\' de Posse Adversária'] = df['Ações defensivas com êxito/90'] * df['Possession Adjustment']
    df['Dribles certos/ 90'] = df['Dribles/90'] * df['Dribles com sucesso, %'] / 100
    df['Duelos Defensivos por 30\' de Posse Adversária'] = df['Duelos defensivos/90'] * df['Possession Adjustment']
    df['Passes precisos para a área de penalti/90'] = df['Passes para a área de penálti/90'] * df['Passes precisos para a área de penálti, %'] / 100
    df['Passes progressivos certos/90'] = df['Passes progressivos/90'] * df['Passes progressivos certos, %'] / 100
    df['Passes progressivos fora da área/90'] = df['Passes progressivos certos/90'] - df['Passes precisos para a área de penalti/90']
    df['Remates à baliza/90'] = df['Remates/90'] * df['Remates à baliza, %'] / 100
    df['Perdas de bola/90'] = (
        (df['Passes/90'] * (100 - df['Passes certos, %']) / 100) +
        (df['Dribles/90'] * (100 - df['Dribles com sucesso, %']) / 100) +
        (df['Remates/90'] * (100 - df['Remates à baliza, %']) / 100) +
        (df['Cruzamentos/90'] * (100 - df['Cruzamentos certos, %']) / 100)
    )
    df['Frequência no drible (%)'] = 100 * df['Dribles/90'] / df['Ações com a bola/90']
    df['Assistências esperadas por 100 passes'] = df['Assistências esperadas/90'] / df['Passes/90'] * 100
    df['Perdas de bola a cada 100 ações'] = df['Perdas de bola/90'] / df['Ações com a bola/90'] * 100
    df['Gols esperados (sem pênaltis)/90'] = (
    (df['Golos esperados'] - (df['Penaltis marcados'] * 0.74)) / (df['Minutos jogados:'] / 90)
)
    return df


def gerar_ranking_zscore(df, metricas, pesos=None):
    if not metricas:
        return None

    df_rank = df.copy()
    df_rank = df_rank.dropna(subset=metricas)

    for metrica in metricas:
        df_rank[f"z_{metrica}"] = zscore(df_rank[metrica].astype(float))

    if pesos:
        df_rank['Z-Score'] = sum(df_rank[f"z_{m}"] * pesos.get(m, 1.0) for m in metricas)
    else:
        df_rank['Z-Score'] = df_rank[[f"z_{m}" for m in metricas]].mean(axis=1)

    df_rank['Percentil'] = df_rank['Z-Score'].rank(pct=True) * 100

    # ✅ Incluir 'Liga' se ela estiver presente no DataFrame original
    colunas_base = [col for col in ['Jogador', 'Posição', 'Equipa', 'Liga'] if col in df.columns]
    colunas_exibir = colunas_base + ['Z-Score', 'Percentil'] + metricas

    return df_rank[colunas_exibir].sort_values(by='Z-Score', ascending=False).reset_index(drop=True)
