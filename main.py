# main.py

from dados.carregar_dados import carregar_e_tratar_dados
from utilitarios.interpretacoes import interpretar, gerar_paragrafo_com_grafico
from utilitarios.constantes import pares_metricas_por_posicao, posicoes_equivalentes
from utilitarios.funcoes_pdf import gerar_pdf_jogador
from utilitarios.constantes import metricas_traduzidas
import pandas as pd
from dados.carregar_dados import normalizar_posicoes
from utilitarios.funcoes_metricas import adicionar_metricas_derivadas
from utilitarios.funcoes_grafico import gerar_grafico_radar
import tempfile
import os
import streamlit as st

def gerar_relatorio_dados(
    df, jogador, equipa, posicao=None,
    liga=None,
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
    col_equipe = "Equipe na liga analisada" if "Equipe na liga analisada" in df.columns else "Equipa"
    df = normalizar_posicoes(df)

    # Limpar a coluna de posição: manter apenas a primeira, se houver múltiplas
    df[coluna_posicao] = df[coluna_posicao].astype(str).apply(lambda x: x.split(",")[0].strip())

    # Detectar posição automaticamente se não for passada
    if posicao is None:
        try:
            linha = df[(df["Jogador"] == jogador) & (df[col_equipe] == equipa)].iloc[0]
            posicao = linha["Posição"] if "Posição" in linha else linha.get("Pos.")
            posicao = str(posicao).split(",")[0].strip()
        except IndexError:
            print(f"[ERRO] Não foi possível identificar a posição do jogador '{jogador}' da equipe '{equipa}'.")
            return None

    # ✅ Carregar DataFrame da Liga BRA 2025.xlsx para os gráficos comparativos
    caminho_df_liga = os.path.join("dataframes", "Brasil 2024.xlsx")
    df_liga = pd.read_excel(caminho_df_liga)

    df_liga = normalizar_posicoes(df_liga)
    df_vasco = df_liga[df_liga['Equipa'].str.contains("Vasco", case=False, na=False)].copy()
    df_liga[coluna_posicao] = df_liga[coluna_posicao].astype(str).apply(lambda x: x.split(",")[0].strip())
    df_liga = adicionar_metricas_derivadas(df_liga)

    from utilitarios.funcoes_grafico import obter_grupo_posicao
    grupo_posicao = obter_grupo_posicao(df_liga, posicao)

    # garante q jogadores do Vasco tb estão no grupo
    vasco_mesma_posicao = obter_grupo_posicao(df_vasco, posicao)
    grupo_posicao = pd.concat([grupo_posicao, vasco_mesma_posicao], ignore_index=True).drop_duplicates(subset=["Jogador", "Equipa"])

    if df_auxiliar is not None:
        df_auxiliar = adicionar_metricas_derivadas(df_auxiliar)
        if 'Posição' in df_auxiliar.columns:
            grupo_aux = df_auxiliar[df_auxiliar['Posição'] == posicao]
        elif 'Pos.' in df_auxiliar.columns:
            grupo_aux = df_auxiliar[df_auxiliar['Pos.'] == posicao]
        else:
            grupo_aux = pd.DataFrame()
        grupo_posicao = pd.concat([grupo_posicao, grupo_aux], ignore_index=True)

    # Buscar a liga no DataFrame, se ela ainda não foi passada
    if liga is None:
        if "Liga" in df.columns:
            liga_series = df[(df["Jogador"] == jogador) & (df[col_equipe] == equipa)]["Liga"]
            liga = liga_series.iloc[0] if not liga_series.empty else "Liga não especificada"
        else:
            liga = "Liga não especificada"

    # Garantir que a coluna "Liga" esteja presente no grupo_posicao
    if "Liga" not in grupo_posicao.columns and "Liga" in df.columns:
        grupo_posicao = pd.merge(
            grupo_posicao,
            df[["Jogador", "Equipa", "Liga"]],
            on=["Jogador", "Equipa"],
            how="left"
        )

    # Buscar o jogador no df original, e não no grupo de comparação
    jogador_df = df[
        (df["Jogador"] == jogador) &
        (df[col_equipe] == equipa)
    ]
    
    # Apenas checar se bate com a liga selecionada (opcional)
    if "Liga" in df.columns and liga:
        jogador_df = jogador_df[jogador_df["Liga"] == liga]

    # Verifica se encontrou os dados do jogador
    if jogador_df.empty:
        st.error(f"❌ Nenhum dado encontrado para **{jogador}** ({equipa}) na liga: {liga}")
        st.info("🔍 Dados disponíveis no grupo filtrado (debug):")
        st.dataframe(grupo_posicao[(grupo_posicao["Jogador"] == jogador)])
        return None
    
    jogador_dados = jogador_df.iloc[0]

    # DEBUG: verificar por que jogador_df está vazio
    print("🔎 DEBUG - Checando filtros para encontrar o jogador no grupo_posicao")
    print("Jogador:", jogador)
    print("Equipa:", equipa)
    print("Liga:", liga)
    print("grupo_posicao.columns:", grupo_posicao.columns.tolist())
    print("Entradas encontradas para jogador e equipa:")
    print(grupo_posicao[(grupo_posicao["Jogador"] == jogador) & (grupo_posicao["Equipa"] == equipa)])
    print("Entradas com jogador + equipa + liga:")
    print(grupo_posicao[
        (grupo_posicao["Jogador"] == jogador) &
        (grupo_posicao["Equipa"] == equipa) &
        (grupo_posicao["Liga"] == liga)
    ])

    jogador_dados = jogador_df.iloc[0]

    radar_temp = tempfile.mktemp(suffix=".png")

    vasco_posicao = df_vasco[df_vasco['Posição'] == posicao]
    jogador_comparado = None
    if not vasco_posicao.empty:
        jogador_comparado = vasco_posicao.sort_values(by="Minutos jogados:", ascending=False).iloc[0]["Jogador"]

    gerar_grafico_radar(
        jogador_df=jogador_df,
        grupo_posicao=grupo_posicao,
        posicao=posicao,
        jogador=jogador,
        nome_arquivo_radar=radar_temp,
        jogador_comparado=jogador_comparado
    )

    radar_path = radar_temp

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

    if exportar_pdf:
        caminho_saida = os.path.join(os.getcwd(), f"{jogador.replace(' ', '_')}_relatorio.pdf")
        gerar_pdf_jogador(
            jogador=jogador,
            posicao=posicao,
            equipa=equipa,
            liga=liga,
            textos=textos,
            imagens=imagens,
            texto_conclusao=texto_conclusao,
            resumo_desempenho=resumo_desempenho,
            comparacao_contextual_bs=comparacao_contextual_bs,
            comparacao_vasco_bs=comparacao_vasco_bs,
            caminho_saida=caminho_saida,
            descricao_inicial=descricao_inicial,
            radar_path_final = radar_path
        )
        print(f"Relatório salvo em: {caminho_saida}")
        return caminho_saida
