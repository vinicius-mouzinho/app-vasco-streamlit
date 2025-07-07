#paginas/comparador.py

import streamlit as st
import pandas as pd
from pathlib import Path
from mplsoccer import PyPizza
import matplotlib.pyplot as plt
from PIL import Image
from dados.carregar_df_streamlit import carregar_df
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import tempfile
import os
from utilitarios.interface_ranking import PERFIS_PRE_DEFINIDOS
from scipy.stats import percentileofscore

def exibir_comparador(df):
    st.write("🔧 Comparador carregado com sucesso")
    # Carregar logo
    logo_path = Path("assets/logo.png")
    if logo_path.exists():
        logo = Image.open(logo_path)
        st.image(logo, width=120)
    
    st.title("🆚 Comparador entre Jogadores")
    
    # Filtros básicos (opcional)
    col1, col2 = st.columns(2)
    with col1:
        posicoes = sorted(df['Posição'].dropna().unique())
        posicao_filtro = st.selectbox("Filtrar por posição (opcional):", ["Todas"] + posicoes)
    
    with col2:
        equipes = sorted(df['Equipa'].dropna().unique())
        equipe_filtro = st.selectbox("Filtrar por equipe (opcional):", ["Todas"] + equipes)
    
    df_filtrado = df.copy()
    if posicao_filtro != "Todas":
        df_filtrado = df_filtrado[df_filtrado['Posição'] == posicao_filtro]
    if equipe_filtro != "Todas":
        df_filtrado = df_filtrado[df_filtrado['Equipa'] == equipe_filtro]
    
    # Seleção de jogadores
    jogadores_disponiveis = sorted(df_filtrado['Jogador'].unique())
    col1, col2 = st.columns(2)
    with col1:
        jogador1 = st.selectbox("Jogador 1", jogadores_disponiveis)
    with col2:
        jogador2 = st.selectbox("Jogador 2", jogadores_disponiveis, index=1 if len(jogadores_disponiveis) > 1 else 0)
    
    if jogador1 == jogador2:
        st.warning("Selecione dois jogadores diferentes.")
    else:
        df_jogadores = df_filtrado[df_filtrado['Jogador'].isin([jogador1, jogador2])]
    
        metricas_usadas_nos_perfis = sorted(set(m for perfil in PERFIS_PRE_DEFINIDOS.values() for m in perfil))
        metricas_comuns = [m for m in metricas_usadas_nos_perfis if m in df.columns and df_jogadores[m].notna().all()]
        # Selecionar um perfil pronto
        perfil_escolhido = st.selectbox("Escolha um perfil-base para comparação:", list(PERFIS_PRE_DEFINIDOS.keys()))
        metricas_perfil = list(PERFIS_PRE_DEFINIDOS[perfil_escolhido].keys())
        
        # Confirmar as métricas do perfil com opção de ajuste manual
        st.markdown("### 📊 Métricas usadas na comparação:")
        metricas_selecionadas = st.multiselect(
            "Métricas para comparar:",
            options=metricas_comuns,
            default=metricas_perfil
        )
    
        if metricas_selecionadas and st.button("🔍 Comparar"):
            jogador1_data = df_jogadores[df_jogadores['Jogador'] == jogador1][metricas_selecionadas].values[0]
            jogador2_data = df_jogadores[df_jogadores['Jogador'] == jogador2][metricas_selecionadas].values[0]
    
            # Tabela comparativa com coloração por percentil
            st.subheader("📋 Tabela Comparativa")
            
            # Criar cópia dos dados para calcular percentis com base em jogadores da mesma posição com mais de 900 minutos
            coluna_posicao = "Posição" if "Posição" in df.columns else "Pos."
            grupo_referencia = df[(df[coluna_posicao] == df_jogadores[coluna_posicao].values[0]) & (df["Minutos jogados:"] > 900)]
            
            # Função para calcular percentil (inverso para algumas métricas)
            def calcular_percentil(metrica, valor):
                if grupo_referencia[metrica].dropna().empty:
                    return None
                if metrica == "Perdas de bola a cada 100 ações":
                    return 100 - percentileofscore(grupo_referencia[metrica].dropna(), valor)
                else:
                    return percentileofscore(grupo_referencia[metrica].dropna(), valor)
            
            # Construir DataFrame da tabela
            linhas = []
            for metrica in metricas_selecionadas:
                val1 = df_jogadores[df_jogadores['Jogador'] == jogador1][metrica].values[0]
                val2 = df_jogadores[df_jogadores['Jogador'] == jogador2][metrica].values[0]
                p1 = calcular_percentil(metrica, val1)
                p2 = calcular_percentil(metrica, val2)
                linhas.append({
                    "Métrica": metrica,
                    jogador1: val1,
                    jogador2: val2,
                    f"{jogador1}_percentil": p1,
                    f"{jogador2}_percentil": p2
                })
            
            tabela = pd.DataFrame(linhas)
            tabela_formatada = tabela[["Métrica", jogador1, jogador2]].copy()

            # Estilizar tabela com cores baseadas nos percentis
            def colorir(val, percentil):
                if pd.isna(percentil):
                    return "color: black"
                if percentil >= 75:
                    return "color: white; background-color: green"
                elif percentil >= 50:
                    return "color: black; background-color: lightgreen"
                elif percentil >= 25:
                    return "color: black; background-color: #ffd580"  # amarelo claro
                else:
                    return "color: white; background-color: red"
            
            def colorir_tabela(row):
                estilo_linha = {}
                nome_metrica = row["Métrica"]
            
                val1 = row[jogador1]
                val2 = row[jogador2]
            
                # Pegar os percentis reais da outra tabela
                p1 = tabela[tabela["Métrica"] == nome_metrica][f"{jogador1}_percentil"].values[0]
                p2 = tabela[tabela["Métrica"] == nome_metrica][f"{jogador2}_percentil"].values[0]
            
                for jogador, percentil in zip([jogador1, jogador2], [p1, p2]):
                    if pd.isna(percentil):
                        estilo_linha[jogador] = "color: black"
                    elif percentil >= 75:
                        estilo_linha[jogador] = "color: white; background-color: green"
                    elif percentil >= 50:
                        estilo_linha[jogador] = "color: black; background-color: lightgreen"
                    elif percentil >= 25:
                        estilo_linha[jogador] = "color: black; background-color: #ffd580"
                    else:
                        estilo_linha[jogador] = "color: white; background-color: red"
            
                estilo_linha["Métrica"] = ""  # sem estilo
                return pd.Series(estilo_linha)

            # Montar tabela com valor + percentil formatado
            tabela_formatada = tabela[["Métrica"]].copy()
            for jogador in [jogador1, jogador2]:
                col_val = tabela[jogador]
                col_pct = tabela[f"{jogador}_percentil"]
                col_fmt = col_val.round(2).astype(str) + " (" + "> " + col_pct.round(0).fillna(0).astype(int).astype(str) + "%)"
                tabela_formatada[jogador] = col_fmt
            
            # Aplicar gradiente com base nos percentis
            percentis_only = tabela[[f"{jogador1}_percentil", f"{jogador2}_percentil"]].copy()
            
            # Renomear colunas para coincidir com a tabela_formatada
            percentis_only.columns = [jogador1, jogador2]
            
            # Aplica gradiente com base no DataFrame de percentis (como gmap)
            st.dataframe(
                tabela_formatada.style.background_gradient(
                    axis=None,
                    subset=[jogador1, jogador2],
                    cmap="RdYlGn",
                    gmap=percentis_only[[jogador1, jogador2]]
                ),
                use_container_width=True
            )

            # Explicação da tabela
            with st.expander("ℹ️ Entenda a Tabela Comparativa"):
                st.markdown("""
                - Cada linha representa uma **métrica estatística** utilizada na comparação dos dois jogadores.
                - Os valores exibidos seguem o formato: `valor numérico (percentil)`  
                  Exemplo: `1.85 (> 78%)` significa que o jogador teve **1.85** nessa métrica, com desempenho superior a **78%** dos jogadores da mesma posição.
                - O **fundo colorido** da célula representa o nível de desempenho em relação ao grupo:
                    - 🟩 Verde forte: percentil acima de 75 (excelente)
                    - 🟨 Amarelo: percentil entre 25 e 50 (regular)
                    - 🟥 Vermelho: percentil abaixo de 25 (baixo desempenho)
                - Para a métrica **"Perdas de bola a cada 100 ações"**, o percentil é **invertido**: quanto **menor** o valor, **melhor** o desempenho. Uma célula mais verde indica que o jogador perde menos a bola.
                """)
            import numpy as np
            import matplotlib.pyplot as plt
            from mplsoccer import PyPizza
            
            st.subheader("🎯 Radar Comparativo")
            
            # Normalização entre 0 e 1
            valores_normalizados = pd.DataFrame([jogador1_data, jogador2_data], columns=metricas_selecionadas)
            valores_normalizados = (valores_normalizados - valores_normalizados.min()) / (valores_normalizados.max() - valores_normalizados.min())
            
            val_j1 = valores_normalizados.iloc[0].tolist()
            val_j2 = valores_normalizados.iloc[1].tolist()
            labels = metricas_selecionadas
            
            # Preparar o radar
            num_vars = len(labels)
            angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
            val_j1 += val_j1[:1]
            val_j2 += val_j2[:1]
            angles += angles[:1]
            
            fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
            ax.set_theta_offset(np.pi / 2)
            ax.set_theta_direction(-1)
            
            # Linhas de contorno
            ax.plot(angles, val_j1, color="#C00000", linewidth=2, label=jogador1)
            ax.fill(angles, val_j1, color="#C00000", alpha=0.25)
            
            ax.plot(angles, val_j2, color="#000000", linewidth=2, label=jogador2)
            ax.fill(angles, val_j2, color="#000000", alpha=0.25)
            
            # Ajustes de eixos
            ax.set_thetagrids(np.degrees(angles[:-1]), labels, fontsize=10)
            ax.set_ylim(0, 1)
            ax.grid(True)
            
            # Legenda
            ax.legend(loc='upper right', bbox_to_anchor=(1.2, 1.1))
            
            st.pyplot(fig)

    
# Função auxiliar para gerar PDF
def exportar_comparativo_pdf(jogador1, jogador2, tabela_df, radar_fig):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
        doc = SimpleDocTemplate(tmpfile.name, pagesize=A4)
        story = []
        styles = getSampleStyleSheet()

        # Logo
        logo_path = "assets/logo.png"
        if os.path.exists(logo_path):
            story.append(RLImage(logo_path, width=80, height=80))
            story.append(Spacer(1, 12))

        # Título
        story.append(Paragraph(f"<b>Comparativo entre {jogador1} e {jogador2}</b>", styles['Title']))
        story.append(Spacer(1, 12))

        # Tabela
        data = [tabela_df.columns.tolist()] + tabela_df.values.tolist()
        table = Table(data)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#C00000")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ]))
        story.append(table)
        story.append(Spacer(1, 24))

        # Salvar radar como imagem temporária
        radar_path = os.path.join(tempfile.gettempdir(), "radar.png")
        radar_fig.savefig(radar_path, dpi=300, bbox_inches='tight')
        story.append(RLImage(radar_path, width=400, height=400))

        doc.build(story)

        return tmpfile.name
