"""Gera .docx da carta 'Emitir Contracheque'."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.docx_carta import bullet, heading, nova_carta, numbered, para, para_rich, salvar

SLUG = "emitir-contracheque"
PORTAL = "https://www.portaldoservidor.ms.gov.br/Entrar/Login"
PLAY = "https://play.google.com/store/apps/details?id=br.gov.ms.msapp"
APPSTORE = "https://apps.apple.com/br/app/ms-digital/id1482970942"

doc = nova_carta("Emitir Contracheque")

heading(doc, "O QUE É?")
para(doc,
    "Serviço on-line em que o servidor público estadual consulta e baixa o demonstrativo "
    "mensal de pagamento (contracheque). Você acessa pelo aplicativo MS Digital ou pelo Portal "
    "do Servidor, no navegador.")

heading(doc, "Exigências")
with numbered(doc) as n:
    n([("text", "Matrícula funcional", False)])
    n([("text", "Senha de acesso ao ", False), ("link", PORTAL, "Portal do Servidor")])
    n([
        ("text", "Para usar pelo aplicativo MS Digital (", False),
        ("link", PLAY, "Google Play"),
        ("text", " / ", False),
        ("link", APPSTORE, "App Store"),
        ("text", "): conta gov.br autenticada ou CPF e senha do Portal do Servidor", False),
    ])

heading(doc, "Quem pode utilizar?")
para(doc, "Servidor público estadual com vínculo ativo no Governo de Mato Grosso do Sul.")

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
    n([("text", "Selecione ", True), ("text", "a opção Servidor Público e, em seguida, Portal do Servidor.", False)])
    n([("text", "Escolha ", True), ("text", "seu vínculo funcional na lista. Se o vínculo não aparecer, informe CPF e senha do Portal do Servidor para autenticar.", False)])
    n([("text", "Toque ", True), ("text", "em Contracheque no menu.", False)])
    n([("text", "Selecione ", True), ("text", "o ano e o mês que deseja consultar.", False)])
    n([("text", "Toque ", True), ("text", "em Baixar PDF para salvar ou compartilhar o arquivo.", False)])

para_rich(doc, [("text", "Pelo Portal do Servidor (navegador):", True)])
with numbered(doc) as n:
    n([
        ("text", "Acesse ", True),
        ("text", "o ", False),
        ("link", PORTAL, "Portal do Servidor"),
        ("text", ".", False),
    ])
    n([("text", "Informe ", True), ("text", "CPF, senha e resolva o desafio de verificação.", False)])
    n([("text", "Clique ", True), ("text", "em Serviços e, no menu, escolha Dados Financeiros e depois Emissão de Contracheque.", False)])
    n([("text", "Selecione ", True), ("text", "o ano e o mês desejados.", False)])
    n([("text", "Baixe ", True), ("text", "ou imprima o PDF do contracheque.", False)])

heading(doc, "Outras Informações")

para_rich(doc, [("text", "Canais de atendimento:", True)])
bullet(doc, [
    ("text", "Portal: ", False),
    ("link", "https://www.portaldoservidor.ms.gov.br", "www.portaldoservidor.ms.gov.br"),
])
bullet(doc, [
    ("text", "Aplicativo MS Digital: ", False),
    ("link", PLAY, "Google Play"),
    ("text", " / ", False),
    ("link", APPSTORE, "App Store"),
])
para_rich(doc, [("text", "Esqueceu a senha?", True)])
bullet(doc, [
    ("link", "https://www.portaldoservidor.ms.gov.br/SenhaDeAcesso/EsqueciMinhaSenha",
     "Recuperar senha do Portal do Servidor"),
])

salvar(doc, SLUG)
