# utilitarios/constantes.py

# Traduções das métricas para uso nos relatórios
metricas_traduzidas = {
    "Golos sem ser por penálti/90": "Gols (sem pênaltis) por 90'",
    "Assistências/90": "Assistências por 90'",
    "Assistências esperadas/90": "Assistências Esperadas por 90'",
    "Passes progressivos fora da área/90": "Passes Progressivos Fora da Área por 90'",
    "Toques na área/90": "Toques na Área por 90'",
    "Passes para a área de penálti/90": "Passes para a Área por 90'",
    "Remates/90": "Finalizações por 90'",
    "Remates à baliza, %": "Acerto no chute (%)",
    "Passes/90": "Passes por 90'",
    "Passes certos, %": "Acerto no Passe (%)",
    "Cruzamentos/90": "Cruzamentos por 90'",
    "Cruzamentos certos, %": "Precisão nos cruzamentos (%)",
    "Dribles certos/ 90": "Dribles Certos por 90'",
    "Faltas sofridas/90": "Faltas Sofridas por 90'",
    "Duelos ofensivos/90": "Duelos Ofensivos por 90'",
    "Duelos ofensivos ganhos, %": "Eficiência nos Duelos Ofensivos (%)",
    "Duelos defensivos/90": "Duelos Defensivos por 90'",
    "Duelos defensivos ganhos, %": "Eficiência nos Duelos Defensivos (%)",
    "Duelos/90": "Duelos por 90'",
    "Duelos ganhos, %": "Eficiência nos Duelos (%)",
    "Ações Defensivas por 30' de Posse Adversária": "Ações Defensivas por 30' de Posse Adversária",
    "Passes progressivos/90": "Passes Progressivos por 90'",
    "Passes progressivos certos, %": "Precisão nos Passes Progressivos (%)",
    "Corridas progressivas/90": "Corridas Progressivas por 90'",
    "Duelos Defensivos por 30' de Posse Adversária": "Duelos Defensivos por 30' de Posse Adversária",
    "Golos marcados, %": "Conversão de Gols (%)",
    "Dribles/90": "Dribles tentados por 90'",
    "Dribles com sucesso, %": "Eficiência nos Dribles (%)",
    "Passes longos recebidos/90": "Passes Longos Recebidos por 90'",
    "Duelos aérios/90": "Duelos Aéreos por 90'",
    "Duelos aéreos ganhos, %": "Duelos Aéreos Ganhos (%)",
    "Passes progressivos certos/90": "Passes Progressivos Certos por 90'",
    "Passes curtos / médios /90": "Passes curtos/médios por 90'",
    "Passes curtos / médios precisos, %": "Eficiência nos passes curtos/médios (%)",
    "Passes longos/90": "Passes longos por 90'",
    "Passes longos certos, %": "Eficiência nos passes longos (%)",
    "Faltas/90": "Faltas por 90'"
}

# Nomes encurtados e formatados para radar
nomes_radar_metricas = {
    "Golos sem ser por penálti/90": "Gols\n(sem pên.)",
    "Assistências/90": "Assistências",
    "Assistências esperadas/90": "Assist.\nEsperadas",
    "Passes progressivos fora da área/90": "Passes\nprog.",
    "Toques na área/90": "Toques \nna área",
    "Passes para a área de penálti/90": "Passes\np/ área",
    "Remates/90": "Volume\nde Finalizações",
    "Remates à baliza, %": "Acerto no \nchute (%)",
    "Passes/90": "Volume\nde Passes",
    "Passes certos, %": "Acerto\npasses (%)",
    "Cruzamentos/90": "Volume de\nCruzamentos",
    "Cruzamentos certos, %": "Acerto\ncruz. (%)",
    "Dribles certos/ 90": "Dribles\ncertos",
    "Faltas sofridas/90": "Faltas\nsofridas",
    "Duelos ofensivos/90": "Duelos\nof.",
    "Duelos ofensivos ganhos, %": "Eficiência\nduelos of. (%)",
    "Duelos defensivos/90": "Duelos\ndef.",
    "Duelos defensivos ganhos, %": "Eficiência\nduelos def. (%)",
    "Duelos/90": "Particip.\nem Duelos",
    "Duelos ganhos, %": "Eficiência\nem duelos (%)",
    "Ações Defensivas por 30' de Posse Adversária": "Ações def.",
    "Passes progressivos/90": "Passes prog.",
    "Passes progressivos certos, %": "Acerto\npasse prog. (%)",
    "Passes progressivos certos/90": "Passes\nprog. certos",
    "Corridas progressivas/90": "Conduções\nprog.",
    "Duelos Defensivos por 30' de Posse Adversária": "Duelos\ndef.",
    "Golos marcados, %": "Conversão\ngols (%)",
    "Dribles/90": "Dribles\ntentados",
    "Dribles com sucesso, %": "Eficiência\ndrible (%)",
    "Passes longos recebidos/90": "Passes\nLongos Rec.",
    "Duelos aérios/90": "Volume de\nDuelos Aéreos",
    "Duelos aéreos ganhos, %": "Vit.\nAéreos (%)",
    "Passes curtos / médios /90": "Passes\ncurtos/médios",
    "Passes curtos / médios precisos, %": "Ef.curtos\n/médios (%)",
    "Passes longos/90": "Passes\nlongos",
    "Passes longos certos, %": "Ef.\nlongos (%)",
    "Faltas/90": "Faltas"
}

