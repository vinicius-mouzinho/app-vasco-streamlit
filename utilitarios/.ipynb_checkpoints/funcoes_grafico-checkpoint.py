# utilitarios/funcoes_grafico.py

import numpy as np
import matplotlib.pyplot as plt
from mplsoccer import PyPizza
from scipy.stats import percentileofscore
from .constantes import nomes_radar_metricas, pares_metricas_por_posicao, posicoes_equivalentes

# Função para obter todos os jogadores que atuam em posições equivalentes
def obter_grupo_posicao(df, posicao):
    equivalentes = posicoes_equivalentes.get(posicao, [posicao])
    return df[df['Posição'].astype(str).apply(lambda p: any(p.strip().startswith(eq) for eq in equivalentes))].copy()


# Função para gerar gráfico radar com ou sem comparação
def gerar_grafico_radar(jogador_df, grupo_posicao, posicao, jogador, nome_arquivo_radar, jogador_comparado=None):
    pares = pares_metricas_por_posicao.get(posicao, [])
    
    metricas_usadas = []
    for par in pares:
        for m in par:
            if m not in metricas_usadas:
                metricas_usadas.append(m)

    metricas_validas = [
        m for m in metricas_usadas
        if m in jogador_df.columns
        and grupo_posicao[m].notna().all()
        and np.isfinite(grupo_posicao[m]).all()
    ]

    if not metricas_validas:
        print(f"❌ Nenhuma métrica válida para gerar radar de {jogador}")
        return

    jogador_valores = jogador_df.iloc[0][metricas_validas].values.astype(float)
    percentuais_jogador = [
        int(round(np.clip(percentileofscore(grupo_posicao[m], val, kind="rank"), 0, 100)))
        if np.isfinite(val) else 50
        for m, val in zip(metricas_validas, jogador_valores)
    ]

    if jogador_comparado:
        comparado_df = grupo_posicao[(grupo_posicao["Equipa"] == "Vasco da Gama") & (grupo_posicao["Jogador"] == jogador_comparado)]
        if comparado_df.empty:
            print(f"⚠️ {jogador_comparado} não encontrado no Vasco para comparação.")
            return
        comparado_valores = comparado_df.iloc[0][metricas_validas].values.astype(float)
        percentuais_comparado = [
            int(round(np.clip(percentileofscore(grupo_posicao[m], val, kind="rank"), 0, 100)))
            if np.isfinite(val) else 50
            for m, val in zip(metricas_validas, comparado_valores)
        ]
    else:
        percentuais_comparado = None

    nomes_traduzidos = [nomes_radar_metricas.get(m, m) for m in metricas_validas]
    n = len(nomes_traduzidos)

    baker = PyPizza(
        params=nomes_traduzidos,
        min_range=[0] * n,
        max_range=[100] * n,
        background_color="#ffffff",
        straight_line_color="#000000",
        straight_line_lw=1,
        last_circle_lw=1,
        last_circle_color="#000000",
        inner_circle_size=8
    )

    slice_colors = ["#cc0000"] * n
    value_bck_colors = ["#cc0000"] * n
    value_colors = ["#ffffff"] * n

    compare_colors = ["#3D3D3D"] * n if jogador_comparado else None
    compare_value_colors = ["#ffffff"] * n if jogador_comparado else None
    compare_value_bck_colors = ["000000"] * n if jogador_comparado else None

    fig, ax = baker.make_pizza(
        values=percentuais_jogador,
        compare_values=percentuais_comparado,
        figsize=(8, 8),
        color_blank_space=["#f0f0f0"] * n,
        slice_colors=slice_colors,
        value_bck_colors=value_bck_colors,
        value_colors=value_colors,
        compare_colors=compare_colors,
        compare_value_colors=compare_value_colors,
        compare_value_bck_colors=compare_value_bck_colors,
        blank_alpha=0.4,
        kwargs_slices=dict(edgecolor="#000000", zorder=2, linewidth=1),
        kwargs_compare=dict(edgecolor="#000000", zorder=4, linewidth=1, alpha=1.0),
        kwargs_params=dict(color="#000000", fontsize=10, va="center"),
        kwargs_values=dict(
            color="#ffffff",
            fontsize=9,
            zorder=4,
            bbox=dict(edgecolor="none", facecolor="#cc0000", boxstyle="round,pad=0.2")
        ),
        kwargs_compare_values=dict(
            color="#ffffff",
            fontsize=9,
            zorder=5,
            bbox=dict(edgecolor="none", facecolor="#000000", boxstyle="round,pad=0.2")
        ) if jogador_comparado else None
    )

    for text_obj, p in zip(baker.value_texts, percentuais_jogador):
        text_obj.set_text(f"{p}%")
    if jogador_comparado:
        for text_obj, p in zip(baker.compare_value_texts, percentuais_comparado):
            text_obj.set_text(f"{p}%")

        fig.text(0.435, 1.02, jogador, fontsize=18, fontweight="bold", color="#cc0000", ha='right')
        fig.text(0.5, 1.02, "VS", fontsize=14, fontweight="normal", color="#444444", ha='center')
        fig.text(0.565, 1.02, jogador_comparado, fontsize=18, fontweight="bold", color="#000000", ha='left')
        fig.text(0.5, 1.06, "Radar de Desempenho Geral", fontsize=16, fontweight="bold", color="black", ha='center')
    else:
        fig.suptitle(f"{jogador}", fontsize=24, fontweight="bold", y=1.0005, color="#cc0000")

    fig.savefig(nome_arquivo_radar, dpi=300)
    plt.close(fig)

    # Validação de leitura
    with open(nome_arquivo_radar, "rb") as f:
        f.read()
