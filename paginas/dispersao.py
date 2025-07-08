import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Pares de métricas por posição com nome amigável

PARES_METRICAS_POR_POSICAO = {
    "CB": [
        ("Duelos Defensivos por 30' de Posse Adversária", "Duelos defensivos ganhos, %", "Eficiência Defensiva"),
        ("Duelos aérios/90", "Duelos aéreos ganhos, %", "Dominância Aérea"),
        ("Cortes/90", "Interseções/90", "Recuperações e Cortes"),
        ("Passes/90", "Passes certos, %", "Volume e Precisão de Passe"),
        ("Passes longos/90", "Passes longos certos, %", "Construção com Passes Longos"),
        ("Faltas/90", "Cartões amarelos/90", "Agressividade Defensiva"),
    ],
    "LB": [
        ("Cruzamentos/90", "Cruzamentos certos, %", "Eficiência nos Cruzamentos"),
        ("Assistências esperadas por 100 passes", "Passes progressivos certos/90", "Criação e Progresso"),
        ("Corridas progressivas/90", "Dribles/90", "Iniciativa Ofensiva"),
        ("Duelos ofensivos/90", "Duelos ofensivos ganhos, %", "1v1 no Ataque"),
        ("Duelos Defensivos por 30' de Posse Adversária", "Duelos defensivos ganhos, %", "Eficiência Defensiva Lateral"),
        ("Passes para terço final/90", "Passes certos para terço final, %", "Distribuição no Terço Final"),
    ],
    "RB": [
        ("Cruzamentos/90", "Cruzamentos certos, %", "Eficiência nos Cruzamentos"),
        ("Assistências/90", "Passes progressivos certos/90", "Criação pelo Corredor Direito"),
        ("Corridas progressivas/90", "Dribles/90", "Agressividade Ofensiva"),
        ("Duelos ofensivos/90", "Duelos ofensivos ganhos, %", "Confronto Individual Ofensivo"),
        ("Duelos Defensivos por 30' de Posse Adversária", "Duelos defensivos ganhos, %", "Solidez Defensiva"),
        ("Golos sem ser por penálti/90", "Assistências/90", "Participações Diretas em Gols"),
    ],
    "DMF": [
        ("Interceções ajust. à posse", "Ações Defensivas por 30' de Posse Adversária", "Recuperação e Cobertura"),
        ("Passes para a frente/90", "Passes para a frente certos, %", "Progresso Vertical"),
        ("Duelos/90", "Duelos ganhos, %", "Domínio Físico"),
        ("Passes progressivos/90", "Passes progressivos certos, %", "Distribuição Progressiva"),
        ("Faltas/90", "Cartões amarelos/90", "Intensidade Defensiva"),
    ],
    "CMF": [
        ("Assistências esperadas por 100 passes", "Passes chave/90", "Criação de Oportunidades"),
        ("Passes progressivos/90", "Passes progressivos certos, %", "Construção Progressiva"),
        ("Ações com a bola/90", "Perdas de bola a cada 100 ações", "Volume e Segurança"),
        ("Passes para terço final/90", "Passes certos para terço final, %", "Distribuição Avançada"),
        ("Duelos/90", "Duelos ganhos, %", "Competitividade em Campo"),
    ],
    "AMF": [
        ("Gols esperados (sem pênaltis)/90", "Assistências esperadas por 100 passes", "Participações em Gols Esperadas"),
        ("Golos sem ser por penálti/90", "Assistências/90", "Participações em Gols"),
        ("Dribles/90", "Frequência no drible (%)", "1v1 e Iniciativa"),
        ("Toques na área/90", "Remates à baliza/90", "Presença no Terço Final"),
        ("Passes progressivos/90", "Passes para a área de penálti/90", "Infiltração com Passes"),
    ],
    "LW": [
        ("Dribles/90", "Frequência no drible (%)", "Agressividade no 1v1"),
        ("Corridas progressivas/90", "Toques na área/90", "Progressão e Presença"),
        ("Assistências/90", "Cruzamentos certos, %", "Serviço e Entrega"),
        ("Golos sem ser por penálti/90", "Remates à baliza/90", "Finalização e Objetividade"),
        ("Passes para a área de penálti/90", "Assistências esperadas/90", "Criação na Área"),
    ],
    "RW": [
        ("Dribles/90", "Frequência no drible (%)", "Iniciativa Ofensiva Direita"),
        ("Golos sem ser por penálti/90", "Assistências/90", "Decisivo no Terço Final"),
        ("Cruzamentos/90", "Cruzamentos certos, %", "Eficiência nos Cruzamentos"),
        ("Passes chave/90", "Assistências esperadas por 100 passes", "Criação de Chances"),
        ("Remates à baliza/90", "Golos marcados, %", "Finalização com Eficiência"),
    ],
    "CF": [
        ("Golos sem ser por penálti/90", "Remates à baliza/90", "Finalização Direta"),
        ("Toques na área/90", "Remates/90", "Presença Ofensiva"),
        ("Golos de cabeça/90", "Duelos aéreos ganhos, %", "Jogo Aéreo"),
        ("Assistências/90", "Passes inteligentes/90", "Participação em Assistências"),
        ("Golos marcados, %", "Remates à baliza, %", "Aproveitamento nas Finalizações"),
    ],
}