# Contextos de interpretação para as métricas
contextos_gerais = {
    "Golos sem ser por penálti/90": {
        "positivo": "indicando alta capacidade goleadora.",
        "negativo": "sugerindo menor capacidade de contribuir com gols."
    },
    "Assistências/90": {
        "positivo": "sinalizando participação decisiva na criação de gols.",
        "negativo": "o que pode refletir menor efetividade no último passe."
    },
    "Assistências esperadas/90": {
        "positivo": "refletindo criação constante de oportunidades de alta qualidade.",
        "negativo": "sugerindo que suas ações ofensivas não geram muitas chances reais de gol."
    },
    "Passes progressivos fora da área/90": {
        "positivo": "contribuindo para o avanço territorial da equipe.",
        "negativo": "indicando pouca ação em passes que rompem linhas fora da zona de finalização."
    },
    "Toques na área/90": {
        "positivo": "indicando alta característica de pisar na área.",
        "negativo": "indicando pouca infiltração na área adversária."
    },
    "Passes para a área de penálti/90": {
        "positivo": "indicando capacidade de fazer passes para companheiros em áreas perigosas.",
        "negativo": "indicando menor presença em passes para companheiros em zonas perigosas."
    },
    "Remates/90": {
        "positivo": "demonstrando volume ofensivo e proatividade para finalizar.",
        "negativo": "com pouca iniciativa de finalização ao longo dos jogos."
    },
    "Remates à baliza, %": {
        "positivo": "indicando precisão nas finalizações executadas.",
        "negativo": "com baixa taxa de sucesso nos chutes tentados."
    },
    "Passes/90": {
        "positivo": "sendo peça chave na circulação da bola.",
        "negativo": "indicando baixa participação na posse."
    },
    "Passes certos, %": {
        "positivo": "mantendo alta confiabilidade na circulação de bola.",
        "negativo": "indicando perda de posse frequente em tentativas de passe."
    },
    "Cruzamentos/90": {
        "positivo": "construindo volume ofensivo a partir da faixa lateral.",
        "negativo": "com baixa frequência de bolas cruzadas à área adversária."
    },
    "Cruzamentos certos, %": {
        "positivo": "revelando boa pontaria em bolas cruzadas.",
        "negativo": "indicando baixa efetividade ao acionar companheiros na área em bolas cruzadas."
    },
    "Dribles certos/ 90": {
        "positivo": "sendo eficiente ao superar adversários no mano a mano.",
        "negativo": "com pouca produtividade em jogadas de desequilíbrio no mano a mano."
    },
    "Faltas sofridas/90": {
        "positivo": "mostrando protagonismo e incômodo à marcação adversária.",
        "negativo": "sugerindo que defensores não precisam pará-lo com faltas frequentemente."
    },
    "Duelos ofensivos/90": {
        "positivo": "indicando disposição constante nos enfrentamentos com adversários.",
        "negativo": "com pouca participação em confrontos ofensivos."
    },
    "Duelos ofensivos ganhos, %": {
        "positivo": "revelando superioridade técnica e física nos embates de ataque.",
        "negativo": "indicando menor sucesso em vencer disputas individuais no ataque."
    },
    "Duelos defensivos/90": {
        "positivo": "demonstrando esforço para recuperar a bola em disputas contra adversários.",
        "negativo": "com baixa contribuição na fase defensiva."
    },
    "Duelos defensivos ganhos, %": {
        "positivo": "com bom desempenho na contenção do oponente.",
        "negativo": "revelando dificuldade em vencer disputas defensivas."
    },
    "Duelos/90": {
        "positivo": "mostrando competitividade em diferentes tipos de embates no campo.",
        "negativo": "indicando menor intensidade nos confrontos individuais."
    },
    "Duelos ganhos, %": {
        "positivo": "revelando solidez e competência em diferentes tipos de disputa.",
        "negativo": "com dificuldade para se impor nos confrontos."
    },
    "Ações Defensivas por 30' de Posse Adversária": {
        "positivo": "demonstrando grande presença nas ações defensivas quando o adversário tem a bola.",
        "negativo": "sugerindo baixa contribuição para recuperar a bola em momentos defensivos."
    },
    "Passes progressivos/90": {
        "positivo": "mostrando boa iniciativa para avançar território com passes.",
        "negativo": "revelando pouca iniciativa para romper linhas com a bola."
    },
    "Passes progressivos certos, %": {
        "positivo": "indicando eficiência nas tentativas de passes verticais.",
        "negativo": "mostrando dificuldade em executar passes progressivos com qualidade."
    },
    "Passes progressivos certos/90": {
        "positivo": "mostrando boa capacidade de avanço territorial com passes.",
        "negativo": "revelando pouca iniciativa para romper linhas com a bola."
    },
    "Corridas progressivas/90": {
        "positivo": "revelando boa capacidade de conduzir a bola em direção ao gol adversário.",
        "negativo": "indicando pouca presença conduzindo a bola em progressão."
    },
    "Duelos Defensivos por 30' de Posse Adversária": {
        "positivo": "indicando participação frequente nos duelos enquanto defende.",
        "negativo": "revelando baixa presença em embates defensivos durante a posse adversária."
    },
    "Golos marcados, %": {
        "positivo": "indicando excelente aproveitamento das finalizações.",
        "negativo": "sugerindo baixa eficiência nas chances de gol que recebe."
    },
    "Dribles com sucesso, %": {
        "positivo": "demonstrando eficiência nos lances de um contra um.",
        "negativo": "indicando baixa eficiência em superar adversários com a bola."
    },
    "Passes longos recebidos/90": {
        "positivo": "mostrando ser um alvo constante em bolas longas.",
        "negativo": "com pouca participação sendo alvo de lançamentos longos."
    },
    "Duelos aérios/90": {
        "positivo": "indicando envolvimento constante em disputas pelo alto.",
        "negativo": "com baixa presença nas bolas aéreas."
    },
    "Duelos aéreos ganhos, %": {
        "positivo": "revelando domínio nos confrontos aéreos.",
        "negativo": "sugerindo fragilidade nas disputas aéreas."
    },
    "Dribles/90": {
        "positivo": "indicando alta proatividade na busca por enfrentamentos individuais.",
        "negativo": "sugerindo baixa proatividade na busca por dribles."
    },
    "Passes curtos / médios /90": {
        "positivo": "sendo peça chave na circulação de bola curta/média.",
        "negativo": "indicando baixa participação no jogo através de passes com menor distância."
    },
    "Passes curtos / médios precisos, %": {
        "positivo": "mantendo alta confiabilidade na manutenção da posse em trocas de passe próximas.",
        "negativo": "apresentando baixa confiabilidade em trocas de passe próximas."
    },
    "Passes longos/90": {
        "positivo": "possuindo característica de tentar bolas longas frequentemente.",
        "negativo": "com baixa procura por bolas longas ao longo da partida."
    },
    "Passes longos certos, %": {
        "positivo": "indicando alta eficiência em suas tentativas de bola longa.",
        "negativo": "indicando baixa eficiência em suas tentativas de bola longa."
    },
    "Faltas/90": {
        "positivo": "indicando que precisa recorrer a faltas para parar seus adversários frequentemente.",
        "negativo": "indicando que não é um jogador faltoso."
    }
}

