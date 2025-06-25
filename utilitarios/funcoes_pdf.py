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

    doc.build(story)
    return caminho_saida
