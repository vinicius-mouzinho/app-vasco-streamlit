import streamlit as st
import os
import tempfile
from dados.carregar_df_streamlit import carregar_df
from main import gerar_relatorio_dados
from dados.carregar_dados import normalizar_posicoes

def exibir_pagina_relatorio_individual():
    st.header("📄 Relatório Individual de Jogador")
    
    df = carregar_df(st.session_state.arquivo_atual)
    if df is None or df.empty:
        st.warning("Nenhum DataFrame carregado.")
        return

    df = normalizar_posicoes(df)

    if not all(col in df.columns for col in ["Jogador", "Equipa", "Liga"]):
        st.error("O DataFrame deve conter as colunas 'Jogador', 'Equipa' e 'Liga'.")
        return

    # Filtros locais
    ligas = sorted(df['Liga'].dropna().unique())
    liga = st.selectbox("Selecione a liga:", ligas, key="select_liga")

    df_liga = df[df['Liga'] == liga].copy()
    col_equipe_liga = 'Equipa na liga analisada'
    if col_equipe_liga not in df_liga.columns:
        st.error("A coluna 'Equipa na liga analisada' está ausente no DataFrame.")
        return

    equipas = sorted(df_liga[col_equipe_liga].dropna().unique())
    equipa = st.selectbox("Escolha a equipa:", equipas, key="select_equipa")

    df_equipa = df_liga[df_liga[col_equipe_liga] == equipa].copy()
    df_equipa = normalizar_posicoes(df_equipa)

    jogadores = sorted(df_equipa['Jogador'].dropna().unique())
    jogador = st.selectbox("Escolha o jogador:", jogadores, key="select_jogador")

    # Permitir seleção manual da posição
    posicoes_disponiveis = sorted(df['Posição'].dropna().unique())
    posicao = st.selectbox("Selecione a posição para o relatório:", posicoes_disponiveis, key="select_posicao")

    # Upload de imagens opcionais
    st.markdown("### 🖼️ Imagens opcionais para o relatório")
    img_perfil_analitico = st.file_uploader("📌 Perfil Analítico (opcional)", type=["png", "jpg"])
    comparacao_contextual_bs = st.file_uploader("📊 Comparação Contextual (opcional)", type=["png", "jpg"])
    comparacao_vasco_bs = st.file_uploader("⚔️ Comparação VS Vasco (opcional)", type=["png", "jpg"])

    # Função auxiliar para salvar imagem temporária
    def salvar_imagem_temp(imagem):
        if imagem is not None:
            suffix = os.path.splitext(imagem.name)[-1]
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
            temp_file.write(imagem.read())
            temp_file.close()
            return temp_file.name
        return None

    img_perfil_path = salvar_imagem_temp(img_perfil_analitico)
    contextual_path = salvar_imagem_temp(comparacao_contextual_bs)
    vasco_path = salvar_imagem_temp(comparacao_vasco_bs)

    if st.button("📄 Gerar Relatório PDF"):
        with st.spinner("Gerando relatório..."):
            caminho_pdf = gerar_relatorio_dados(
                df=df,
                jogador=jogador,
                posicao=posicao,
                equipa=equipa,
                liga=liga,
                img_perfil_analitico=img_perfil_path,
                comparacao_contextual_bs=contextual_path,
                comparacao_vasco_bs=vasco_path,
                exportar_pdf=True
            )
            st.success("✅ Relatório gerado com sucesso!")
            with open(caminho_pdf, "rb") as file:
                st.download_button(
                    label="📥 Baixar PDF",
                    data=file,
                    file_name=os.path.basename(caminho_pdf),
                    mime="application/pdf"
                )
