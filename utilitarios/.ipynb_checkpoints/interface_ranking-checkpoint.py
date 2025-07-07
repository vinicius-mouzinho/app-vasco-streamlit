# utilitarios/interface_ranking.py

import streamlit as st
from utilitarios.funcoes_metricas import gerar_ranking_zscore
from utilitarios.constantes import liga_forca
from utilitarios.funcoes_pdf import exportar_ranking_pdf

PERFIS_PRE_DEFINIDOS = {
    "1º Volante Construtor": {
        'Ações Defensivas por 30\' de Posse Adversária': 1.5,
        'Duelos Defensivos por 30\' de Posse Adversária': 1.5,
        'Duelos aérios/90': 0.5,
        'Duelos aéreos ganhos, %': 0.5,
        'Faltas sofridas/90': 0.5,
        'Corridas progressivas/90': 0.5,
        'Ações com a bola/90': 2.0,
        'Passes para terço final/90': 1.0,
        'Passes certos para terço final, %': 1.0,
        'Passes progressivos/90': 1.5,
        'Passes progressivos certos, %': 1.5,
        'Perdas de bola a cada 100 ações': -2.0
    },
    "Meia de infiltração": {
        'Corridas progressivas/90': 1.0,
        'Passes progressivos/90': 1.0,
        'Passes progressivos certos, %': 1.0,
        'Dribles certos/ 90': 1.0,
        'Golos sem ser por penálti/90': 2.0,
        'Gols esperados (sem pênaltis)/90': 2.0,
        'Toques na área/90': 1.0,
        'Assistências esperadas por 100 passes': 3.0,
        'Perdas de bola a cada 100 ações': -2.0
    },
    "Extremo de força": {
        'Acelerações/90': 0.75,
        'Corridas progressivas/90': 1.25,
        'Frequência no drible (%)': 1.5,
        'Dribles com sucesso, %': 1.5,
        'Golos sem ser por penálti/90': 1.25,
        'Gols esperados (sem pênaltis)/90': 1.25,
        'Assistências esperadas por 100 passes': 2.5,
        'Duelos Defensivos por 30\' de Posse Adversária': 2.0,
        'Perdas de bola a cada 100 ações': -2.0
    }
}

@st.cache_data(show_spinner=False)
def gerar_ranking_cached(df, metricas, pesos):
    return gerar_ranking_zscore(df, metricas, pesos)

