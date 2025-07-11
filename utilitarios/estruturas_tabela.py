# utilitarios/estruturas_tabela.py

# Colunas que sempre estarão presentes em qualquer tabela
COLUNAS_FIXAS = [
    "Jogador",
    "Equipa",
    "Equipa na liga analisada",
    "Posição",
    "Idade",
    "Minutos jogados:"
]

# Colunas que devem sempre ficar fixas no início da tabela (usadas para ordenação visual)
COLUNAS_FIXAS_VISUAL = [
    "Jogador", "Posição", "Equipa", "Equipa na liga analisada", "Idade", "Liga"
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
    ],
    "GOLEIROS": [
    "Golos sofridos", "Golos sofridos/90", "Remates sofridos", "Remates sofridos/90",
    "Jogos sem sofrer gols", "Defesas, %", "Golos sofridos esperados",
    "Golos sofridos esperados/90", "Golos expectáveis defendidos", "Golos expectáveis defendidos por 90"
    ]
}


COLUNAS_EXCLUIR_COMPLETA = [
        'Emprestado', 'Ações defensivas com êxito/90', 'Duelos defensivos/90',
        'Cortes de carrinho ajust. à posse', 'Interseções/90',
        'Cartões amarelos', 'Cartões amarelos/90', 'Cartões vermelhos', 'Cartões vermelhos/90',
        'Acções atacantes com sucesso/90', 'Remate',
        'Cruzamentos do flanco esquerdo/90', 'Cruzamentos precisos do flanco esquerdo, %',
        'Cruzamentos do flanco direito/90', 'Cruzamentos precisos do flanco direito, %',
        'Passes para trás/90', 'Passes para trás certos, %',
        'Passes laterais/90', 'Passes laterais certos, %',
        'Comprimento médio de passes, m', 'Comprimento médio de passes longos, m',
        'Segundas assistências/90', 'Terceiras assistências/90', 'Passes chave/90',
        'Receção de passes em profundidade/90', 'Cruzamentos em profundidade recebidos/90'
    ]

def selecionar_colunas(df, tipo_tabela):
    if tipo_tabela == "Completa":
        colunas_desejadas = [col for col in df.columns if col not in COLUNAS_EXCLUIR_COMPLETA]
    elif tipo_tabela in TIPOS_TABELA:
        colunas_desejadas = TIPOS_TABELA[tipo_tabela]
    else:
        colunas_desejadas = []

    # Garante que as colunas fixas estão no início sem duplicar
    colunas_existentes = [col for col in COLUNAS_FIXAS_VISUAL if col in df.columns]
    colunas_metricas = [
        col for col in colunas_desejadas
        if col in df.columns and col not in colunas_existentes
    ]

    colunas_unificadas = colunas_existentes + colunas_metricas
    return df[colunas_unificadas]
