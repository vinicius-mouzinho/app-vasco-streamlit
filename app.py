# app.py

import streamlit as st
import os
import pandas as pd
from dados.carregar_df_streamlit import carregar_df, listar_arquivos_sem_extensao
from seguranca.autenticacao import criar_autenticador
from dados.unificar_dataframes import unificar_dataframes
from utilitarios.filtros import aplicar_filtros_basicos
from utilitarios.interface_ranking import exibir_ranking_por_perfil
from utilitarios.estruturas_tabela import selecionar_colunas
from paginas.relatorio_individual import exibir_pagina_relatorio_individual
from paginas.comparador import exibir_comparador
from utilitarios.estilo_tabela import aplicar_cor_por_percentil_por_posicao
from utilitarios.estruturas_tabela import COLUNAS_FIXAS

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

    # Mapeamento: nomes limpos -> nomes reais
    mapa_arquivos = listar_arquivos_sem_extensao()
    nomes_limpos = list(mapa_arquivos.keys())

    # Define o padrão
    if "arquivo_atual" not in st.session_state:
        st.session_state.arquivo_atual = "Todos os jogadores.pkl"

    nome_limpo_atual = os.path.splitext(st.session_state.arquivo_atual)[0]

    nome_escolhido = st.selectbox(
        "Selecione um DataFrame:",
        nomes_limpos,
        index=nomes_limpos.index(nome_limpo_atual) if nome_limpo_atual in nomes_limpos else 0
    )

    # Atualiza session_state e recarrega cache
    arquivo_selecionado = mapa_arquivos[nome_escolhido]
    if arquivo_selecionado != st.session_state.arquivo_atual:
        st.session_state.arquivo_atual = arquivo_selecionado
        st.cache_data.clear()

    # Carrega o DataFrame
    df = carregar_df(st.session_state.arquivo_atual)
    df_filtrado, filtros_aplicados, df_base_para_percentil = aplicar_filtros_basicos(df)

    st.success(f"✅ Arquivo carregado: {st.session_state.arquivo_atual}")

    # Aba 1: Filtros e Tabelas
    if aba_selecionada == "Filtros e Tabelas":
        st.markdown("---")
        st.subheader("📋 Visualização dos Dados")

        tipo_tabela = st.selectbox(
            "Selecione o tipo de tabela:",
            ["Completa", "Finalização", "Último Passe", "Construção de jogo", "Drible e 1x1"]
        )

        df_tabela = selecionar_colunas(df_filtrado, tipo_tabela)
        colunas_metricas = [col for col in df_tabela.columns if col not in COLUNAS_FIXAS]
        
        if tipo_tabela != "Completa":
            df_base_tabela = selecionar_colunas(df_base_para_percentil, tipo_tabela)
            styled_df = aplicar_cor_por_percentil_por_posicao(df_tabela, colunas_metricas, df_base=df_base_tabela)
            st.write(styled_df)
        else:
            st.dataframe(df_tabela, use_container_width=True, hide_index=True)

    # Aba 2: Relatório Individual
    elif aba_selecionada == "Relatório Individual":
        exibir_pagina_relatorio_individual()

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