pares_metricas_por_posicao = {
    "CB": [
        ("Passes/90", "Passes certos, %"),
        ("Passes curtos / médios /90", "Passes curtos / médios precisos, %"),
        ("Passes longos/90", "Passes longos certos, %"),
        ("Passes progressivos/90", "Passes progressivos certos, %"),
        ("Dribles certos/ 90", "Corridas progressivas/90"),
        ("Ações Defensivas por 30' de Posse Adversária", "Faltas/90"),
        ("Duelos Defensivos por 30' de Posse Adversária", "Duelos defensivos ganhos, %"),
        ("Duelos aérios/90", "Duelos aéreos ganhos, %"),
        ("Duelos/90", "Duelos ganhos, %")
    ],
    "RCB": [
        ("Passes/90", "Passes certos, %"),
        ("Passes curtos / médios /90", "Passes curtos / médios precisos, %"),
        ("Passes longos/90", "Passes longos certos, %"),
        ("Passes progressivos/90", "Passes progressivos certos, %"),
        ("Dribles certos/ 90", "Corridas progressivas/90"),
        ("Ações Defensivas por 30' de Posse Adversária", "Faltas/90"),
        ("Duelos Defensivos por 30' de Posse Adversária", "Duelos defensivos ganhos, %"),
        ("Duelos aérios/90", "Duelos aéreos ganhos, %"),
        ("Duelos/90", "Duelos ganhos, %")
    ],
    "LCB": [
        ("Passes/90", "Passes certos, %"),
        ("Passes curtos / médios /90", "Passes curtos / médios precisos, %"),
        ("Passes longos/90", "Passes longos certos, %"),
        ("Passes progressivos/90", "Passes progressivos certos, %"),
        ("Dribles certos/ 90", "Corridas progressivas/90"),
        ("Ações Defensivas por 30' de Posse Adversária", "Faltas/90"),
        ("Duelos Defensivos por 30' de Posse Adversária", "Duelos defensivos ganhos, %"),
        ("Duelos aérios/90", "Duelos aéreos ganhos, %"),
        ("Duelos/90", "Duelos ganhos, %")
    ],
    "LB": [
        ("Golos sem ser por penálti/90", "Assistências/90"),
        ("Passes progressivos certos/90", "Assistências esperadas/90"),
        ("Passes/90", "Passes certos, %"),
        ("Cruzamentos/90", "Cruzamentos certos, %"),
        ("Dribles certos/ 90", "Corridas progressivas/90"),
        ("Duelos ofensivos/90", "Duelos ofensivos ganhos, %"),
        ("Duelos Defensivos por 30' de Posse Adversária", "Duelos defensivos ganhos, %"),
        ("Ações Defensivas por 30' de Posse Adversária", "Faltas/90"),
        ("Duelos aérios/90", "Duelos aéreos ganhos, %"),
        ("Duelos/90", "Duelos ganhos, %")
    ],
    "RB": [
        ("Golos sem ser por penálti/90", "Assistências/90"),
        ("Passes progressivos certos/90", "Assistências esperadas/90"),
        ("Passes/90", "Passes certos, %"),
        ("Cruzamentos/90", "Cruzamentos certos, %"),
        ("Dribles certos/ 90", "Corridas progressivas/90"),
        ("Duelos ofensivos/90", "Duelos ofensivos ganhos, %"),
        ("Duelos Defensivos por 30' de Posse Adversária", "Duelos defensivos ganhos, %"),
        ("Ações Defensivas por 30' de Posse Adversária", "Faltas/90"),
        ("Duelos aérios/90", "Duelos aéreos ganhos, %"),
        ("Duelos/90", "Duelos ganhos, %")
    ],
    "DMF": [
        ("Passes/90", "Passes certos, %"),
        ("Assistências esperadas/90", "Toques na área/90"),
        ("Passes progressivos fora da área/90", "Passes progressivos certos, %"),
        ("Passes longos/90", "Passes longos certos, %"),
        ("Dribles/90", "Dribles com sucesso, %"),
        ("Corridas progressivas/90", "Faltas sofridas/90"),
        ("Ações Defensivas por 30' de Posse Adversária", "Faltas/90"),
        ("Duelos Defensivos por 30' de Posse Adversária", "Duelos defensivos ganhos, %"),
        ("Duelos aérios/90", "Duelos aéreos ganhos, %"),
        ("Duelos/90", "Duelos ganhos, %")
    ],
    "RDMF":[
        ("Passes/90", "Passes certos, %"),
        ("Assistências esperadas/90", "Toques na área/90"),
        ("Passes progressivos fora da área/90", "Passes progressivos certos, %"),
        ("Passes longos/90", "Passes longos certos, %"),
        ("Dribles/90", "Dribles com sucesso, %"),
        ("Corridas progressivas/90", "Faltas sofridas/90"),
        ("Ações Defensivas por 30' de Posse Adversária", "Faltas/90"),
        ("Duelos Defensivos por 30' de Posse Adversária", "Duelos defensivos ganhos, %"),
        ("Duelos aérios/90", "Duelos aéreos ganhos, %"),
        ("Duelos/90", "Duelos ganhos, %")
    ],
    "LDMF":[
        ("Passes/90", "Passes certos, %"),
        ("Assistências esperadas/90", "Toques na área/90"),
        ("Passes progressivos fora da área/90", "Passes progressivos certos, %"),
        ("Passes longos/90", "Passes longos certos, %"),
        ("Dribles/90", "Dribles com sucesso, %"),
        ("Corridas progressivas/90", "Faltas sofridas/90"),
        ("Ações Defensivas por 30' de Posse Adversária", "Faltas/90"),
        ("Duelos Defensivos por 30' de Posse Adversária", "Duelos defensivos ganhos, %"),
        ("Duelos aérios/90", "Duelos aéreos ganhos, %"),
        ("Duelos/90", "Duelos ganhos, %")
    ],
    "RCMF": [
        ("Passes/90", "Passes certos, %"),
        ("Assistências esperadas/90", "Toques na área/90"),
        ("Passes progressivos fora da área/90", "Passes progressivos certos, %"),
        ("Dribles/90", "Dribles com sucesso, %"),
        ("Corridas progressivas/90", "Faltas sofridas/90"),
        ("Ações Defensivas por 30' de Posse Adversária", "Faltas/90"),
        ("Duelos Defensivos por 30' de Posse Adversária", "Duelos defensivos ganhos, %"),
        ("Duelos aérios/90", "Duelos aéreos ganhos, %"),
        ("Duelos/90", "Duelos ganhos, %")
    ],
    "LCMF": [
        ("Passes/90", "Passes certos, %"),
        ("Assistências esperadas/90", "Toques na área/90"),
        ("Passes progressivos fora da área/90", "Passes progressivos certos, %"),
        ("Dribles/90", "Dribles com sucesso, %"),
        ("Corridas progressivas/90", "Faltas sofridas/90"),
        ("Ações Defensivas por 30' de Posse Adversária", "Faltas/90"),
        ("Duelos Defensivos por 30' de Posse Adversária", "Duelos defensivos ganhos, %"),
        ("Duelos aérios/90", "Duelos aéreos ganhos, %"),
        ("Duelos/90", "Duelos ganhos, %")
    ],
    "AMF": [
        ("Golos sem ser por penálti/90", "Assistências/90"),
        ("Passes progressivos fora da área/90", "Assistências esperadas/90"),
        ("Passes para a área de penálti/90", "Toques na área/90"),
        ("Remates/90", "Remates à baliza, %"),
        ("Passes/90", "Passes certos, %"),
        ("Cruzamentos/90", "Cruzamentos certos, %"),
        ("Faltas sofridas/90", "Dribles certos/ 90", ),
        ("Duelos ofensivos/90", "Duelos ofensivos ganhos, %"),
        ("Duelos Defensivos por 30' de Posse Adversária", "Duelos defensivos ganhos, %"),
        ("Duelos/90", "Duelos ganhos, %")
    ],
     "RW": [
        ("Golos sem ser por penálti/90", "Assistências/90"),
        ("Passes progressivos fora da área/90", "Assistências esperadas/90"),
        ("Passes para a área de penálti/90", "Toques na área/90"),
        ("Remates/90", "Remates à baliza, %"),
        ("Dribles/90", "Dribles com sucesso, %"),
        ("Cruzamentos/90", "Cruzamentos certos, %"),
        ("Faltas sofridas/90", "Corridas progressivas/90", ),
        ("Duelos ofensivos/90", "Duelos ofensivos ganhos, %"),
        ("Duelos defensivos/90", "Duelos defensivos ganhos, %"),
        ("Duelos/90", "Duelos ganhos, %")
    ],
    "LW": [
        ("Golos sem ser por penálti/90", "Assistências/90"),
        ("Passes progressivos fora da área/90", "Assistências esperadas/90"),
        ("Passes para a área de penálti/90", "Toques na área/90"),
        ("Remates/90", "Remates à baliza, %"),
        ("Dribles/90", "Dribles com sucesso, %"),
        ("Cruzamentos/90", "Cruzamentos certos, %"),
        ("Faltas sofridas/90", "Corridas progressivas/90", ),
        ("Duelos ofensivos/90", "Duelos ofensivos ganhos, %"),
        ("Duelos Defensivos por 30' de Posse Adversária", "Duelos defensivos ganhos, %"),
        ("Duelos/90", "Duelos ganhos, %")
    ],
    "CF": [
        ("Golos sem ser por penálti/90", "Assistências/90"),
        ("Remates/90", "Golos marcados, %"),
        ("Passes progressivos certos/90", "Assistências esperadas/90"),
        ("Passes/90", "Passes certos, %"),
        ("Dribles/90", "Dribles com sucesso, %"),
        ("Passes longos recebidos/90", "Toques na área/90"),
        ("Ações Defensivas por 30' de Posse Adversária", "Faltas sofridas/90"),
        ("Duelos aérios/90", "Duelos aéreos ganhos, %"),
        ("Duelos Defensivos por 30' de Posse Adversária", "Duelos defensivos ganhos, %"),
        ("Duelos ofensivos/90", "Duelos ofensivos ganhos, %")
    ]
}

