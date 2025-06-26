import streamlit as st
import os
from dados.carregar_df_streamlit import carregar_df
import pandas as pd
from seguranca.autenticacao import criar_autenticador
from dados.unificar_dataframes import unificar_dataframes

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
    arquivos_disponiveis = [arq for arq in os.listdir(PASTA_DATAFRAMES) if arq.endswith(('.xlsx', '.csv', '.pkl'))]

    # Selecionar arquivo
    arquivo_selecionado = st.selectbox("Selecione um DataFrame:", ["Todos os jogadores da base de dados"] + arquivos_disponiveis)
    
    if arquivo_selecionado == "Todos os jogadores da base de dados":
        df = unificar_dataframes()
        st.success("✅ Todos os DataFrames foram unificados com sucesso.")
    else:
        df = carregar_df(arquivo_selecionado)
        st.success(f"✅ Arquivo carregado: {arquivo_selecionado}")

    # Carregar e mostrar o DataFrame
    if arquivo_selecionado:
        # Verificação de colunas necessárias
        if 'Naturalidade' in df.columns and 'País de nacionalidade' in df.columns:
            st.markdown("### 🔎 Filtros por Nacionalidade / Naturalidade")

            # Lista de países sul-americanos
            paises_sulamericanos = [
                'Brazil', 'Argentina', 'Uruguay', 'Colombia', 'Chile',
                'Paraguay', 'Peru', 'Ecuador', 'Bolivia', 'Venezuela'
            ]

            # Opções de filtro personalizadas
            opcoes_personalizadas = ["Todos", "Apenas Sul-Americanos", "Sul-Americanos + Portugueses"]

            # Coletar países únicos
            todos_paises_nacionalidade = set()
            for val in df['País de nacionalidade'].dropna():
                for pais in str(val).split(','):
                    todos_paises_nacionalidade.add(pais.strip())

            todos_paises_nacionalidade.update(df['Naturalidade'].dropna().unique())

            opcoes_filtro = opcoes_personalizadas + sorted(todos_paises_nacionalidade)
            pais_filtro = st.selectbox("Filtrar jogadores por país de nacionalidade ou naturalidade:", opcoes_filtro)
            
            # Aplicar filtro
            if pais_filtro == "Apenas Sul-Americanos":
                df = df[
                    df['Naturalidade'].isin(paises_sulamericanos) |
                    df['País de nacionalidade'].fillna('').apply(lambda x: any(pais in x for pais in paises_sulamericanos))
                ]
            elif pais_filtro == "Sul-Americanos + Portugueses":
                paises_alvo = paises_sulamericanos + ['Portugal']
                df = df[
                    df['Naturalidade'].isin(paises_alvo) |
                    df['País de nacionalidade'].fillna('').apply(lambda x: any(pais in x for pais in paises_alvo))
                ]
            elif pais_filtro != "Todos":
                df = df[
                    (df['Naturalidade'] == pais_filtro) |
                    (df['País de nacionalidade'].fillna('').str.contains(pais_filtro))
                ]

        # Padronizar coluna de equipe
        if 'Equipa dentro de um período de tempo seleccionado' in df.columns:
            df['Equipa'] = df['Equipa dentro de um período de tempo seleccionado']
            df.drop(columns=['Equipa dentro de um período de tempo seleccionado'], inplace=True)

        # Ajustar a posição principal e aplicar substituições padronizadas
        coluna_posicao_original = 'Pos.' if 'Pos.' in df.columns else 'Posição'
        df['Posição'] = (
            df[coluna_posicao_original]
            .astype(str)
            .str.split(',', n=1).str[0]
            .replace({
                'RMAF': 'RW',
                'LMAF': 'LW',
                'LAMF': 'AMF',
                'RAMF': 'AMF',
                'RDMF': 'DMF',
                'LDMF': 'DMF',
                'RCMF': 'CMF',
                'LCMF': 'CMF',
                'LWB': 'LB',
                'RWB': 'RB',
                'LWF': 'LW',
                'RWF': 'RW'
            })
        )
        
        # Filtros adicionais
        if 'Equipa' in df.columns:
            equipe_selecionada = st.selectbox("Filtrar por equipe (opcional):", ['Todas'] + sorted(df['Equipa'].dropna().unique()))
            if equipe_selecionada != 'Todas':
                df = df[df['Equipa'] == equipe_selecionada]

        posicoes_disponiveis = sorted(df['Posição'].dropna().unique())
        posicao_filtro = st.selectbox("Filtrar por posição (opcional):", ['Todas'] + posicoes_disponiveis)
        if posicao_filtro != 'Todas':
            df = df[df['Posição'] == posicao_filtro]

        # Mostrar DataFrame final
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
