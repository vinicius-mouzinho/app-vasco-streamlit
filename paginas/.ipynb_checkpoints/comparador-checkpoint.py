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
    
        metricas_numericas = [col for col in df.columns if df[col].dtype in ['float64', 'int64'] and df[col].nunique() > 5]
        metricas_comuns = [m for m in metricas_numericas if df_jogadores[m].notna().all()]
        metricas_selecionadas = st.multiselect("Métricas para comparar:", metricas_comuns, default=metricas_comuns[:6])
    
        if metricas_selecionadas and st.button("🔍 Comparar"):
            jogador1_data = df_jogadores[df_jogadores['Jogador'] == jogador1][metricas_selecionadas].values[0]
            jogador2_data = df_jogadores[df_jogadores['Jogador'] == jogador2][metricas_selecionadas].values[0]
    
            # Tabela comparativa
            st.subheader("📋 Tabela Comparativa")
            tabela = pd.DataFrame({
                "Métrica": metricas_selecionadas,
                jogador1: jogador1_data,
                jogador2: jogador2_data
            })
            st.dataframe(tabela.set_index("Métrica"), use_container_width=True)
    
            # Radar comparativo com PyPizza
            st.subheader("🎯 Radar Comparativo")
    
            fig, ax = plt.subplots(figsize=(10, 10))
            pizza = PyPizza(
                params=metricas_selecionadas,
                background_color="#FFFFFF",
                straight_line_color="#000000",
                straight_line_lw=1,
                last_circle_lw=1,
                other_circle_lw=0,
                inner_circle_size=0
            )
    
            # Normalizar valores de 0 a 100 para comparação visual
            valores_normalizados = pd.DataFrame([jogador1_data, jogador2_data], columns=metricas_selecionadas)
            valores_normalizados = (valores_normalizados - valores_normalizados.min()) / (valores_normalizados.max() - valores_normalizados.min()) * 100
    
            pizza.make_pizza(
                values=valores_normalizados.iloc[0].tolist(),
                compare_values=valores_normalizados.iloc[1].tolist(),
                figsize=(10, 10),
                color_blank_space="same",
                color_compare="#000000",     # preto
                color="#C00000",             # vermelho queimado Vasco
                edgecolor="#000000",
                kwargs_compare={"label": jogador2, "linewidth": 2},
                kwargs_patch={"label": jogador1, "linewidth": 2},
                ax=ax
            )
    
            plt.legend(loc="upper center", fontsize=14)
            st.pyplot(fig)
    
            # Exportar PDF
            st.subheader("📤 Exportar Comparativo")
            if st.button("📄 Gerar PDF"):
                pdf_path = exportar_comparativo_pdf(jogador1, jogador2, tabela, fig)
                with open(pdf_path, "rb") as f:
                    st.download_button(
                        label="⬇️ Baixar PDF",
                        data=f,
                        file_name=f"Comparativo_{jogador1}_vs_{jogador2}.pdf",
                        mime="application/pdf"
                    )
    
    
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
