"""Helpers para gerar .docx da Carta de Servico no padrao SETDIG.

Concentra: Arial 12, hiperlinks azuis clicaveis (#0563C1), listas numeradas
com reinicio por bloco (via `numbered` context manager) e escrita final.
"""
from contextlib import contextmanager
from pathlib import Path

from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt

FONT = "Arial"
SIZE = 12
LINK_COLOR = "0563C1"

ROOT = Path(__file__).resolve().parent.parent.parent
SAIDA = ROOT / "exemplos" / "saida"


# ---------- fonte ----------

def _apply_font(rpr, size=SIZE):
    rFonts = rpr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rpr.append(rFonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rFonts.set(qn(attr), FONT)


def _set_run_font(run, bold=False, size=SIZE):
    run.font.name = FONT
    run.font.size = Pt(size)
    run.bold = bold
    _apply_font(run._element.get_or_add_rPr(), size=size)


# ---------- doc ----------

def nova_carta(titulo):
    doc = Document()
    style = doc.styles["Normal"]
    style.font.name = FONT
    style.font.size = Pt(SIZE)
    _apply_font(style.element.get_or_add_rPr())
    heading(doc, titulo, level=1)
    return doc


def salvar(doc, slug):
    out = SAIDA / slug / f"{slug}.docx"
    out.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(out))
    print(f"OK -> {out}")
    return out


# ---------- primitivas ----------

def heading(doc, texto, level=2):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run(texto)
    size = {1: 18, 2: 14, 3: 12}[level]
    _set_run_font(run, bold=True, size=size)
    return p


def para(doc, texto=""):
    p = doc.add_paragraph()
    if texto:
        run = p.add_run(texto)
        _set_run_font(run)
    return p


def _add_hyperlink(paragraph, url, text):
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
    color.set(qn("w:val"), LINK_COLOR)
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


def _fill(p, segments):
    for seg in segments:
        if seg[0] == "text":
            _, txt, bold = seg
            run = p.add_run(txt)
            _set_run_font(run, bold=bold)
        elif seg[0] == "link":
            _, url, label = seg
            _add_hyperlink(p, url, label)


def para_rich(doc, segments):
    p = doc.add_paragraph()
    _fill(p, segments)
    return p


def bullet(doc, segments, *, sub=False):
    p = doc.add_paragraph(style="List Bullet")
    if sub:
        p.paragraph_format.left_indent = Pt(36)
    _fill(p, segments)
    return p


# ---------- lista numerada com reinicio por bloco ----------

def _ensure_numbering(doc):
    """Garante que numbering.xml existe (criado sob demanda por python-docx)."""
    try:
        return doc.part.numbering_part
    except (AttributeError, KeyError):
        pass
    # Forcar criacao inserindo e removendo paragrafo temporario com List Number
    tmp = doc.add_paragraph(style="List Number")
    tmp._element.getparent().remove(tmp._element)
    return doc.part.numbering_part


def _first_abstract_num_id(numbering_el):
    for num in numbering_el.findall(qn("w:num")):
        ref = num.find(qn("w:abstractNumId"))
        if ref is not None:
            return ref.get(qn("w:val"))
    return "0"


def _mint_num_id(doc):
    """Cria novo w:num apontando pro abstractNumId do List Number, com startOverride=1."""
    numbering_part = _ensure_numbering(doc)
    numbering_el = numbering_part.element
    abstract_id = _first_abstract_num_id(numbering_el)

    existing_ids = [
        int(n.get(qn("w:numId")))
        for n in numbering_el.findall(qn("w:num"))
    ]
    new_id = (max(existing_ids) if existing_ids else 0) + 1

    new_num = OxmlElement("w:num")
    new_num.set(qn("w:numId"), str(new_id))

    abstract_ref = OxmlElement("w:abstractNumId")
    abstract_ref.set(qn("w:val"), abstract_id)
    new_num.append(abstract_ref)

    override = OxmlElement("w:lvlOverride")
    override.set(qn("w:ilvl"), "0")
    start = OxmlElement("w:startOverride")
    start.set(qn("w:val"), "1")
    override.append(start)
    new_num.append(override)

    numbering_el.append(new_num)
    return new_id


def _set_num_id(paragraph, num_id, ilvl=0):
    pPr = paragraph._element.get_or_add_pPr()
    numPr = pPr.find(qn("w:numPr"))
    if numPr is None:
        numPr = OxmlElement("w:numPr")
        pPr.append(numPr)
    for tag in ("w:ilvl", "w:numId"):
        existing = numPr.find(qn(tag))
        if existing is not None:
            numPr.remove(existing)
    ilvl_el = OxmlElement("w:ilvl")
    ilvl_el.set(qn("w:val"), str(ilvl))
    numPr.append(ilvl_el)
    numId_el = OxmlElement("w:numId")
    numId_el.set(qn("w:val"), str(num_id))
    numPr.append(numId_el)


@contextmanager
def numbered(doc):
    """Bloco de lista numerada com reinicio garantido em 1.

    Uso:
        with numbered(doc) as n:
            n([("text", "Item 1", False)])
            n([("text", "Item 2", False)])
    """
    num_id = _mint_num_id(doc)

    def add(segments, *, sub=False):
        p = doc.add_paragraph(style="List Number")
        _set_num_id(p, num_id, ilvl=1 if sub else 0)
        if sub:
            p.paragraph_format.left_indent = Pt(36)
        _fill(p, segments)
        return p

    yield add
