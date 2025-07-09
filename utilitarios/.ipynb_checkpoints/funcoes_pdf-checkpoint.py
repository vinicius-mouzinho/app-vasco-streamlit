# utilitarios/funcoes_pdf.py

import os
import tempfile
from utilitarios.constantes import posicoes_formatadas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle
)
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import tempfile
import os
from utilitarios.constantes import abreviar_liga

# REGISTRO DAS FONTES
pdfmetrics.registerFont(TTFont("Inter", "assets/Inter-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Inter-Bold", "assets/Inter-Bold.ttf"))

# ESTILOS DE PARÁGRAFOS
styles = getSampleStyleSheet()

TituloJogador = ParagraphStyle(
    name="TituloJogador",
    fontName="Inter-Bold",
    fontSize=34,
    leading=36,
    spaceAfter=10,
    alignment=TA_LEFT
)

Subtitulo = ParagraphStyle(
    name="Subtitulo",
    fontName="Inter",
    fontSize=15,
    leading=18,
    spaceBefore=0,
    spaceAfter=4,
    alignment=TA_LEFT
)

TextoJustificado = ParagraphStyle(
    name="TextoJustificado",
    fontName="Inter",
    fontSize=11,
    leading=16,
    alignment=TA_JUSTIFY
)

TextoResumo = ParagraphStyle(
    name="TextoResumo",
    fontName="Inter",
    fontSize=11,
    leading=16,
    alignment=TA_LEFT,
    leftIndent=10,
    spaceBefore=6
)

TituloResumo = ParagraphStyle(
    name="TituloResumo",
    fontName="Inter-Bold",
    fontSize=13,
    leading=18,
    spaceBefore=14,
    spaceAfter=4,
    alignment=TA_LEFT
)

def gerar_pdf_jogador(
    jogador, posicao, equipa, liga,
    textos, imagens,
    radar_path=None,
    radar_path_final=None,
    texto_conclusao=None,
    resumo_desempenho=None,
    comparacao_contextual_bs=None,
    comparacao_vasco_bs=None,
    caminho_saida=None,
    descricao_inicial=None
):
    if not caminho_saida:
        caminho_saida = os.path.join(tempfile.gettempdir(), f"{jogador}_relatorio.pdf")

    doc = SimpleDocTemplate(caminho_saida, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=1.5*cm, bottomMargin=1.5*cm)

    story = []
    from reportlab.platypus import Table, TableStyle, Image as RLImage

    logo_path = os.path.join("assets", "logo.png")
    if os.path.exists(logo_path):
        logo = RLImage(logo_path)
        logo._restrictSize(4*cm, 4*cm)  # limite máximo sem distorcer
    else:
        logo = Spacer(1, 4*cm)  # fallback
    
    titulo_coluna = [
        Paragraph(f"<b>{jogador} - {equipa} ({liga})</b>", TituloJogador),
        Paragraph("Relatório Comparativo (VS Atletas do BR2024)", Subtitulo),
        Paragraph("Departamento de Scout - Vasco", Subtitulo)
]
    
    cabecalho = Table([[logo, titulo_coluna]], colWidths=[3.6*cm, 13.4*cm])
    cabecalho.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ]))
    
    story.append(cabecalho)
    story.append(Spacer(1, 20))

    if descricao_inicial:
        story.append(Paragraph(descricao_inicial.strip(), TextoJustificado))
        story.append(Spacer(1, 30))

    # Radar
    if radar_path and os.path.exists(radar_path):
        story.append(Image(radar_path, width=15*cm, height=15*cm))
        story.append(Spacer(1, 12))

    # Gráficos de dispersão + interpretações
    for img, texto in zip(imagens, textos):
        if os.path.exists(img):
            story.append(Image(img, width=15*cm, height=12*cm))
        story.append(Paragraph(texto, TextoJustificado))
        story.append(Spacer(1, 10))

    # Comparações
    if comparacao_contextual_bs and os.path.exists(comparacao_contextual_bs):
        story.append(PageBreak())
        story.append(Paragraph("Comparativo Estatístico - Contexto Geral", Subtitulo))
        story.append(Spacer(1, 6))
        story.append(Image(comparacao_contextual_bs, width=17*cm, height=11*cm))
        story.append(Spacer(1, 8))

    if comparacao_vasco_bs and os.path.exists(comparacao_vasco_bs):
        story.append(Paragraph("Comparativo Estatístico - Vasco da Gama", Subtitulo))
        story.append(Spacer(1, 6))
        story.append(Image(comparacao_vasco_bs, width=17*cm, height=11*cm))
        story.append(Spacer(1, 8))

    # Conclusão
    if texto_conclusao:
        story.append(Paragraph("Conclusão", TituloResumo))
        story.append(Paragraph(texto_conclusao.strip(), TextoJustificado))

    # Resumo final
    if resumo_desempenho:
        pontos_fortes = resumo_desempenho.get("pontos_fortes", [])
        pontos_fracos = resumo_desempenho.get("pontos_fracos", [])

        story.append(PageBreak())
        story.append(Paragraph("Resumo do Desempenho", TituloResumo))

        if pontos_fortes:
            story.append(Paragraph("Pontos fortes", TituloResumo))
            story.append(Spacer(1, 6))
            story.append(Paragraph(", ".join(pontos_fortes), TextoResumo))
            story.append(Spacer(1, 10))

        if pontos_fracos:
            story.append(Paragraph("Pontos de atenção", TituloResumo))
            story.append(Spacer(1, 6))
            story.append(Paragraph(", ".join(pontos_fracos), TextoResumo))
            
    # Radar no final (se fornecido)
    if radar_path_final and os.path.exists(radar_path_final):
        story.append(PageBreak())
        story.append(Paragraph("Radar de Desempenho Geral", TituloResumo))
        story.append(Spacer(1, 10))
        story.append(Image(radar_path_final, width=15*cm, height=15*cm))
        story.append(Spacer(1, 10))


    doc.build(story)
    return caminho_saida


