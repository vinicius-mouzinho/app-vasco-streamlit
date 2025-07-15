import streamlit as st
import os
from dados.carregar_df_streamlit import carregar_df
from main import gerar_relatorio_dados
from dados.carregar_dados import normalizar_posicoes

def exibir_pagina_relatorio_individual():
    st.header("📄 Relatório Individual de Jogador")
    
    # Carregar e normalizar o DataFrame
    df = carregar_df(st.session_state.arquivo_atual)
    if df is None or df.empty:
        st.warning("Nenhum DataFrame carregado.")
        return
    df = normalizar_posicoes(df)  # ✅ garante que LWF → LW, etc.

    # Verificar colunas essenciais
    if not all(col in df.columns for col in ["Jogador", "Equipa", "Liga"]):
        st.error("O DataFrame deve conter as colunas 'Jogador', 'Equipa' e 'Liga'.")
        return

    # 1. Selecionar a liga
    ligas = sorted(df['Liga'].dropna().unique())
    liga = st.selectbox("Selecione a liga:", ligas, key="select_liga")

    # 2. Selecionar a equipe com base na liga
    df_liga = df[df['Liga'] == liga].copy()
    col_equipe_liga = 'Equipa na liga analisada'
    if col_equipe_liga not in df_liga.columns:
        st.error("A coluna 'Equipa na liga analisada' está ausente no DataFrame. Ela é essencial para filtrar corretamente os clubes da liga.")
        return

    equipas = sorted(df_liga[col_equipe_liga].dropna().unique())
    equipa = st.selectbox("Escolha a equipa:", equipas, key="select_equipa")

    # 3. Selecionar o jogador com base na equipe e liga
    df_equipa = df_liga[df_liga[col_equipe_liga] == equipa].copy()
    df_equipa = normalizar_posicoes(df_equipa)  # ✅ reforça normalização após filtro
    jogadores = sorted(df_equipa['Jogador'].dropna().unique())
    jogador = st.selectbox("Selecione o jogador:", jogadores, key="select_jogador")

    # 4. Detectar posição automaticamente
    pos_col = 'Posição' if 'Posição' in df.columns else 'Pos.'
    jogador_df = df_equipa[df_equipa['Jogador'] == jogador]

    if jogador_df.empty:
        st.error("Não foi possível encontrar os dados completos do jogador selecionado.")
        return

    posicao_detectada = jogador_df[pos_col].values[0]
    st.markdown(f"🧭 **Posição detectada:** `{posicao_detectada}`")

    # 5. Permitir ajuste manual da posição
    todas_posicoes = sorted(df_liga[pos_col].dropna().unique())
    posicao_escolhida = st.selectbox(
        "Selecionar posição para análise:",
        todas_posicoes,
        index=todas_posicoes.index(posicao_detectada) if posicao_detectada in todas_posicoes else 0,
        key="select_posicao"
    )

    # 6. Botão para gerar o relatório
    if st.button("Gerar Relatório PDF"):
        with st.spinner("Gerando relatório..."):
            caminho_pdf = gerar_relatorio_dados(
                df=df,
                jogador=jogador,
                equipa=equipa,
                posicao=posicao_escolhida,
                nome_arquivo_df=st.session_state.arquivo_atual,
                exportar_pdf=True,
                liga=liga
            )
        if caminho_pdf:
            st.success("Relatório gerado com sucesso!")
            with open(caminho_pdf, "rb") as f:
                st.download_button(
                    label="📥 Baixar Relatório PDF",
                    data=f,
                    file_name=os.path.basename(caminho_pdf),
                    mime="application/pdf"
                )