# Equivalência entre posições para comparação
posicoes_equivalentes = {
    "RB": ["RB"],
    "LB": ["LB"],
    "RW": ["RW", "LW"],
    "LW": ["LW", "RW"],
    "CB": ["CB", "RCB", "LCB"],
    "RCB": ["CB", "RCB", "LCB"],
    "LCB": ["CB", "RCB", "LCB"],
    "DMF": ["DMF", "RDMF", "LDMF"],
    "RDMF": ["DMF", "RDMF", "LDMF"],
    "LDMF": ["DMF", "RDMF", "LDMF"],
    "RCMF": ["RCMF", "LCMF"],
    "LCMF": ["RCMF", "LCMF"]
}


posicoes_formatadas = {
    "CF": "Atacante",
    "RW": "Extremo",
    "LW": "Extremo",
    "AMF": "Meia-atacante",
    "DMF": "Médio Defensivo",
    "RDMF": "Médio Defensivo",
    "LDMF": "Médio Defensivo",
    "CMF": "Médio",
    "RCMF": "Médio",
    "LCMF": "Médio",
    "RB": "Lateral-direito",
    "LB": "Lateral-esquerdo",
    "CB": "Zagueiro",
    "RCB": "Zagueiro",
    "LCB": "Zagueiro"
}

liga_forca = {
    'Inglaterra 24-25': 100.0,
    'Espanha 24-25': 94.0,
    'Itália 24-25': 94.0,
    'Alemanha 24-25': 93.2,
    'França 24-25': 92.3,
    'Bélgica 24-25': 86.9,
    'Portugal 24-25': 86.2,
    'Brasil 2024': 85.7,
    'Brasil 2025': 85.7,
    'Holanda 24-25': 85.1,
    'Argentina 2025': 84.9,
    'EUA 25': 84.8,
    'México 24-25': 84.8,
    'Japão 2025': 84.1,
    'Croácia 24-25': 84.0,
    'Polônia 2025': 8
}