def exibir_ranking_por_perfil(df):
    st.markdown("---")
    st.header("📈 Ranking por Perfil de Jogador")

    perfil_selecionado = st.selectbox("Escolha um perfil-base:", ["Nenhum"] + list(PERFIS_PRE_DEFINIDOS.keys()))

    if perfil_selecionado != "Nenhum":
        metricas_default = PERFIS_PRE_DEFINIDOS[perfil_selecionado]
        st.markdown("### 🔍 Métricas e pesos do perfil (personalize abaixo)")

        metricas_disponiveis = sorted([
            col for col in df.columns
            if df[col].dtype in ['float64', 'int64'] and df[col].nunique() > 5
        ])

        metricas_selecionadas = st.multiselect(
            "Métricas selecionadas:",
            options=metricas_disponiveis,
            default=list(metricas_default.keys())
        )

        pesos = {}
        for metrica in metricas_selecionadas:
            col1, col2 = st.columns([0.7, 0.3])
            with col1:
                st.write(metrica)
            with col2:
                peso = st.number_input("Peso", key=metrica, value=metricas_default.get(metrica, 1.0), step=0.1)
                pesos[metrica] = peso

        ajustar_por_liga = st.checkbox("⚖️ Ajustar ranking pela força da liga", value=True)

        if st.button("🔄 Gerar Ranking"):
            with st.spinner("Calculando ranking..."):
                df_filtrado = df.copy()
                if 'Minutos jogados' in df_filtrado.columns:
                    df_filtrado = df_filtrado.sort_values(by='Minutos jogados', ascending=False)

                df_filtrado = df_filtrado.drop_duplicates(subset=['Jogador', 'Equipa', 'Liga'])
                df_ranking_raw = gerar_ranking_cached(df_filtrado, metricas_selecionadas, pesos)

                colunas_extras = ['Idade', 'Minutos jogados:', 'Valor de mercado', 'Contrato termina']
                colunas_disponiveis = [col for col in colunas_extras if col in df_filtrado.columns]

                df_ranking_raw = df_ranking_raw.merge(
                    df_filtrado[['Jogador', 'Equipa'] + colunas_disponiveis],
                    on=['Jogador', 'Equipa'],
                    how='left'
                )

                if df_ranking_raw is not None and not df_ranking_raw.empty:
                    df_ranking = df_ranking_raw.copy()
                    if ajustar_por_liga and 'Liga' in df_ranking.columns:
                        df_ranking['Força da Liga'] = df_ranking['Liga'].map(liga_forca).fillna(80)
                        df_ranking['Z-Score Ajustado'] = df_ranking['Z-Score'] * df_ranking['Força da Liga'] / 100
                        df_ranking['Percentil Ajustado'] = df_ranking['Z-Score Ajustado'].rank(pct=True) * 100
                    else:
                        df_ranking['Percentil'] = df_ranking['Z-Score'].rank(pct=True) * 100

                    st.session_state["df_ranking_gerado"] = df_ranking
                    st.session_state["ajuste_liga"] = ajustar_por_liga
                    st.session_state["perfil_selecionado"] = perfil_selecionado

    # Mostrar ranking se existir no estado
    if "df_ranking_gerado" in st.session_state:
        df_ranking = st.session_state["df_ranking_gerado"]
        ajustar_por_liga = st.session_state["ajuste_liga"]
        perfil_selecionado = st.session_state["perfil_selecionado"]

        # 🔁 Selecionar colunas a exibir conforme o modo
        if ajustar_por_liga and "Z-Score Ajustado" in df_ranking.columns:
            colunas_base = [
                'Jogador', 'Equipa', 'Posição', 'Idade', 'Minutos jogados:',
                'Valor de mercado', 'Contrato termina', 'Liga', 'Força da Liga',
                'Z-Score Ajustado', 'Percentil Ajustado'
            ]
        else:
            colunas_base = [
                'Jogador', 'Equipa', 'Posição', 'Idade', 'Minutos jogados',
                'Valor de mercado', 'Contrato termina', 'Liga', 'Z-Score', 'Percentil'
            ]
        
        colunas_extra = [col for col in df_ranking.columns if col not in colunas_base]
        df_exibir = df_ranking[colunas_base + colunas_extra].copy()
        
        # 🔧 Ajuste: arredondar floats
        colunas_float = df_exibir.select_dtypes(include=['float']).columns
        df_exibir[colunas_float] = df_exibir[colunas_float].round(2)
        
        # 🔧 Corrigir idade
        if 'Idade' in df_exibir.columns:
            df_exibir['Idade'] = df_exibir['Idade'].fillna(0).astype(int)
        
        # 🔧 Corrigir valor de mercado
        if 'Valor de mercado' in df_exibir.columns:
            def formatar_valor(valor):
                try:
                    valor_float = float(valor)
                    if valor_float >= 1_000_000:
                        return f"€{valor_float / 1_000_000:.2f}M"
                    elif valor_float >= 1_000:
                        return f"€{valor_float / 1_000:.0f} mil"
                    elif valor_float == 0:
                        return "Não informado"
                    else:
                        return f"€{valor_float:.0f}"
                except:
                    return valor
            df_exibir['Valor de mercado'] = df_exibir['Valor de mercado'].apply(formatar_valor)
        
        # 🔲 Gradiente personalizado para métricas do perfil
        metricas_para_gradiente = [m for m in metricas_selecionadas if m in df_exibir.columns]
        style = df_exibir.style

        # Definir colunas Z/P
        coluna_z = "Z-Score Ajustado" if ajustar_por_liga else "Z-Score"
        coluna_p = "Percentil Ajustado" if ajustar_por_liga else "Percentil"

        # Gradiente nos Z-Scores e Percentis
        style = style.background_gradient(subset=[coluna_z], cmap="Greens")
        style = style.background_gradient(subset=[coluna_p], cmap="Blues")

        # Métricas cujo menor valor é melhor
        metricas_invertidas = ["Perdas de bola a cada 100 ações"]

        for metrica in metricas_para_gradiente:
            if metrica in df_exibir.columns:
                serie = df_exibir[metrica]

                # Usa ranking percentual
                percentis = serie.rank(pct=True)

                # Inverte o gradiente se for métrica negativa
                if metrica in metricas_invertidas:
                    percentis = 1 - percentis

                style = style.background_gradient(
                    subset=[metrica],
                    cmap="RdYlGn",
                    gmap=percentis
                )

        st.dataframe(style, use_container_width=True)


        # PDF export
        num_extremos = st.slider("📥 Quantos jogadores extremos deseja incluir no PDF?", min_value=5, max_value=50, value=20)
        if st.button("📄 Baixar Ranking em PDF"):
            with st.spinner("Gerando PDF..."):
                pesos = pesos
                caminho_pdf = exportar_ranking_pdf(df_exibir, perfil=perfil_selecionado, pesos_utilizados=pesos, top_n=num_extremos)
                with open(caminho_pdf, "rb") as file:
                    st.download_button(
                        label="📥 Clique aqui para baixar o PDF",
                        data=file,
                        file_name=f"Ranking_{perfil_selecionado.replace(' ', '_')}.pdf",
                        mime="application/pdf"
                    )
    else:
        st.info("Selecione um perfil e clique em 'Gerar Ranking' para visualizar resultados.")
