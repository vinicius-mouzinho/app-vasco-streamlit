# utilitarios/estruturas_tabela.py

# Colunas que sempre estarão presentes em qualquer tabela
COLUNAS_FIXAS = [
    "Jogador",
    "Equipa",
    "Posição",
    "Idade",
    "Minutos jogados:"
]

# Categorias de métricas por tipo de tabela
TIPOS_TABELA = {
    "Finalização": [
        "Golos", "Golos/90", "Golos sem ser por penálti", "Golos sem ser por penálti/90",
        "Golos esperados", "Golos esperados/90", "Gols esperados (sem pênaltis)/90", "Golos de cabeça", "Golos de cabeça/90",
        "Remate", "Remates/90", "Remates à baliza/90", "Remates à baliza, %",
        "Golos marcados, %", "Toques na área/90", "Penaltis marcados", "Conversão de pênaltis, %"
    ],
    "Último Passe": [
        "Assistências", "Assistências/90", "Assistências esperadas", "Assistências esperadas/90",
        "Assistências esperadas por 100 passes", "Assistências para remate/90",
        "Passes inteligentes/90", "Passes inteligentes certos, %",
        "Passes para a área de penálti/90", "Passes para a área de penálti, %",
        "Passes em profundidade/90", "Passes em profundidade certos, %",
        "Cruzamentos/90", "Cruzamentos certos, %"
    ],
    "Construção de jogo": [
        "Ações com a bola/90", "Passes/90", "Passes certos, %",
        "Passes para a frente/90", "Passes para a frente certos, %",
        "Passes longos/90", "Passes longos certos, %",
        "Passes para terço final/90", "Passes certos para terço final, %",
        "Passes progressivos/90", "Passes progressivos certos, %",
        "Passes recebidos/90", "Perdas de bola/90", "Perdas de bola a cada 100 ações"
    ],
    "Drible e 1x1": [
        "Dribles/90", "Dribles com sucesso, %", "Dribles certos/ 90", "Frequência no drible (%)",
        "Acelerações/90", "Corridas progressivas/90", "Duelos ofensivos/90", "Duelos ofensivos ganhos, %",
        "Toques na área/90"
    ]
}

def selecionar_colunas(df, tipo_tabela):
    """
    Retorna um DataFrame com todas as colunas (se tipo_tabela = 'Completa'),
    ou com as colunas fixas + as colunas específicas do tipo de tabela.
    """
    if tipo_tabela == "Completa":
        return df  # Mostra todas as colunas do DataFrame original

    if tipo_tabela not in TIPOS_TABELA:
        return df[COLUNAS_FIXAS]

    colunas_desejadas = COLUNAS_FIXAS + [
        col for col in TIPOS_TABELA[tipo_tabela] if col in df.columns
    ]
    return df[colunas_desejadas]
