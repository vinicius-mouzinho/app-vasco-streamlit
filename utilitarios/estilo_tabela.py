# utilitarios/estilo_tabela.py

import pandas as pd
from scipy.stats import percentileofscore
from utilitarios.estruturas_tabela import COLUNAS_FIXAS

def aplicar_cor_por_percentil_por_posicao(df, colunas_metricas, coluna_posicao="Posição"):
    df_colorido = df.copy()

    # Pré-calcula os percentis por posição e métrica
    percentis_dict = {}
    for posicao, grupo in df.groupby(coluna_posicao):
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
                else:
                    r = int(255 * ((100 - percentil) / 50))
                    g = 255

                estilos.append(f"background-color: rgb({r}, {g}, 100);")
            except:
                estilos.append("")

        return estilos

    colunas_existentes = [col for col in COLUNAS_FIXAS + colunas_metricas if col in df.columns]
    df_visivel = df[colunas_existentes]
    return df_visivel.style.apply(estilo_linha, axis=1)
