import streamlit as st

def aplicar_filtros_basicos(df):
    """Aplica filtros interativos no DataFrame e retorna o DataFrame filtrado."""
    filtros_aplicados = {}

    st.markdown("## 🎛️ Filtros")

    with st.expander("Mostrar / Ocultar filtros", expanded=True):
        col1, col2 = st.columns(2)

        # Filtro por nacionalidade/naturalidade
        with col1:
            if 'Naturalidade' in df.columns and 'País de nacionalidade' in df.columns:
                paises_sulamericanos = [
                    'Brazil', 'Argentina', 'Uruguay', 'Colombia', 'Chile',
                    'Paraguay', 'Peru', 'Ecuador', 'Bolivia', 'Venezuela'
                ]
                opcoes_personalizadas = ["Todos", "Apenas Sul-Americanos", "Sul-Americanos + Portugueses"]
                todos_paises_nacionalidade = set()

                for val in df['País de nacionalidade'].dropna():
                    for pais in str(val).split(','):
                        todos_paises_nacionalidade.add(pais.strip())

                todos_paises_nacionalidade.update(df['Naturalidade'].dropna().unique())
                opcoes_filtro = opcoes_personalizadas + sorted(todos_paises_nacionalidade)
                pais_filtro = st.selectbox("País", opcoes_filtro)

                if pais_filtro == "Apenas Sul-Americanos":
                    df = df[
                        df['Naturalidade'].isin(paises_sulamericanos) |
                        df['País de nacionalidade'].fillna('').apply(lambda x: any(pais in x for pais in paises_sulamericanos))
                    ]
                    filtros_aplicados['País'] = paises_sulamericanos
                elif pais_filtro == "Sul-Americanos + Portugueses":
                    paises_alvo = paises_sulamericanos + ['Portugal']
                    df = df[
                        df['Naturalidade'].isin(paises_alvo) |
                        df['País de nacionalidade'].fillna('').apply(lambda x: any(pais in x for pais in paises_alvo))
                    ]
                    filtros_aplicados['País'] = paises_alvo
                elif pais_filtro != "Todos":
                    df = df[
                        (df['Naturalidade'] == pais_filtro) |
                        (df['País de nacionalidade'].fillna('').str.contains(pais_filtro))
                    ]
                    filtros_aplicados['País'] = pais_filtro

        # Padronizar nome da coluna de equipe, se necessário
        if 'Equipa dentro de um período de tempo seleccionado' in df.columns:
            df['Equipa'] = df['Equipa dentro de um período de tempo seleccionado']
            df.drop(columns=['Equipa dentro de um período de tempo seleccionado'], inplace=True)

        # Padronizar coluna de posição
        coluna_posicao_original = 'Pos.' if 'Pos.' in df.columns else 'Posição'
        df['Posição'] = (
            df[coluna_posicao_original]
            .astype(str)
            .str.split(',', n=1).str[0]
            .replace({
                'RMAF': 'RW', 'LMAF': 'LW', 'LAMF': 'LW', 'RAMF': 'RW',
                'RDMF': 'DMF', 'LDMF': 'DMF', 'RCMF': 'CMF', 'LCMF': 'CMF',
                'LWB': 'LB', 'RWB': 'RB', 'LWF': 'LW', 'RWF': 'RW'
            })
        )

        # Filtro por posição
        with col2:
            posicoes_disponiveis = sorted(df['Posição'].dropna().unique())
            posicoes_selecionadas = st.multiselect("Posições", posicoes_disponiveis, default=posicoes_disponiveis)
            if posicoes_selecionadas:
                df = df[df['Posição'].isin(posicoes_selecionadas)]
                filtros_aplicados['Posição'] = posicoes_selecionadas


        # LINHA 2: IDADE / MINUTOS / CONTRATO
        col3, col4, col5 = st.columns(3)

        with col3:
            if 'Idade' in df.columns:
                idade_min = st.number_input("Idade mínima", min_value=10, max_value=50, value=15)
                idade_max = st.number_input("Idade máxima", min_value=10, max_value=50, value=40)
                df = df[(df['Idade'] >= idade_min) & (df['Idade'] <= idade_max)]
                filtros_aplicados['Idade'] = (idade_min, idade_max)

        with col4:
            minutos_col = next((col for col in df.columns if 'minuto' in col.lower()), None)
            if minutos_col:
                minutos_min = st.number_input("Minutos jogados (mín.)", min_value=0, value=0)
                df = df[df[minutos_col] >= minutos_min]
                filtros_aplicados['Minutos'] = minutos_min

        with col5:
            col_contrato = next((col for col in df.columns if 'contrato' in col.lower()), None)
            if col_contrato:
                anos_contrato = sorted(df[col_contrato].dropna().astype(str).unique())
                ano_filtro = st.selectbox("Contrato termina em:", ["Todos"] + anos_contrato)
                if ano_filtro != "Todos":
                    df = df[df[col_contrato].astype(str).str.contains(ano_filtro)]
                    filtros_aplicados['Contrato termina'] = ano_filtro

    return df, filtros_aplicados
