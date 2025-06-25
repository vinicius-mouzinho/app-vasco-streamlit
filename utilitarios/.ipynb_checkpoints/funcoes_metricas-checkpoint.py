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
