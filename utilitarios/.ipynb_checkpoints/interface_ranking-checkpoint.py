# utilitarios/interface_ranking.py

import streamlit as st
from utilitarios.funcoes_metricas import gerar_ranking_zscore
from utilitarios.constantes import liga_forca

# Cache dos rankings para evitar recálculo excessivo
@st.cache_data(show_spinner=False)
def gerar_ranking_cached(df, metricas, pesos):
    return gerar_ranking_zscore(df, metricas, pesos)

def exibir_ranking_por_perfil(df):
    st.markdown("---")
    st.header("📈 Ranking por Perfil de Jogador")

    PERFIS_PRE_DEFINIDOS = {
        "Meia de infiltração": {
            'Corridas progressivas/90': 0.5,
            'Passes progressivos/90': 0.75,
            'Passes progressivos certos, %': 0.75,
            'Dribles certos/ 90': 1.0,
            'Remates/90': 1.0,
            'Assistências esperadas por 100 passes': 2.0,
            'Golos sem ser por penálti/90': 2.0,
            'Toques na área/90': 2.0
        },
        "Extremo de força": {
            'Acelerações/90': 0.75,
            'Corridas progressivas/90': 1.25,
            'Frequência no drible (%)': 1.5,
            'Dribles com sucesso, %': 1.5,
            'Golos sem ser por penálti/90': 1.5,
            'Assistências esperadas por 100 passes': 1.5,
            'Duelos Defensivos por 30\' de Posse Adversária': 2.0,
            'Perdas de bola a cada 100 ações': -1.5
        }
    }

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
                df_ranking_raw = gerar_ranking_cached(df, metricas_selecionadas, pesos)

                if df_ranking_raw is not None and not df_ranking_raw.empty:
                    df_ranking = df_ranking_raw.copy()
                    if 'Liga' in df.columns:
                        if all(col in df.columns for col in ['Jogador', 'Equipa']) and all(col in df_ranking.columns for col in ['Jogador', 'Equipa']):
                            df_ranking = df_ranking.merge(
                                df[['Jogador', 'Equipa', 'Liga']],
                                on=['Jogador', 'Equipa'],
                                how='left'
                            )

                    if ajustar_por_liga and 'Liga' in df_ranking.columns:
                        df_ranking['Força da Liga'] = df_ranking['Liga'].map(liga_forca).fillna(80)
                        df_ranking['Z-Score Ajustado'] = df_ranking['Z-Score'] * df_ranking['Força da Liga'] / 100
                        df_ranking['Percentil Ajustado'] = df_ranking['Z-Score Ajustado'].rank(pct=True) * 100

                        # Organizar colunas para exibição
                        colunas_base = ['Jogador', 'Equipa', 'Posição', 'Liga', 'Força da Liga',
                                        'Z-Score Ajustado', 'Percentil Ajustado']
                        colunas_extra = [col for col in df_ranking.columns if col not in colunas_base]
                        df_exibir = df_ranking[colunas_base + colunas_extra]

                        st.success(f"✅ Ranking ajustado por liga gerado com {len(metricas_selecionadas)} métricas")
                        st.dataframe(df_exibir.style
                            .background_gradient(subset=["Z-Score Ajustado"], cmap="Greens")
                            .background_gradient(subset=["Percentil Ajustado"], cmap="Blues"),
                            use_container_width=True
                        )
                    else:
                        st.success(f"✅ Ranking gerado com {len(metricas_selecionadas)} métricas (sem ajuste por liga)")
                        st.dataframe(df_ranking.style
                            .background_gradient(subset=["Z-Score"], cmap="Greens")
                            .background_gradient(subset=["Percentil"], cmap="Blues"),
                            use_container_width=True
                        )
                else:
                    st.warning("⚠️ Ranking vazio ou erro nos dados.")

    else:
        st.info("Selecione um perfil para visualizar e ajustar métricas.")