def exibir_grafico_dispersao(df):
    st.header("📈 Gráfico de Dispersão Interativo")

    if df is None or df.empty:
        st.warning("Nenhum dado disponível para plotar.")
        return

    metricas_numericas = df.select_dtypes(include='number').columns.tolist()
    if not metricas_numericas:
        st.warning("Não há métricas numéricas suficientes no DataFrame.")
        return

    jogador_destaque = st.selectbox("🔍 Jogador em destaque (opcional)", ["Nenhum"] + sorted(df["Jogador"].dropna().unique()))

    modo = st.radio("Escolha o modo de visualização:", ["Pré-definido por posição", "Manual"])

    if modo == "Pré-definido por posição":
        posicoes_disponiveis = list(PARES_METRICAS_POR_POSICAO.keys())
        posicao_escolhida = st.selectbox("📌 Escolha a posição", posicoes_disponiveis)
        opcoes_metricas = PARES_METRICAS_POR_POSICAO[posicao_escolhida]
        nomes_disponiveis = [nome for _, _, nome in opcoes_metricas]
        nome_selecionado = st.selectbox("📊 Escolha a análise", nomes_disponiveis)
        eixo_x, eixo_y, _ = next(par for par in opcoes_metricas if par[2] == nome_selecionado)
    else:
        col1, col2 = st.columns(2)
        with col1:
            eixo_x = st.selectbox("📈 Eixo X", metricas_numericas)
        with col2:
            eixo_y = st.selectbox("📉 Eixo Y", metricas_numericas)
        nome_selecionado = f"{eixo_y} vs {eixo_x}"

    df_plot = df.copy()

    def grupo(row):
        if row["Jogador"] == jogador_destaque:
            return "Jogador Selecionado"
        elif "vasco" in str(row.get("Equipa", "")).lower():
            return "Jogador do Vasco"
        else:
            return "Outros"

    df_plot["Grupo"] = df_plot.apply(grupo, axis=1)
    df_plot["Label"] = df_plot["Jogador"]

    color_map = {
        "Jogador Selecionado": "darkorange",
        "Jogador do Vasco": "royalblue",
        "Outros": "saddlebrown"
    }

    fig = px.scatter(
        df_plot,
        x=eixo_x,
        y=eixo_y,
        color="Grupo",
        text="Label",
        hover_name="Jogador",
        opacity=0.85,
        color_discrete_map=color_map,
        height=800,
        template="plotly_white"
    )

    fig.update_traces(
        marker=dict(size=14),
        textposition='top center',
        textfont=dict(size=16)
    )

    media_x = df_plot[eixo_x].mean()
    media_y = df_plot[eixo_y].mean()

    fig.add_shape(
        type="line",
        x0=media_x, x1=media_x,
        y0=df_plot[eixo_y].min(), y1=df_plot[eixo_y].max(),
        line=dict(color="gray", width=1, dash="dash")
    )
    fig.add_shape(
        type="line",
        x0=df_plot[eixo_x].min(), x1=df_plot[eixo_x].max(),
        y0=media_y, y1=media_y,
        line=dict(color="gray", width=1, dash="dash")
    )

    fig.update_layout(
        title=nome_selecionado,
        xaxis_title=eixo_x,
        yaxis_title=eixo_y,
        legend_title="Grupo",
        font=dict(size=12),
        xaxis=dict(title=dict(text=eixo_x, font=dict(size=18))),
        yaxis=dict(title=dict(text=eixo_y, font=dict(size=18)))
    )

    st.plotly_chart(fig, use_container_width=True)
