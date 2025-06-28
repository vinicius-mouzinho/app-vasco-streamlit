import streamlit as st
import os
from dados.carregar_df_streamlit import carregar_df
import pandas as pd
from seguranca.autenticacao import criar_autenticador
from dados.unificar_dataframes import unificar_dataframes
from utilitarios.filtros import aplicar_filtros_basicos
from utilitarios.interface_ranking import exibir_ranking_por_perfil

st.set_page_config(page_title="Scout Vasco - App de Análise de Dados", layout="wide")

# Autenticação
autenticador = criar_autenticador()
nome, autenticado, usuario = autenticador.login('Login', 'main')

if autenticado:
    autenticador.logout('Sair', 'sidebar')
    st.sidebar.success(f'Bem-vindo, {nome}!')
    st.title("📊 Scout Vasco - App de Análise de Dados")

    # Caminho fixo para a pasta com os DataFrames
    PASTA_DATAFRAMES = "dataframes"
    arquivos_disponiveis = sorted(
    [arq for arq in os.listdir(PASTA_DATAFRAMES) if arq.endswith(('.xlsx', '.csv', '.pkl'))]
)

    arquivos_disponiveis = sorted(
    [arq for arq in os.listdir(PASTA_DATAFRAMES) if arq.endswith(('.xlsx', '.csv', '.pkl'))]
    )

    arquivo_selecionado = st.selectbox("Selecione um DataFrame:", arquivos_disponiveis)

    df = carregar_df(arquivo_selecionado)
    st.success(f"✅ Arquivo carregado: {arquivo_selecionado}")


    if arquivo_selecionado:
        df, filtros_aplicados = aplicar_filtros_basicos(df)
    
        st.markdown("---")
        st.subheader("📋 Dados filtrados")
        st.dataframe(df, use_container_width=True)

        st.markdown("---")
        st.header("📄 Gerar Relatório Individual")

        jogadores = sorted(df['Jogador'].dropna().unique())
        jogador_selecionado = st.selectbox("Escolha o jogador para gerar o relatório:", jogadores)

        coluna_posicao = 'Pos.' if 'Pos.' in df.columns else 'Posição'
        posicoes = sorted(df[coluna_posicao].dropna().unique())
        posicao_selecionada = st.selectbox("Selecione a posição do jogador:", posicoes)

        if st.button("Gerar Relatório PDF"):
            from main import gerar_relatorio_dados

            # Obter equipe
            equipa = df[df['Jogador'] == jogador_selecionado]['Equipa'].values[0]

            # Criar DataFrame auxiliar com posição ajustada
            df_auxiliar = df[df['Jogador'] == jogador_selecionado].copy()
            df_auxiliar[coluna_posicao] = posicao_selecionada

            # Gerar relatório
            caminho_pdf = gerar_relatorio_dados(
                df=df,
                jogador=jogador_selecionado,
                equipa=equipa,
                posicao=posicao_selecionada,
                df_auxiliar=df_auxiliar,
                texto_conclusao=None,
                resumo_desempenho=None,
                exportar_pdf=True,
                nome_arquivo_df=arquivo_selecionado
            )

            if caminho_pdf and os.path.exists(caminho_pdf):
                st.success(f"✅ Relatório de {jogador_selecionado} gerado com sucesso!")
                with open(caminho_pdf, "rb") as f:
                    st.download_button(
                        label="📥 Baixar PDF do Relatório",
                        data=f,
                        file_name=os.path.basename(caminho_pdf),
                        mime="application/pdf"
                    )
            else:
                st.error("❌ O relatório não pôde ser gerado. Verifique os dados disponíveis.")

        exibir_ranking_por_perfil(df)