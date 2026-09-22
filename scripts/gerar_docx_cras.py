"""Gera .docx da carta 'Consultar endereços dos CRAS'."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.docx_carta import bullet, heading, nova_carta, numbered, para, para_rich, salvar

SLUG = "consultar-enderecos-cras"
PLAY = "https://play.google.com/store/apps/details?id=br.gov.ms.msapp"
APPSTORE = "https://apps.apple.com/br/app/ms-digital/id1482970942"

doc = nova_carta("Consultar endereços dos CRAS")

heading(doc, "O QUE É?")
para(doc,
    "Serviço on-line em que você consulta o endereço, telefone e e-mail dos Centros "
    "de Referência de Assistência Social (CRAS) do Estado de Mato Grosso do Sul. "
    "Você faz a busca pelo aplicativo MS Digital, escolhendo o município e a unidade desejada.")

heading(doc, "Exigências")
with numbered(doc) as n:
    n([
        ("text", "Aplicativo MS Digital instalado (", False),
        ("link", PLAY, "Google Play"),
        ("text", " / ", False),
        ("link", APPSTORE, "App Store"),
        ("text", ")", False),
    ])
    n([("text", "Conta gov.br autenticada ou CPF e senha", False)])

heading(doc, "Quem pode utilizar?")
para(doc, "Qualquer cidadão que precise localizar um CRAS em Mato Grosso do Sul.")

heading(doc, "Prazo")
para(doc, "Imediato")

heading(doc, "Custos")
para(doc, "Sem custos")

heading(doc, "Etapas")

para_rich(doc, [("text", "Pelo aplicativo MS Digital:", True)])
with numbered(doc) as n:
    n([
        ("text", "Baixe ", True),
        ("text", "o aplicativo MS Digital na ", False),
        ("link", PLAY, "Google Play"),
        ("text", " (Android) ou ", False),
        ("link", APPSTORE, "App Store"),
        ("text", " (iPhone).", False),
    ])
    n([("text", "Faça login ", True), ("text", "com sua conta gov.br ou com CPF e senha.", False)])
    n([("text", "Acesse ", True), ("text", "a categoria Assistência Social.", False)])
    n([("text", "Selecione ", True), ("text", "o serviço Endereços dos CRAS.", False)])
    n([("text", "Escolha ", True), ("text", "o município desejado.", False)])
    n([("text", "Selecione ", True), ("text", "o CRAS. A tela mostra telefone, e-mail e endereço da unidade.", False)])
    n([("text", "Toque ", True), ("text", "no telefone para ligar ou no endereço para abrir a localização no mapa.", False)])

heading(doc, "Outras Informações")

para_rich(doc, [("text", "Consulta alternativa pela internet:", True)])
bullet(doc, [
    ("link", "https://www.sead.ms.gov.br/fale-conosco/unidades/unidades-regionais/", "Unidades Regionais da SEAD"),
    ("text", " — lista completa das unidades e contatos no site oficial", False),
])

para_rich(doc, [
    ("text", "Órgão responsável: ", True),
    ("text", "Secretaria de Estado de Assistência Social — SEAD", False),
])

salvar(doc, SLUG)
