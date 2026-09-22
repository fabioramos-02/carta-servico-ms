"""Gera .docx da Carta CID (Fundesporte)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.docx_carta import bullet, heading, nova_carta, numbered, para, para_rich, salvar

SLUG = "carteira-identificacao-desportiva-cid"
PLAY = "https://play.google.com/store/apps/details?id=br.gov.ms.msapp"
APPSTORE = "https://apps.apple.com/br/app/ms-digital/id1482970942"

doc = nova_carta("Consultar Carteira de Identificação Desportiva (CID)")

heading(doc, "O QUE É?")
para(doc,
    "Documento digital que identifica atletas e técnicos bolsistas da Fundação de Desporto e Lazer "
    "de Mato Grosso do Sul (Fundesporte). A CID também pode dar direito a descontos em estabelecimentos "
    "parceiros. A consulta é feita pelo aplicativo MS Digital.")

heading(doc, "Exigências")
with numbered(doc) as n:
    n([("text", "CPF (Cadastro de Pessoas Físicas)", False)])
    n([("text", "Código de inscrição do beneficiário na Fundesporte", False)])
    n([
        ("text", "Aplicativo MS Digital instalado (", False),
        ("link", PLAY, "Google Play"),
        ("text", " / ", False),
        ("link", APPSTORE, "App Store"),
        ("text", ")", False),
    ])

heading(doc, "Quem pode utilizar?")
para(doc, "Atletas e técnicos bolsistas da Fundesporte habilitados a receber a CID.")

heading(doc, "Prazo")
para(doc, "Imediato")

heading(doc, "Custos")
para(doc, "Sem custos")

heading(doc, "Etapas")
with numbered(doc) as n:
    n([
        ("text", "Baixe ", True),
        ("text", "o aplicativo MS Digital na ", False),
        ("link", PLAY, "Google Play"),
        ("text", " (Android) ou ", False),
        ("link", APPSTORE, "App Store"),
        ("text", " (iPhone).", False),
    ])
    n([
        ("text", "Abra ", True),
        ("text", "o aplicativo e localize o ícone ", False),
        ("text", "Cultura e Esporte", True),
        ("text", ".", False),
    ])
    n([
        ("text", "Selecione ", True),
        ("text", "a opção ", False),
        ("text", "Carteira de Identificação Desportiva", True),
        ("text", ".", False),
    ])
    n([("text", "Informe ", True), ("text", "seu CPF e o código de inscrição do beneficiário.", False)])
    n([("text", "Salve ", True), ("text", "os dados no aparelho para agilizar consultas futuras, se quiser.", False)])
    n([("text", "Apresente ", True), ("text", "a CID no estabelecimento parceiro para usar os benefícios.", False)])

heading(doc, "Outras Informações")

para_rich(doc, [("text", "Versão física:", True)])
bullet(doc, [
    ("text", "A carteira impressa é entregue junto ao kit dos programas Bolsa Atleta e Bolsa Técnico. "
             "[VERIFICAR: material só cita entrega em julho/2021; confirmar se a prática segue nas edições atuais]", False),
])

para_rich(doc, [("text", "Estabelecimentos parceiros:", True)])
bullet(doc, [("text", "A lista de parceiros e descontos deve ser consultada nos canais oficiais da Fundesporte.", False)])

para_rich(doc, [("text", "Canais de atendimento:", True)])
bullet(doc, [
    ("text", "Site da Fundesporte: ", False),
    ("link", "https://www.fundesporte.ms.gov.br", "www.fundesporte.ms.gov.br"),
])
bullet(doc, [("text", "[FALTA: telefone, e-mail e endereço de atendimento presencial da Fundesporte]", False)])

para_rich(doc, [("text", "Legislação:", True)])
bullet(doc, [
    ("text", "Decreto Estadual nº 14.802, de 17 de agosto de 2017 — regulamenta a política de parcerias "
             "com empresas privadas para concessão de descontos.", False),
])

para_rich(doc, [
    ("text", "Órgão responsável: ", True),
    ("text", "Fundação de Desporto e Lazer de Mato Grosso do Sul (Fundesporte).", False),
])

salvar(doc, SLUG)