from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT

def adicionar_explicacao_final(elementos, perfil, pesos_utilizados):
    estilo_explicacao = ParagraphStyle(
        name='Explicação',
        fontSize=9,
        leading=12,
        alignment=TA_LEFT,
        spaceBefore=12,
        spaceAfter=6
    )

    explicacao_texto = f"""
    <b>Nota metodológica:</b> Este ranking foi gerado com base no desempenho estatístico dos jogadores nas métricas específicas atribuídas ao perfil <b>{perfil}</b>. 
    Cada métrica recebeu um peso conforme sua importância tática para essa função, e os dados foram normalizados por meio de Z-Score, possibilitando a comparação entre atletas 
    de diferentes ligas e contextos. Os valores finais refletem a frequência e a eficiência com que cada jogador executa ações relevantes para o perfil escolhido.
    """

    elementos.append(Spacer(1, 16))
    elementos.append(Paragraph(explicacao_texto, estilo_explicacao))

    # Gerar lista de métricas e pesos
    linhas_metricas = "<b>Métricas e pesos utilizados:</b><br/><br/>"
    for metrica, peso in pesos_utilizados.items():
        linhas_metricas += f"• {metrica}: <b>{peso}</b><br/>"

    elementos.append(Paragraph(linhas_metricas, estilo_explicacao))



from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
import tempfile
import pandas as pd
import os
from reportlab.lib.units import cm
from utilitarios.funcoes_pdf import adicionar_explicacao_final

def exportar_ranking_pdf(df, perfil, pesos_utilizados, top_n=20):
    caminho_temp = tempfile.mktemp(suffix=".pdf")

    # 🔽 Selecionar e ordenar colunas
    colunas_pdf = [
        'Jogador', 'Equipa', 'Posição', 'Idade', 'Minutos jogados:',
        'Valor de mercado', 'Contrato termina', 'Liga', 'Z-Score Ajustado'
    ]
    df_pdf = df[colunas_pdf].copy()
    df_pdf = df_pdf.sort_values(by='Z-Score Ajustado', ascending=False).head(top_n)

    # 🔽 Formatar 'Contrato termina' como Mês/Ano
    df_pdf['Contrato termina'] = pd.to_datetime(df_pdf['Contrato termina'], errors='coerce').dt.strftime('%b/%y')
    df_pdf['Contrato termina'] = df_pdf['Contrato termina'].fillna("")

    # 🔽 Renomear colunas
    df_pdf.rename(columns={
        'Posição': 'Pos.',
        'Minutos jogados:': 'Minutos',
        'Contrato termina': 'Fim Contrato',
        'Z-Score Ajustado': 'Z-Score'
    }, inplace=True)


    df_pdf['Valor de mercado'] = df_pdf['Valor de mercado'].apply(
    lambda x: "Não informado" if isinstance(x, str) and x.strip() == "€0" else x
    )

    # 🔽 Abreviar liga
    df_pdf['Liga'] = df_pdf['Liga'].apply(abreviar_liga)

    # 🔽 Criar documento PDF com margens laterais visíveis
    doc = SimpleDocTemplate(
        caminho_temp,
        pagesize=A4,
        leftMargin=1.0*cm,
        rightMargin=1.0*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )

    elementos = []

    # 🔽 Adicionar logo
    logo_path = os.path.join("assets", "logo.png")
    if os.path.exists(logo_path):
        elementos.append(Image(logo_path, width=100, height=100))
        elementos.append(Spacer(1, 12))

    # 🔽 Título
    estilo_titulo = getSampleStyleSheet()["Heading1"]
    estilo_titulo.alignment = TA_CENTER
    elementos.append(Paragraph(f"Ranking - Perfil: {perfil}", estilo_titulo))
    elementos.append(Spacer(1, 12))

    # 🔽 Construir tabela
    dados_tabela = [df_pdf.columns.tolist()] + df_pdf.values.tolist()
    tabela = Table(dados_tabela, repeatRows=1)

    estilo_tabela = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f60000')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
    ])

    # 🔽 Gradiente do Z-Score baseado no DataFrame completo
    if 'Z-Score Ajustado' in df.columns:
        valores_completos = df['Z-Score Ajustado'].tolist()
        minimo = min(valores_completos)
        maximo = max(valores_completos)
        intervalo = maximo - minimo if maximo != minimo else 1

        for i, valor in enumerate(df_pdf['Z-Score'].tolist(), start=1):
            intensidade = (valor - minimo) / intervalo
            cor = colors.linearlyInterpolatedColor(
                colors.HexColor('#d6f5d6'),  # verde claro
                colors.HexColor('#006400'),  # verde escuro
                0, 1, intensidade
            )
            estilo_tabela.add('BACKGROUND', (-1, i), (-1, i), cor)

    tabela.setStyle(estilo_tabela)
    elementos.append(tabela)

    # 🔽 Explicação metodológica ao final
    adicionar_explicacao_final(elementos, perfil, pesos_utilizados)

    doc.build(elementos)
    return caminho_temp