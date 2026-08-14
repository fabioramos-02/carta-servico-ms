"""Gera .docx da carta de servico em Arial 12 com hiperlinks clicaveis."""
from docx import Document
from docx.shared import Pt, RGBColor
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

OUT = r"C:\Users\framos\Documents\SETDIG\2026\Projetos\exemplo-carta-de-servico\carta-cartao-visitante-sistema-prisional.docx"

FONT = "Arial"
SIZE = 12

doc = Document()

# Estilo default Arial 12 em todo o documento
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
    """Adiciona hyperlink clicavel azul sublinhado, Arial 12."""
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
    """segments = [(tipo, ...)]. tipos: ('text', str, bold), ('link', url, label)."""
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


# =========== CONTEUDO ===========

add_heading("Solicitar Carteira de Visitante do Sistema Prisional", 1)

add_heading("O QUE E?", 2)
add_para(
    "Documento obrigatorio para visitar pessoas presas nas unidades prisionais de Mato Grosso do Sul. "
    "A emissao e feita on-line pela AGEPEN (Agencia Estadual de Administracao do Sistema Penitenciario), "
    "sem precisar ir presencialmente. Quem nao conseguir pedir on-line pode procurar o Patronato Penitenciario "
    "ou a unidade prisional da cidade."
)

# Reescrever com acentos corretos - refazendo
# NOTE: vou remover paragrafo acima e reescrever tudo com acentuacao
# (limpo o body xml)
# Actually python-docx: mais simples reescrever
# Rebuild:
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

add_heading("Solicitar Carteira de Visitante do Sistema Prisional", 1)

add_heading("O QUE É?", 2)
add_para(
    "Documento obrigatório para visitar pessoas presas nas unidades prisionais de Mato Grosso do Sul. "
    "A emissão é feita on-line pela AGEPEN (Agência Estadual de Administração do Sistema Penitenciário), "
    "sem precisar ir presencialmente. Quem não conseguir pedir on-line pode procurar o Patronato Penitenciário "
    "ou a unidade prisional da cidade."
)

add_heading("Exigências", 2)

add_para_rich([("text", "Visitante com 18 anos ou mais:", True)])
add_bullet([("text", "Foto 3x4 com fundo branco e data (até 120 dias antes do pedido)", False)], numbered=True)
add_bullet([("text", "CPF (Cadastro de Pessoas Físicas)", False)], numbered=True)
add_bullet([("text", "Documento oficial com foto (RG, CNH, passaporte ou carteira profissional)", False)], numbered=True)
add_bullet([
    ("text", "Comprovante de residência recente (até 90 dias) em seu nome. Se não estiver em seu nome, use a ", False),
    ("link", "https://www.agepen.ms.gov.br/wp-content/uploads/2026/01/DECLARACAO-DE-RESIDENCIA.pdf", "declaração de residência"),
], numbered=True)
add_bullet([("text", "Certidão de casamento (se for cônjuge)", False)], numbered=True)
add_bullet([
    ("text", "Escritura Pública de União Estável ou ", False),
    ("link", "https://www.agepen.ms.gov.br/wp-content/uploads/2026/01/DECLARACAO-DE-VINCULO-AFETIVO-PARA-FINS-DE-VISITACAO.pdf", "Declaração de Vínculo Afetivo"),
    ("text", " com firma reconhecida (se for companheiro ou companheira)", False),
], numbered=True)
add_bullet([
    ("link", "https://certidao-unificada.cjf.jus.br/#/solicitacao-certidao", "Certidão Criminal Federal"),
], numbered=True)
add_bullet([
    ("link", "https://www5.tjms.jus.br/servicos/certidoes/", "Certidão Criminal Estadual do TJMS"),
    ("text", ". Se você morou em outro estado nos últimos 5 anos, pegue também no Tribunal de Justiça daquele estado.", False),
], numbered=True)

add_para_rich([("text", "Visitante entre 12 e 17 anos (o responsável legal faz o pedido):", True)])
add_bullet([("text", "Foto 3x4 com fundo branco e data (até 120 dias antes)", False)], numbered=True)
add_bullet([("text", "CPF", False)], numbered=True)
add_bullet([("text", "Documento oficial com foto", False)], numbered=True)
add_bullet([("text", "Comprovante de residência recente (até 90 dias)", False)], numbered=True)
add_bullet([
    ("link", "https://www.agepen.ms.gov.br/wp-content/uploads/2026/01/TERMO-DE-RESPONSABILIDADE-DE-MENORES.pdf", "Termo de responsabilidade de menores"),
], numbered=True)

add_para_rich([("text", "Visitante menor de 12 anos (o responsável legal pede a inclusão no rol de visitantes):", True)])
add_bullet([("text", "Certidão de nascimento ou RG", False)], numbered=True)
add_bullet([("text", "CPF", False)], numbered=True)
add_bullet([
    ("link", "https://www.agepen.ms.gov.br/wp-content/uploads/2026/01/TERMO-DE-RESPONSABILIDADE-DE-MENORES.pdf", "Termo de responsabilidade de menores"),
], numbered=True)

add_para_rich([
    ("text", "Importante: ", True),
    ("text", "a assinatura da pessoa presa na Declaração de Vínculo Afetivo é colhida pelo Patronato Penitenciário e conferida pelo Serviço Social ou pelo Diretor da unidade onde ela cumpre pena.", False),
])
add_para(
    "Pessoas com 16 ou 17 anos podem pedir sem responsável apenas se forem cônjuge ou companheiro em casamento ou união estável já registrados."
)

