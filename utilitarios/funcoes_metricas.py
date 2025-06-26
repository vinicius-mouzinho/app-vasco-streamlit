import pandas as pd

def adicionar_metricas_derivadas(df):
    df['Ações com a bola'] = df['Passes/90'] + df['Cruzamentos/90'] + df['Dribles/90'] + df['Remates/90']
    df['Possession Adjustment'] = df['Interceções ajust. à posse'] / df['Interseções/90']
    df['Ações Defensivas por 30\' de Posse Adversária'] = df['Ações defensivas com êxito/90'] * df['Possession Adjustment']
    df['Dribles certos/ 90'] = df['Dribles/90'] * df['Dribles com sucesso, %'] / 100
    df['Duelos Defensivos por 30\' de Posse Adversária'] = df['Duelos defensivos/90'] * df['Possession Adjustment']
    df['Passes precisos para a área de penalti/90'] = df['Passes para a área de penálti/90'] * df['Passes precisos para a área de penálti, %'] / 100
    df['Passes progressivos certos/90'] = df['Passes progressivos/90'] * df['Passes progressivos certos, %'] / 100
    df['Passes progressivos fora da área/90'] = df['Passes progressivos certos/90'] - df['Passes precisos para a área de penalti/90']
    df['Remates à baliza/90'] = df['Remates/90'] * df['Remates à baliza, %'] / 100
    df['Perdas de bola'] = (
        (df['Passes/90'] * (100 - df['Passes certos, %']) / 100) +
        (df['Dribles/90'] * (100 - df['Dribles com sucesso, %']) / 100) +
        (df['Remates/90'] * (100 - df['Remates à baliza, %']) / 100) +
        (df['Cruzamentos/90'] * (100 - df['Cruzamentos certos, %']) / 100)
    )
    df['Frequência no drible (%)'] = 100 * df['Dribles/90'] / df['Ações com a bola']
    return df

from scipy.stats import zscore

import pandas as pd
from scipy.stats import zscore, percentileofscore

def gerar_ranking_zscore(df, perfil):
    if perfil == "Extremo de força":
        # 🔹 Defina as métricas e pesos do perfil
        metricas_pesos = {
            'Acelerações/90': 2.0,
            'Corridas progressivas/90': 2.0,
            'Dribles/90': 2.0,
            'Duelos ofensivos/90': 1.5,
            'Duelos ofensivos ganhos, %': 1.5,
            'Duelos/90': 1.0,
            'Duelos ganhos, %': 1.0
        }

        # 🔹 Filtra jogadores com dados disponíveis nas métricas
        colunas_disponiveis = [m for m in metricas_pesos if m in df.columns]
        if not colunas_disponiveis:
            return None

        df_filtrado = df.dropna(subset=colunas_disponiveis).copy()

        # 🔹 Calcula Z-Score padronizado por métrica
        for metrica in colunas_disponiveis:
            df_filtrado[f"z_{metrica}"] = zscore(df_filtrado[metrica])

        # 🔹 Calcula o z-score ponderado (pontuação final)
        df_filtrado["Z-Score"] = sum(
            df_filtrado[f"z_{metrica}"] * peso
            for metrica, peso in metricas_pesos.items()
            if f"z_{metrica}" in df_filtrado.columns
        )

        # 🔹 Percentil baseado no Z-Score
        df_filtrado["Percentil"] = df_filtrado["Z-Score"].apply(
            lambda x: round(percentileofscore(df_filtrado["Z-Score"], x), 2)
        )

        # 🔹 Seleciona colunas para exibir
        colunas_exibir = ['Jogador', 'Equipa', 'Posição', 'Idade', 'Z-Score', 'Percentil']
        for col in colunas_exibir:
            if col not in df_filtrado.columns:
                df_filtrado[col] = None

        df_resultado = df_filtrado[colunas_exibir].sort_values(by="Z-Score", ascending=False).reset_index(drop=True)
        return df_resultado

    # Se o perfil não for reconhecido
    return None
