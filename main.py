# main.py

from dados.carregar_dados import carregar_e_tratar_dados
from utilitarios.interpretacoes import interpretar, gerar_paragrafo_com_grafico
from utilitarios.constantes import pares_metricas_por_posicao, posicoes_equivalentes
from utilitarios.funcoes_pdf import gerar_pdf_jogador
from utilitarios.constantes import metricas_traduzidas
import pandas as pd

import os

def gerar_relatorio_dados(
    df, jogador, equipa, posicao,
    nome_arquivo_df=None,
    df_auxiliar=None,
    img_perfil_analitico=None,
    comparacao_contextual_bs=None,
    comparacao_vasco_bs=None,
    comparar_individualmente_vasco=False,
    texto_conclusao=None,
    resumo_desempenho=None,
    exportar_pdf=True,
    modo_liga=False
):
    from matplotlib import pyplot as plt

    textos = []
    imagens = []

    coluna_posicao = 'Pos.' if 'Pos.' in df.columns else 'Posição'
    # Limpar a coluna de posição: manter apenas a primeira, se houver múltiplas
    df[coluna_posicao] = df[coluna_posicao].astype(str).apply(lambda x: x.split(",")[0].strip())
    # ✅ Carregar DataFrame da Liga BRA 2025.xlsx para os gráficos comparativos
    caminho_df_liga = os.path.join("dataframes", "Liga BRA 2024.xlsx")
    df_liga = pd.read_excel(caminho_df_liga)
    df_liga[coluna_posicao] = df_liga[coluna_posicao].astype(str).apply(lambda x: x.split(",")[0].strip())
    # === Adicionar métricas derivadas ao df_liga ===
    df_liga['Ações com a bola'] = df_liga['Passes/90'] + df_liga['Cruzamentos/90'] + df_liga['Dribles/90'] + df_liga['Remates/90']
    df_liga['Possession Adjustment'] = df_liga['Interceções ajust. à posse'] / df_liga['Interseções/90']
    df_liga['Ações Defensivas por 30\' de Posse Adversária'] = df_liga['Ações defensivas com êxito/90'] * df_liga['Possession Adjustment']
    df_liga['Dribles certos/ 90'] = df_liga['Dribles/90'] * df_liga['Dribles com sucesso, %'] / 100
    df_liga['Duelos Defensivos por 30\' de Posse Adversária'] = df_liga['Duelos defensivos/90'] * df_liga['Possession Adjustment']
    df_liga['Passes precisos para a área de penalti/90'] = df_liga['Passes para a área de penálti/90'] * df_liga['Passes precisos para a área de penálti, %'] / 100
    df_liga['Passes progressivos certos/90'] = df_liga['Passes progressivos/90'] * df_liga['Passes progressivos certos, %'] / 100
    df_liga['Passes progressivos fora da área/90'] = df_liga['Passes progressivos certos/90'] - df_liga['Passes precisos para a área de penalti/90']
    df_liga['Remates à baliza/90'] = df_liga['Remates/90'] * df_liga['Remates à baliza, %'] / 100
    df_liga['Perdas de bola'] = (
        (df_liga['Passes/90'] * (100 - df_liga['Passes certos, %']) / 100) +
        (df_liga['Dribles/90'] * (100 - df_liga['Dribles com sucesso, %']) / 100) +
        (df_liga['Remates/90'] * (100 - df_liga['Remates à baliza, %']) / 100) +
        (df_liga['Cruzamentos/90'] * (100 - df_liga['Cruzamentos certos, %']) / 100)
    )
    df_liga['Frequência no drible (%)'] = 100 * df_liga['Dribles/90'] / df_liga['Ações com a bola']
    grupo_posicao = df_liga[df_liga[coluna_posicao] == posicao]
    
    if df_auxiliar is not None:
        if 'Posição' in df_auxiliar.columns:
            grupo_aux = df_auxiliar[df_auxiliar['Posição'] == posicao]
        elif 'Pos.' in df_auxiliar.columns:
            grupo_aux = df_auxiliar[df_auxiliar['Pos.'] == posicao]
        else:
            grupo_aux = pd.DataFrame()  # vazio se não encontrar coluna válida
    
        grupo_posicao = pd.concat([grupo_posicao, grupo_aux])

    if df_auxiliar is not None:
        # === Adicionar métricas derivadas ao df_auxiliar ===
        df_auxiliar['Ações com a bola'] = df_auxiliar['Passes/90'] + df_auxiliar['Cruzamentos/90'] + df_auxiliar['Dribles/90'] + df_auxiliar['Remates/90']
        df_auxiliar['Possession Adjustment'] = df_auxiliar['Interceções ajust. à posse'] / df_auxiliar['Interseções/90']
        df_auxiliar['Ações Defensivas por 30\' de Posse Adversária'] = df_auxiliar['Ações defensivas com êxito/90'] * df_auxiliar['Possession Adjustment']
        df_auxiliar['Dribles certos/ 90'] = df_auxiliar['Dribles/90'] * df_auxiliar['Dribles com sucesso, %'] / 100
        df_auxiliar['Duelos Defensivos por 30\' de Posse Adversária'] = df_auxiliar['Duelos defensivos/90'] * df_auxiliar['Possession Adjustment']
        df_auxiliar['Passes precisos para a área de penalti/90'] = df_auxiliar['Passes para a área de penálti/90'] * df_auxiliar['Passes precisos para a área de penálti, %'] / 100
        df_auxiliar['Passes progressivos certos/90'] = df_auxiliar['Passes progressivos/90'] * df_auxiliar['Passes progressivos certos, %'] / 100
        df_auxiliar['Passes progressivos fora da área/90'] = df_auxiliar['Passes progressivos certos/90'] - df_auxiliar['Passes precisos para a área de penalti/90']
        df_auxiliar['Remates à baliza/90'] = df_auxiliar['Remates/90'] * df_auxiliar['Remates à baliza, %'] / 100
        df_auxiliar['Perdas de bola'] = (
            (df_auxiliar['Passes/90'] * (100 - df_auxiliar['Passes certos, %']) / 100) +
            (df_auxiliar['Dribles/90'] * (100 - df_auxiliar['Dribles com sucesso, %']) / 100) +
            (df_auxiliar['Remates/90'] * (100 - df_auxiliar['Remates à baliza, %']) / 100) +
            (df_auxiliar['Cruzamentos/90'] * (100 - df_auxiliar['Cruzamentos certos, %']) / 100)
        )
        df_auxiliar['Frequência no drible (%)'] = 100 * df_auxiliar['Dribles/90'] / df_auxiliar['Ações com a bola']
        grupo_posicao = pd.concat([grupo_posicao, df_auxiliar[df_auxiliar['Posição'] == posicao]])

    jogador_df = grupo_posicao[grupo_posicao["Jogador"] == jogador]
    
    jogador_dados = jogador_df.iloc[0]
    if nome_arquivo_df:
        partes = nome_arquivo_df.replace(".xlsx", "").replace(".csv", "").replace(".pkl", "").split()
        liga = " ".join(partes[:2])  # Exemplo: 'Liga ARG'
    else:
        liga = liga  # mantém o que foi passado
    
    desc_texto = f"{jogador} é um jogador do {equipa} atuando pela {liga}. "
    minutos = int(jogador_dados.get("Minutos jogados:", 0))
    minutagem_em_partidas = round(minutos / 90, 1)
    gols = int(jogador_dados.get("Golos", 0))
    assist = int(jogador_dados.get("Assistências", 0))
    idade = int(jogador_dados.get("Idade", 0))
    altura = int(jogador_dados.get("Altura", 0))
    naturalidade = jogador_dados.get("Naturalidade", "informação não disponível")
    pe = jogador_dados.get("Pé", "não informado").lower()
    contrato = jogador_dados.get("Contrato termina")
    contrato = contrato if pd.notna(contrato) else "não informado"
    valor_bruto = jogador_dados.get("Valor de mercado", 0)
    
    try:
        valor_milhoes = float(valor_bruto) / 1_000_000
        valor_formatado = f"€{valor_milhoes:.1f}M"
    except:
        valor_formatado = "não informado"
    
    desc_texto += f"Dentro dessa temporada, possui {minutos} minutos jogados ({minutagem_em_partidas} jogos), participando de {gols} gols e {assist} assistências. "
    desc_texto += f"Tem {idade} anos, {altura}cm de altura, nasceu no(a) {naturalidade} e seu pé dominante é o {pe}. "
    desc_texto += f"Seu contrato se encerra em {contrato}, e o atleta tem valor de mercado de {valor_formatado}, segundo a Transfermarkt."
    
    descricao_inicial = desc_texto

    if jogador_df.empty:
        print(f"Jogador {jogador} não encontrado na posição {posicao}.")
        return None

    pontos_fortes = []
    pontos_fracos = []

    pares_metricas = pares_metricas_por_posicao.get(posicao, [])
    for m1, m2 in pares_metricas:
        if m1 in jogador_df.columns and m2 in jogador_df.columns:
            texto_1 = interpretar(jogador, m1, jogador_df[m1].values[0], grupo_posicao[m1], pontos_fortes, pontos_fracos, segunda=False)
            texto_2 = interpretar(jogador, m2, jogador_df[m2].values[0], grupo_posicao[m2], pontos_fortes, pontos_fracos, segunda=True)
            gerar_paragrafo_com_grafico(m1, m2, texto_1, texto_2, grupo_posicao, jogador, equipa, imagens, textos, exportar_pdf)

    if resumo_desempenho is None:
        resumo_desempenho = {
            "pontos_fortes": [metricas_traduzidas.get(m, m) for m in pontos_fortes],
            "pontos_fracos": [metricas_traduzidas.get(m, m) for m in pontos_fracos]
        }

    radar_path = None  # Aqui você pode inserir o caminho do radar gerado, se quiser

    if exportar_pdf:
        caminho_saida = os.path.join(os.getcwd(), f"{jogador.replace(' ', '_')}_relatorio.pdf")
        gerar_pdf_jogador(
            jogador=jogador,
            posicao=posicao,
            equipa=equipa,
            liga=liga,
            textos=textos,
            imagens=imagens,
            radar_path=radar_path,
            texto_conclusao=texto_conclusao,
            resumo_desempenho=resumo_desempenho,
            comparacao_contextual_bs=comparacao_contextual_bs,
            comparacao_vasco_bs=comparacao_vasco_bs,
            caminho_saida=caminho_saida,
            descricao_inicial=descricao_inicial
        )
        print(f"Relatório salvo em: {caminho_saida}")
        return caminho_saida 
