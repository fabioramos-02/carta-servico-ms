"""Gera .docx da carta 'Emitir Contracheque' em Arial 12 com hiperlinks clicaveis.

Uso:
    python scripts/gerar_docx_contracheque.py

Escreve em exemplos/saida/emitir-contracheque.docx.
"""
from pathlib import Path
from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "exemplos" / "saida" / "emitir-contracheque" / "emitir-contracheque.docx"

FONT = "Arial"
SIZE = 12

doc = Document()

style = doc.styles["Normal"]
style.font.name = FONT
style.font.size = Pt(SIZE)
rpr = style.element.get_or_add_rPr()
rfonts = rpr.find(qn("w:rFonts"))
if rfonts is None:
    rfonts = OxmlElement("w:rFonts")
    rpr.append(rfonts)
for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
    rfonts.set(qn(attr), FONT)


def set_run_font(run, bold=False, size=SIZE):
    run.font.name = FONT
    run.font.size = Pt(size)
    r = run._element
    rPr = r.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.append(rFonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rFonts.set(qn(attr), FONT)
    run.bold = bold


def add_hyperlink(paragraph, url, text):
    part = paragraph.part
    r_id = part.relate_to(
        url,
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
        is_external=True,
    )
    hyperlink = OxmlElement("w:hyperlink")
    hyperlink.set(qn("r:id"), r_id)

    new_run = OxmlElement("w:r")
    rPr = OxmlElement("w:rPr")

    rFonts = OxmlElement("w:rFonts")
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rFonts.set(qn(attr), FONT)
    rPr.append(rFonts)

    sz = OxmlElement("w:sz")
    sz.set(qn("w:val"), str(SIZE * 2))
    rPr.append(sz)

    color = OxmlElement("w:color")
    color.set(qn("w:val"), "0563C1")
    rPr.append(color)

    u = OxmlElement("w:u")
    u.set(qn("w:val"), "single")
    rPr.append(u)

    new_run.append(rPr)

    t = OxmlElement("w:t")
    t.text = text
    t.set(qn("xml:space"), "preserve")
    new_run.append(t)

    hyperlink.append(new_run)
    paragraph._p.append(hyperlink)
    return hyperlink


def add_heading(text, level=1):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run(text)
    size = {1: 18, 2: 14, 3: 12}[level]
    set_run_font(run, bold=True, size=size)
    return p


def add_para(text=""):
    p = doc.add_paragraph()
    if text:
        run = p.add_run(text)
        set_run_font(run)
    return p


def add_para_rich(segments):
    p = doc.add_paragraph()
    for seg in segments:
        if seg[0] == "text":
            _, txt, bold = seg
            run = p.add_run(txt)
            set_run_font(run, bold=bold)
        elif seg[0] == "link":
            _, url, label = seg
            add_hyperlink(p, url, label)
    return p


def add_bullet(segments, numbered=False, sub=False):
    style_name = "List Number" if numbered else "List Bullet"
    p = doc.add_paragraph(style=style_name)
    if sub:
        p.paragraph_format.left_indent = Pt(36)
    for seg in segments:
        if seg[0] == "text":
            _, txt, bold = seg
            run = p.add_run(txt)
            set_run_font(run, bold=bold)
        elif seg[0] == "link":
            _, url, label = seg
            add_hyperlink(p, url, label)
    return p


# =========== CONTEÚDO ===========

add_heading("Emitir Contracheque", 1)

add_heading("O QUE É?", 2)
add_para(
    "Serviço on-line em que o servidor público estadual consulta e baixa o demonstrativo "
    "mensal de pagamento (contracheque). Você acessa pelo aplicativo MS Digital ou pelo Portal "
    "do Servidor, no navegador. O contracheque fica disponível assim que a Secretaria de Estado "
    "de Administração — SAD fecha a folha de pagamento."
)

add_heading("Exigências", 2)
add_bullet([("text", "Matrícula funcional", False)], numbered=True)
add_bullet([
    ("text", "Senha de acesso ao ", False),
    ("link", "https://www.portaldoservidor.ms.gov.br/Entrar/Login", "Portal do Servidor"),
], numbered=True)
add_bullet([
    ("text", "Para usar pelo aplicativo MS Digital (", False),
    ("link", "https://play.google.com/store/apps/details?id=br.gov.ms.msapp", "Google Play"),
    ("text", " / ", False),
    ("link", "https://apps.apple.com/br/app/ms-digital/id1482970942", "App Store"),
    ("text", "): conta gov.br autenticada ou CPF e senha do Portal do Servidor", False),
], numbered=True)

add_heading("Quem pode utilizar?", 2)
add_para("Servidor público estadual com vínculo ativo no Governo de Mato Grosso do Sul.")

add_heading("Prazo", 2)
add_para("Imediato após o login.")

add_heading("Custos", 2)
add_para("Sem custo.")

add_heading("Etapas", 2)

add_para_rich([("text", "Pelo aplicativo MS Digital:", True)])
add_bullet([
    ("text", "Baixe ", True),
    ("text", "o aplicativo MS Digital na ", False),
    ("link", "https://play.google.com/store/apps/details?id=br.gov.ms.msapp", "Google Play"),
    ("text", " (Android) ou ", False),
    ("link", "https://apps.apple.com/br/app/ms-digital/id1482970942", "App Store"),
    ("text", " (iPhone).", False),
], numbered=True)
add_bullet([
    ("text", "Faça login ", True),
    ("text", "com sua conta gov.br ou com CPF e senha.", False),
], numbered=True)
add_bullet([
    ("text", "Selecione ", True),
    ("text", "a opção Servidor Público e, em seguida, Portal do Servidor.", False),
], numbered=True)
add_bullet([
    ("text", "Escolha ", True),
    ("text", "seu vínculo funcional na lista. Se o vínculo não aparecer, informe CPF e senha do Portal do Servidor para autenticar.", False),
], numbered=True)
add_bullet([
    ("text", "Toque ", True),
    ("text", "em Contracheque no menu.", False),
], numbered=True)
add_bullet([
    ("text", "Selecione ", True),
    ("text", "o ano e o mês que deseja consultar.", False),
], numbered=True)
add_bullet([
    ("text", "Toque ", True),
    ("text", "em Baixar PDF para salvar ou compartilhar o arquivo.", False),
], numbered=True)

add_para_rich([("text", "Pelo Portal do Servidor (navegador):", True)])
add_bullet([
    ("text", "Acesse ", True),
    ("text", "o ", False),
    ("link", "https://www.portaldoservidor.ms.gov.br/Entrar/Login", "Portal do Servidor"),
    ("text", ".", False),
], numbered=True)
add_bullet([
    ("text", "Informe ", True),
    ("text", "CPF, senha e resolva o desafio de verificação.", False),
], numbered=True)
add_bullet([
    ("text", "Clique ", True),
    ("text", "em Serviços e, no menu, escolha Dados Financeiros e depois Emissão de Contracheque.", False),
], numbered=True)
add_bullet([
    ("text", "Selecione ", True),
    ("text", "o ano e o mês desejados.", False),
], numbered=True)
add_bullet([
    ("text", "Baixe ", True),
    ("text", "ou imprima o PDF do contracheque.", False),
], numbered=True)

add_heading("Outras Informações", 2)

add_para_rich([("text", "Canais de atendimento:", True)])
add_bullet([
    ("text", "Portal: ", False),
    ("link", "https://www.portaldoservidor.ms.gov.br", "www.portaldoservidor.ms.gov.br"),
])
add_bullet([
    ("text", "Aplicativo MS Digital: ", False),
    ("link", "https://play.google.com/store/apps/details?id=br.gov.ms.msapp", "Google Play"),
    ("text", " / ", False),
    ("link", "https://apps.apple.com/br/app/ms-digital/id1482970942", "App Store"),
])
add_bullet([("text", "Telefone / e-mail SAD: [FALTA: canal de atendimento não informado no material]", False)])

add_para_rich([("text", "Esqueceu a senha?", True)])
add_bullet([
    ("link", "https://www.portaldoservidor.ms.gov.br/SenhaDeAcesso/EsqueciMinhaSenha", "Recuperar senha do Portal do Servidor"),
])

add_para_rich([("text", "Legislação:", True)])
add_bullet([
    ("link", "https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2017/lei/l13460.htm", "Lei Federal 13.460, de 26 de junho de 2017 — Código de Defesa do Usuário do Serviço Público"),
])
add_bullet([
    ("link", "https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2025/lei/l15263.htm", "Lei Federal 15.263, de 2025 — linguagem simples no serviço público"),
])
add_bullet([("text", "[VERIFICAR: Decreto Estadual 16.744/2026 (MS) — link oficial]", False)])
add_bullet([("text", "[FALTA: portaria SAD sobre contracheque digital, se houver]", False)])

add_para_rich([
    ("text", "Órgão responsável: ", True),
    ("text", "Secretaria de Estado de Administração — SAD", False),
])

OUT.parent.mkdir(parents=True, exist_ok=True)
doc.save(str(OUT))
print(f"OK -> {OUT}")
