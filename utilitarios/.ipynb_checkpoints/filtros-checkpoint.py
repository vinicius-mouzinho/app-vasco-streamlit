import pandas as pd
import streamlit as st
from scipy.stats import percentileofscore

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
                opcoes_personalizadas = [
                    "Todos",
                    "Apenas Sul-Americanos",
                    "Sul-Americanos + Portugueses",
                    "Sul-Americanos + Portugueses + Espanhóis"
                ]
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
        
                elif pais_filtro == "Sul-Americanos + Portugueses + Espanhóis":
                    paises_alvo = paises_sulamericanos + ['Portugal', 'Spain']
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

        if 'Equipa na liga analisada' in df.columns:
            pass
        elif 'Equipa dentro de um período de tempo seleccionado' in df.columns:
            df.rename(columns={'Equipa dentro de um período de tempo seleccionado': 'Equipa na liga analisada'}, inplace=True)

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

        with col2:
            posicoes_disponiveis = sorted(df['Posição'].dropna().unique())
            posicoes_selecionadas = st.multiselect("Posições", posicoes_disponiveis, default=posicoes_disponiveis)
            if posicoes_selecionadas:
                df = df[df['Posição'].isin(posicoes_selecionadas)]
                filtros_aplicados['Posição'] = posicoes_selecionadas

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
                df[col_contrato] = pd.to_datetime(df[col_contrato], errors='coerce', dayfirst=True)
                datas_validas = df[col_contrato].dropna()

                if not datas_validas.empty:
                    data_min = datas_validas.min().date()
                    data_max = datas_validas.max().date()
                    data_limite = st.date_input("Contrato termina até:", value=data_max, min_value=data_min, max_value=data_max)
                    df = df[df[col_contrato].dt.date <= data_limite]
                    filtros_aplicados['Contrato termina até'] = data_limite

    # Salva cópia antes do filtro de percentil
    df_base_para_percentil = df.copy()

    # Filtro por múltiplos percentis
    with st.expander("📈 Filtros por Percentil em Métricas", expanded=False):
        colunas_numericas = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    
        num_filtros = st.number_input("Quantos filtros deseja aplicar?", min_value=1, max_value=10, value=1, step=1)
    
        filtros_percentil = []
        for i in range(num_filtros):
            st.markdown(f"**Filtro #{i+1}**")
            col1, col2 = st.columns(2)
            metrica = col1.selectbox(f"Métrica #{i+1}", colunas_numericas, key=f"metrica_{i}")
            percentil_min = col2.slider(f"Percentil mínimo #{i+1}", 0, 100, 50, key=f"percentil_{i}")
            filtros_percentil.append((metrica, percentil_min))
    
        for metrica, limite in filtros_percentil:
            valores = df[metrica]
            df[f"__percentil_{metrica}__"] = valores.apply(lambda x: percentileofscore(valores, x))
            df = df[df[f"__percentil_{metrica}__"] >= limite]
            df.drop(columns=[f"__percentil_{metrica}__"], inplace=True)

    return df, filtros_aplicados, df_base_para_percentil
