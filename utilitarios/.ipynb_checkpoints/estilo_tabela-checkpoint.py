import pandas as pd
from scipy.stats import percentileofscore
from utilitarios.estruturas_tabela import COLUNAS_FIXAS

def aplicar_cor_por_percentil_por_posicao(df, colunas_metricas, coluna_posicao="Posição", df_base=None):
    df_colorido = df.copy()

    # Usa df_base se fornecido, senão usa o próprio df
    base_para_percentil = df_base if df_base is not None else df

    # Pré-calcula os percentis por posição e métrica
    percentis_dict = {}
    for posicao, grupo in base_para_percentil.groupby(coluna_posicao):
        percentis_dict[posicao] = {}
        for col in colunas_metricas:
            if col in grupo.columns and pd.api.types.is_numeric_dtype(grupo[col]):
                valores = grupo[col].dropna().astype(float)
                percentis_dict[posicao][col] = valores.sort_values().reset_index(drop=True)

    # Função para aplicar estilo por linha (usando os percentis pré-calculados)
    def estilo_linha(row):
        posicao = row[coluna_posicao]
        estilos = []

        for col in df.columns:
            if col not in colunas_metricas:
                estilos.append("")
                continue

            try:
                valor = float(row[col])
                valores = percentis_dict.get(posicao, {}).get(col, None)
                if valores is None or len(valores) < 2:
                    estilos.append("")
                    continue

                percentil = (valores < valor).sum() / len(valores) * 100

                # Gradiente: 0 → vermelho, 50 → cinza, 100 → verde
                if percentil <= 50:
                    r = 255
                    g = int(255 * (percentil / 50))
                    b = int(255 * (percentil / 50))
                else:
                    r = int(255 * ((100 - percentil) / 50))
                    g = 255
                    b = int(255 * ((100 - percentil) / 50))

                cor = f"background-color: rgb({r}, {g}, {b}, 0.8)"
                estilos.append(cor)
            except:
                estilos.append("")
        return estilos

    return df_colorido.style.apply(lambda row: estilo_linha(row), axis=1)