add_heading("Quem pode utilizar?", 2)
add_para(
    "Você pode visitar se for parente até o segundo grau da pessoa presa: pai, mãe, avós, filhos, netos e irmãos. "
    "Cônjuges e companheiros também podem. Amigos só são autorizados quando a pessoa presa não tem visita de "
    "cônjuge, companheiro ou parente."
)

add_heading("Prazo", 2)
add_para("30 dias úteis.")

add_heading("Custos", 2)
add_para("Gratuito.")

add_heading("Etapas", 2)

add_bullet([
    ("text", "Assista ", True),
    ("text", "aos vídeos informativos conforme seu vínculo:", False),
], numbered=True)
add_bullet([("link", "https://www.agepen.ms.gov.br/wp-content/uploads/2025/11/VIDEO-CONJUGES.mp4", "Cônjuges e companheiros")], sub=True)
add_bullet([("link", "https://www.agepen.ms.gov.br/wp-content/uploads/2025/11/VIDEO-DEPENDENTES.mp4", "Dependentes")], sub=True)
add_bullet([("link", "https://www.agepen.ms.gov.br/wp-content/uploads/2025/11/VIDEO-PAIS-E-IRMAOS.mp4", "Pais, mães, irmãos e outros")], sub=True)

add_bullet([
    ("text", "Acesse ", True),
    ("text", "o ", False),
    ("link", "https://www.siapen.ms.gov.br/visitante/", "SIAPEN — Sistema Integrado de Administração do Sistema Penitenciário"),
    ("text", " e clique em Novo.", False),
], numbered=True)

add_bullet([
    ("text", "Preencha ", True),
    ("text", "a aba Formulário com:", False),
], numbered=True)
add_bullet([("text", "Tipo de emissão (primeira via ou renovação)", False)], sub=True)
add_bullet([("text", "Nacionalidade", False)], sub=True)
add_bullet([("text", "Seus dados: CPF, nome completo, data de nascimento, telefone e e-mail válido (a resposta vai por e-mail)", False)], sub=True)
add_bullet([("text", "Dados da pessoa presa: nome completo, unidade prisional, cidade e grau de parentesco. Repita para cada pessoa que for visitar.", False)], sub=True)

add_bullet([
    ("text", "Anexe ", True),
    ("text", "cada documento na lista que aparece ao clicar na seta. O sistema avisa se faltar algum.", False),
], numbered=True)

add_bullet([
    ("text", "Envie ", True),
    ("text", "o cadastro clicando em ENVIAR CADASTRO e depois em SIM para confirmar. Guarde o número de protocolo — você usa ele para acompanhar o pedido no SIAPEN.", False),
], numbered=True)

add_bullet([
    ("text", "Baixe e imprima ", True),
    ("text", "o cartão colorido quando ficar pronto e plastifique. O cartão traz foto, dados pessoais, código de barras e QR Code. Só o cartão impresso é aceito na entrada — celular não vale.", False),
], numbered=True)

add_heading("Outras Informações", 2)

add_para_rich([("text", "Canais de atendimento:", True)])
add_bullet([
    ("text", "Site: ", False),
    ("link", "https://www.agepen.ms.gov.br", "www.agepen.ms.gov.br"),
])
add_bullet([
    ("text", "Sistema: ", False),
    ("link", "https://www.siapen.ms.gov.br/visitante", "www.siapen.ms.gov.br/visitante"),
])
add_bullet([("text", "Presencial: Patronatos Penitenciários ou, onde não houver, a unidade prisional da cidade", False)])
add_bullet([("text", "WhatsApp: [FALTA: número não informado no material]", False)])

add_para_rich([("text", "Tutorial:", True)])
add_bullet([
    ("link", "https://www.agepen.ms.gov.br/wp-content/uploads/2025/09/TUTORIAL-REQUERIMENTO-DE-Cartao-Visitante-REQUERENTE-Versao-1.1-1.pdf", "Como preencher o requerimento do Cartão de Visitante"),
])

add_para_rich([("text", "Legislação:", True)])
add_bullet([
    ("link", "https://www.planalto.gov.br/ccivil_03/leis/l7210.htm", "Lei Federal 7.210, de 11 de julho de 1984 — Lei de Execução Penal"),
])
add_bullet([
    ("link", "https://aacpdappls.net.ms.gov.br/appls/legislacao/secoge/govato.nsf/1b758e65922af3e904256b220050342a/14b3cf561af32e22042571c30049012b?OpenDocument", "Decreto 12.131, de 4 de agosto de 2006 — cria a Unidade Assistencial Patronato AGEPEN"),
])
add_bullet([
    ("link", "https://aacpdappls.net.ms.gov.br/appls/legislacao/secoge/govato.nsf/1b758e65922af3e904256b220050342a/14b3cf561af32e22042571c30049012b?OpenDocument", "Decreto 12.140, de 17 de agosto de 2006 — regimento básico das unidades prisionais de MS"),
])
add_bullet([
    ("link", "https://www.agepen.ms.gov.br/wp-content/uploads/2022/08/Portaria-Normativa-Visitas-DO10912_11_08_2022.pdf", "Portaria Normativa AGEPEN 50, de 9 de agosto de 2022 — disciplina o direito de visita"),
])

add_para_rich([
    ("text", "Órgão responsável: ", True),
    ("text", "Agência Estadual de Administração do Sistema Penitenciário — AGEPEN", False),
])

doc.save(OUT)
print(f"OK -> {OUT}")
