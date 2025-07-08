import streamlit as st
import os
import pandas as pd
from dados.carregar_df_streamlit import carregar_df
from seguranca.autenticacao import criar_autenticador
from dados.unificar_dataframes import unificar_dataframes
from utilitarios.filtros import aplicar_filtros_basicos
from utilitarios.interface_ranking import exibir_ranking_por_perfil
from utilitarios.estruturas_tabela import selecionar_colunas
from paginas.comparador import exibir_comparador

st.set_page_config(page_title="Scout Vasco - App de Análise de Dados", layout="wide")

# Autenticação
autenticador = criar_autenticador()
nome, autenticado, usuario = autenticador.login('Login', 'main')

if autenticado:
    autenticador.logout('Sair', 'sidebar')
    st.sidebar.success(f'Bem-vindo, {nome}!')
    st.title("📊 Scout Vasco - App de Análise de Dados")

    # Menu de abas
    aba_selecionada = st.sidebar.radio(
        "Escolha uma seção:",
        (
            "Filtros e Tabelas",
            "Relatório Individual",
            "Ranking por Perfil",
            "Comparador entre jogadores",
            "Gráfico de Dispersão"
        )
    )

    # Arquivos disponíveis
    PASTA_DATAFRAMES = "dataframes"
    arquivos_disponiveis = sorted([
        arq for arq in os.listdir(PASTA_DATAFRAMES)
        if arq.endswith(('.xlsx', '.csv', '.pkl'))
    ])

    # Sessão para manter arquivo selecionado
    if "arquivo_atual" not in st.session_state:
        st.session_state.arquivo_atual = arquivos_disponiveis[0]

    arquivo_selecionado = st.selectbox(
        "Selecione um DataFrame:",
        arquivos_disponiveis,
        index=arquivos_disponiveis.index(st.session_state.arquivo_atual)
    )

    # Recarrega DataFrame só se mudar o arquivo
    if arquivo_selecionado != st.session_state.arquivo_atual:
        st.session_state.arquivo_atual = arquivo_selecionado
        st.cache_data.clear()

    df = carregar_df(st.session_state.arquivo_atual)
    df_filtrado, filtros_aplicados = aplicar_filtros_basicos(df)

    st.success(f"✅ Arquivo carregado: {st.session_state.arquivo_atual}")

    # Aba 1: Filtros e Tabelas
    if aba_selecionada == "Filtros e Tabelas":
        st.markdown("---")
        st.subheader("📋 Visualização dos Dados")

        tipo_tabela = st.selectbox(
            "Selecione o tipo de tabela:",
            ["Completa", "Finalização", "Último Passe", "Construção de jogo"]
        )

        df_tabela = selecionar_colunas(df_filtrado, tipo_tabela)
        st.dataframe(df_tabela, use_container_width=True)

    # Aba 2: Relatório Individual
    elif aba_selecionada == "Relatório Individual":
        st.header("📄 Gerar Relatório Individual")

        jogadores = sorted(df_filtrado['Jogador'].dropna().unique())
        jogador_selecionado = st.selectbox("Escolha o jogador para gerar o relatório:", jogadores)

        coluna_posicao = 'Pos.' if 'Pos.' in df_filtrado.columns else 'Posição'
        posicoes = sorted(df_filtrado[coluna_posicao].dropna().unique())
        posicao_selecionada = st.selectbox("Selecione a posição do jogador:", posicoes)

        if st.button("Gerar Relatório PDF"):
            from main import gerar_relatorio_dados

            equipa = df_filtrado[df_filtrado['Jogador'] == jogador_selecionado]['Equipa'].values[0]
            df_auxiliar = df_filtrado[df_filtrado['Jogador'] == jogador_selecionado].copy()
            df_auxiliar[coluna_posicao] = posicao_selecionada

            caminho_pdf = gerar_relatorio_dados(
                df=df_filtrado,
                jogador=jogador_selecionado,
                equipa=equipa,
                posicao=posicao_selecionada,
                df_auxiliar=df_auxiliar,
                texto_conclusao=None,
                resumo_desempenho=None,
                exportar_pdf=True,
                nome_arquivo_df=st.session_state.arquivo_atual
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

    # Aba 3: Ranking por Perfil
    elif aba_selecionada == "Ranking por Perfil":
        exibir_ranking_por_perfil(df_filtrado)

    # Aba 4: Comparador entre Jogadores
    elif aba_selecionada == "Comparador entre jogadores":
        exibir_comparador(df_filtrado)

    # Aba 5: Gráfico de Dispersão
    elif aba_selecionada == "Gráfico de Dispersão":
        from paginas.dispersao import exibir_grafico_dispersao
        exibir_grafico_dispersao(df_filtrado)
        