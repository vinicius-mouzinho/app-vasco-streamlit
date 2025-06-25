# utilitarios/interpretacoes.py

import os
import tempfile
import numpy as np
import pandas as pd
import textwrap
import matplotlib.pyplot as plt
from scipy.stats import percentileofscore
from .constantes import metricas_traduzidas, contextos_gerais

# Função para interpretar uma métrica individual
def interpretar(jogador, metrica, valor, serie_comparativa, pontos_fortes, pontos_fracos, segunda=False):
    if pd.isna(valor):
        return f"Dados indisponíveis para {metrica.lower()}."

    nome_metrica = metricas_traduzidas.get(metrica, metrica).replace('\n', ' ')
    percentil = percentileofscore(serie_comparativa, valor, kind='rank')
    ranking = serie_comparativa.rank(ascending=False, method='min')
    posicao_rk = ranking[serie_comparativa == valor].min()

    if percentil > 65:
        pontos_fortes.append(metrica)
    elif percentil < 35:
        pontos_fracos.append(metrica)

    contexto = ""
    if percentil > 65 and metrica in contextos_gerais:
        contexto = contextos_gerais[metrica]["positivo"]
    elif percentil < 35 and metrica in contextos_gerais:
        contexto = contextos_gerais[metrica]["negativo"]

    inicio = f"Em relação a {nome_metrica}, " if segunda else f"Em {nome_metrica}, {jogador} "

    if posicao_rk == len(serie_comparativa):
        return f"{inicio}figura entre os desempenhos mais baixos da liga ({valor:.2f}), {contexto}"
    elif percentil == 100:
        return f"{inicio}é o principal destaque da posição, com {valor:.2f}, {contexto}"
    elif percentil >= 90:
        return f"{inicio}apresenta números muito acima da média, com {valor:.2f}, {contexto}"
    elif percentil >= 65:
        return f"{inicio}está bem acima da média da posição, com {valor:.2f}, {contexto}"
    elif percentil > 50:
        return f"{inicio}está acima da média da posição, com {valor:.2f}."
    elif percentil == 50:
        return f"{inicio}apresenta números compatíveis com a média ({valor:.2f})."
    elif percentil <= 35:
        return f"{inicio}tem desempenho bem abaixo da média ({valor:.2f}), {contexto}"
    else:
        return f"{inicio}está abaixo da média da posição, com {valor:.2f}. {contexto}"


# Função auxiliar para mostrar gráfico + parágrafos
def gerar_paragrafo_com_grafico(
    m1, m2, texto_1, texto_2,
    grupo_posicao, jogador, equipa,
    imagens, textos, exportar_pdf
):
    def exibir_grafico_dispersao(df_plot, metrica_x, metrica_y, jogador, equipa, nome_arquivo=None):
        fig, ax = plt.subplots(figsize=(6, 5))
        outros = df_plot[(df_plot['Equipa'] != 'Vasco da Gama') & ~(df_plot['Jogador'] == jogador)]
        vasco = df_plot[df_plot['Equipa'] == 'Vasco da Gama']
        jogador_row = df_plot[(df_plot['Jogador'] == jogador) & (df_plot['Equipa'] == equipa)]

        ax.scatter(outros[metrica_x], outros[metrica_y], color='gray', alpha=0.4)
        ax.scatter(vasco[metrica_x], vasco[metrica_y], color='blue')
        for _, row in vasco.iterrows():
            ax.text(row[metrica_x], row[metrica_y], row['Jogador'], fontsize=8, color='blue')

        if not jogador_row.empty:
            x = jogador_row[metrica_x].values[0]
            y = jogador_row[metrica_y].values[0]
            if pd.notna(x) and pd.notna(y) and np.isfinite(x) and np.isfinite(y):
                ax.scatter(x, y, color='orange', s=120, edgecolor='black', zorder=5)
                ax.text(x, y, jogador, fontsize=9, weight='bold', color='orange')

        media_x = df_plot[metrica_x].mean()
        media_y = df_plot[metrica_y].mean()
        ax.axvline(media_x, color='black', linestyle='dashed', linewidth=1)
        ax.axhline(media_y, color='black', linestyle='dashed', linewidth=1)
        ax.set_xlabel(metricas_traduzidas.get(metrica_x, metrica_x))
        ax.set_ylabel(metricas_traduzidas.get(metrica_y, metrica_y))
        if metrica_y == "Faltas/90":
            ax.invert_yaxis()
        titulo_bruto = f"{metricas_traduzidas.get(metrica_x)} vs {metricas_traduzidas.get(metrica_y)}"
        titulo_formatado = textwrap.fill(titulo_bruto, width=45)
        ax.set_title(titulo_formatado, fontsize=11, loc='center')

        plt.tight_layout()

        if nome_arquivo:
            plt.savefig(nome_arquivo)
            plt.close()
        else:
            plt.show()

    if exportar_pdf:
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:
            exibir_grafico_dispersao(grupo_posicao, m1, m2, jogador, equipa, nome_arquivo=tmpfile.name)
            imagens.append(tmpfile.name)
            textos.append(texto_1 + "\n" + texto_2)
    else:
        exibir_grafico_dispersao(grupo_posicao, m1, m2, jogador, equipa)
        print(texto_1 + "\n" + texto_2 + "\n")
