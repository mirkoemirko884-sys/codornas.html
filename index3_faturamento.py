# -*- coding: utf-8 -*-
import os
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

# IMPORTAÇÃO DOS MÓDULOS ANTERIORES
import index1_qr
import index2_layout

def gerar_boleto_final(valor_faturamento="R$ 13,00", descricao_produto="1 Cartela (30un)"):
    # Executa o Módulo 1 para garantir que a imagem do Pix exista
    caminho_qr = index1_qr.criar_imagem_qrcode()
    nome_arquivo = "boleto_mairipora_agro.pdf"
    
    COD_BANCO = "237-7"
    NOME_BANCO = "Bradesco"
    COR_BANCO = colors.HexColor('#cc092f') 
    
    data_doc_str = "23/09/2026"
    data_doc_obj = datetime.strptime(data_doc_str, "%d/%m/%Y")
    data_venc_obj = data_doc_obj + timedelta(days=21)
    data_venc_str = data_venc_obj.strftime("%d/%m/%Y")
    
    doc = SimpleDocTemplate(
        nome_arquivo, pagesize=letter,
        rightMargin=30, leftMargin=30, topMargin=20, bottomMargin=20,
        title="Mairiporã Agro - Faturamento V2"
    )
    
    story = []
    styles = getSampleStyleSheet()
    
    # Puxa os estilos configurados no Módulo 2
    estilos = index2_layout.criar_estilos_customizados(styles)
    
    story.append(Paragraph("<b>Mairiporã Agro - Sistema de Faturamento</b>", estilos['title']))
    story.append(Paragraph("Ambiente de Produção Local via VS Code & Python", estilos['sub']))
    story.append(Spacer(1, 8))
    
    # 1. Recibo do Sacado (Topo)
    dados_topo = [
        [Paragraph(f"<b>Beneficiário:</b> Mairiporã Agro ({NOME_BANCO})", estilos['normal']), Paragraph(f"<b>Vencimento:</b> {data_venc_str}", estilos['normal'])],
        [Paragraph(f"<b>Pagador:</b> Cliente de Teste - {descricao_produto}", estilos['normal']), Paragraph("<b>Número do Pedido:</b> #749201", estilos['normal'])],
        [Paragraph("<b>Espécie:</b> R$ (Real)", estilos['normal']), Paragraph(f"<b>Valor Cobrado:</b> {valor_faturamento}", estilos['bold'])]
    ]
    
    t_topo = Table(dados_topo, colWidths=[350, 200])
    t_topo.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_topo)
    story.append(Spacer(1, 8))
    
    story.append(Paragraph("- " * 45, estilos['sub']))
    story.append(Spacer(1, 8))
    
    # Injeta a imagem do QR Code gerada pelo Módulo 1
    img_qrcode = Image(caminho_qr, width=65, height=65)
    
    linha1 = [
        Paragraph(f"<b>{NOME_BANCO}<br/>{COD_BANCO}</b>", estilos['title']),
        img_qrcode,
        Paragraph("<b>23791.79001 01043.513184 91020.150008 7 98480000008500</b>", estilos['bold'])
    ]
    
    # Puxa o texto de observações montado no Módulo 2
    texto_obs = index2_layout.montar_texto_obs(descricao_produto, COR_BANCO)
    
    tabela_boleto_dados = [
        linha1,
        [Paragraph("<b>Local de Pagamento:</b> Qualquer Banco até o vencimento", estilos['normal']), "", Paragraph(f"<b>Vencimento:</b> {data_venc_str}", estilos['bold'])],
        [Paragraph("<b>Beneficiário:</b> Mairiporã Agro - JOSÉ CARLOS SUGUIMOTO", estilos['normal']), "", Paragraph("<b>Agência/Código:</b> 0449 / 0080619-6", estilos['normal'])],
        [Paragraph(f"<b>Data do Doc:</b> {data_doc_str}", estilos['normal']), Paragraph("<b>Nº Doc:</b> 749201", estilos['normal']), Paragraph("<b>Espécie Doc:</b> DM", estilos['normal'])],
        [Paragraph("<b>Uso do Banco:</b>", estilos['normal']), Paragraph("<b>Carteira:</b> 109", estilos['normal']), Paragraph("<b>Espécie:</b> R$", estilos['normal'])],
        [Paragraph("<b>Instruções:</b><br/>• Liberação imediata baseada na relação de confiança.<br/>• Processamento via Pix integrado.", estilos['normal']), "", Paragraph(f"<b>(=) Valor do Doc:</b> {valor_faturamento}", estilos['bold'])],
        [Paragraph(texto_obs, estilos['obs']), "", Paragraph("<b>(-) Descontos:</b>", estilos['normal'])],
        ["", "", Paragraph("<b>(+) Multa / Juros:</b>", estilos['normal'])],
        ["", "", Paragraph(f"<b>(=) Valor Cobrado:</b> {valor_faturamento}", estilos['bold'])]
    ]
    
    t_boleto = Table(tabela_boleto_dados, colWidths=[100, 80, 370])
    t_boleto.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ALIGN', (1,0), (1,0), 'CENTER'),
        ('VALIGN', (0,0), (-1,0), 'MIDDLE'),
        ('LINEBELOW', (0,0), (-1,0), 2, COR_BANCO),
        ('SPAN', (0,1), (1,1)),
        ('SPAN', (0,2), (1,2)),
        ('SPAN', (0,5), (1,5)),
        ('SPAN', (0,6), (1,8)),
        ('BOX', (0,1), (-1,-1), 1, colors.black),
        ('INNERGRID', (0,1), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('PADDING', (0,0), (-1,-1), 4),
        ('BACKGROUND', (2,1), (2,1), colors.HexColor('#f8fafc')),
        ('BACKGROUND', (2,8), (2,8), colors.HexColor('#f1f5f9')),
    ]))
    
    story.append(t_boleto)
    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>Obrigado por sua preferência e parceria com a Mairiporã Agro!</b>", estilos['agradece']))
    
    doc.build(story)
    print(f"✔️ Módulo 3 concluído: PDF '{nome_arquivo}' gerado com sucesso completo!")

if __name__ == "__main__":
    gerar_boleto_final()
