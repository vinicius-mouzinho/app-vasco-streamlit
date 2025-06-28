import streamlit as st
from utilitarios.funcoes_metricas import gerar_ranking_zscore

def exibir_ranking_por_perfil(df):
    st.markdown("---")
    st.header("📈 Ranking por Perfil de Jogador")

    PERFIS_PRE_DEFINIDOS = {
        "Extremo de força": {
            'Acelerações/90': 1.0,
            'Corridas progressivas/90': 1.0,
            'Frequência no drible (%)': 1.5,
            'Dribles com sucesso, %': 1.5,
            'Golos sem ser por penálti/90': 1.5,
            'Assistências esperadas/90': 1.5,
            'Duelos Defensivos por 30\' de Posse Adversária': 2.0
        },
    # Você poderá adicionar novos perfis aqui depois
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
                peso = st.number_input("Peso", key=metrica, min_value=0.0, value=metricas_default.get(metrica, 1.0), step=0.1)
                pesos[metrica] = peso

        st.markdown("### 📊 Resultado do Ranking")

        with st.spinner("Calculando ranking..."):
            from utilitarios.funcoes_metricas import gerar_ranking_zscore
            df_ranking = gerar_ranking_zscore(df, metricas_selecionadas, pesos)

            if df_ranking is not None and not df_ranking.empty:
                st.success(f"✅ Ranking gerado com {len(metricas_selecionadas)} métricas personalizadas")
                st.dataframe(df_ranking.style
                    .background_gradient(subset=["Z-Score"], cmap="Greens")
                    .background_gradient(subset=["Percentil"], cmap="Blues"),
                    use_container_width=True
                )
            else:
                st.warning("⚠️ Ranking vazio ou erro nos dados.")
    else:
        st.info("Selecione um perfil para visualizar e ajustar métricas.")
