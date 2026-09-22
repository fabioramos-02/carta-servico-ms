"""Gera .docx da carta 'Cartão de Visitante do Sistema Prisional' (AGEPEN)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.docx_carta import bullet, heading, nova_carta, numbered, para, para_rich, salvar

SLUG = "cartao-visitante-sistema-prisional"

DECL_RES = "https://www.agepen.ms.gov.br/wp-content/uploads/2026/01/DECLARACAO-DE-RESIDENCIA.pdf"
DECL_VIN = "https://www.agepen.ms.gov.br/wp-content/uploads/2026/01/DECLARACAO-DE-VINCULO-AFETIVO-PARA-FINS-DE-VISITACAO.pdf"
TERMO_MENOR = "https://www.agepen.ms.gov.br/wp-content/uploads/2026/01/TERMO-DE-RESPONSABILIDADE-DE-MENORES.pdf"
CERT_FED = "https://certidao-unificada.cjf.jus.br/#/solicitacao-certidao"
CERT_TJMS = "https://www5.tjms.jus.br/servicos/certidoes/"
VIDEO_CONJ = "https://www.agepen.ms.gov.br/wp-content/uploads/2025/11/VIDEO-CONJUGES.mp4"
VIDEO_DEP = "https://www.agepen.ms.gov.br/wp-content/uploads/2025/11/VIDEO-DEPENDENTES.mp4"
VIDEO_PAIS = "https://www.agepen.ms.gov.br/wp-content/uploads/2025/11/VIDEO-PAIS-E-IRMAOS.mp4"
SIAPEN = "https://www.siapen.ms.gov.br/visitante/"
SIAPEN_CANAL = "https://www.siapen.ms.gov.br/visitante"
AGEPEN = "https://www.agepen.ms.gov.br"
TUTORIAL = "https://www.agepen.ms.gov.br/wp-content/uploads/2025/09/TUTORIAL-REQUERIMENTO-DE-Cartao-Visitante-REQUERENTE-Versao-1.1-1.pdf"
LEP = "https://www.planalto.gov.br/ccivil_03/leis/l7210.htm"
DEC_12131 = "https://aacpdappls.net.ms.gov.br/appls/legislacao/secoge/govato.nsf/1b758e65922af3e904256b220050342a/14b3cf561af32e22042571c30049012b?OpenDocument"
DEC_12140 = DEC_12131
PORTARIA = "https://www.agepen.ms.gov.br/wp-content/uploads/2022/08/Portaria-Normativa-Visitas-DO10912_11_08_2022.pdf"

doc = nova_carta("Solicitar Carteira de Visitante do Sistema Prisional")

heading(doc, "O QUE É?")
para(doc,
    "Documento obrigatório para visitar pessoas presas nas unidades prisionais de Mato Grosso do Sul. "
    "A emissão é feita on-line pela AGEPEN (Agência Estadual de Administração do Sistema Penitenciário), "
    "sem precisar ir presencialmente. Quem não conseguir pedir on-line pode procurar o Patronato Penitenciário "
    "ou a unidade prisional da cidade.")

heading(doc, "Exigências")

para_rich(doc, [("text", "Visitante com 18 anos ou mais:", True)])
with numbered(doc) as n:
    n([("text", "Foto 3x4 com fundo branco e data (até 120 dias antes do pedido)", False)])
    n([("text", "CPF (Cadastro de Pessoas Físicas)", False)])
    n([("text", "Documento oficial com foto (RG, CNH, passaporte ou carteira profissional)", False)])
    n([
        ("text", "Comprovante de residência recente (até 90 dias) em seu nome. Se não estiver em seu nome, use a ", False),
        ("link", DECL_RES, "declaração de residência"),
    ])
    n([("text", "Certidão de casamento (se for cônjuge)", False)])
    n([
        ("text", "Escritura Pública de União Estável ou ", False),
        ("link", DECL_VIN, "Declaração de Vínculo Afetivo"),
        ("text", " com firma reconhecida (se for companheiro ou companheira)", False),
    ])
    n([("link", CERT_FED, "Certidão Criminal Federal")])
    n([
        ("link", CERT_TJMS, "Certidão Criminal Estadual do TJMS"),
        ("text", ". Se você morou em outro estado nos últimos 5 anos, pegue também no Tribunal de Justiça daquele estado.", False),
    ])

para_rich(doc, [("text", "Visitante entre 12 e 17 anos (o responsável legal faz o pedido):", True)])
with numbered(doc) as n:
    n([("text", "Foto 3x4 com fundo branco e data (até 120 dias antes)", False)])
    n([("text", "CPF", False)])
    n([("text", "Documento oficial com foto", False)])
    n([("text", "Comprovante de residência recente (até 90 dias)", False)])
    n([("link", TERMO_MENOR, "Termo de responsabilidade de menores")])

para_rich(doc, [("text", "Visitante menor de 12 anos (o responsável legal pede a inclusão no rol de visitantes):", True)])
with numbered(doc) as n:
    n([("text", "Certidão de nascimento ou RG", False)])
    n([("text", "CPF", False)])
    n([("link", TERMO_MENOR, "Termo de responsabilidade de menores")])

para_rich(doc, [
    ("text", "Importante: ", True),
    ("text", "a assinatura da pessoa presa na Declaração de Vínculo Afetivo é colhida pelo Patronato Penitenciário e conferida pelo Serviço Social ou pelo Diretor da unidade onde ela cumpre pena.", False),
])
para(doc,
    "Pessoas com 16 ou 17 anos podem pedir sem responsável apenas se forem cônjuge ou companheiro em casamento ou união estável já registrados.")

heading(doc, "Quem pode utilizar?")
para(doc,
    "Você pode visitar se for parente até o segundo grau da pessoa presa: pai, mãe, avós, filhos, netos e irmãos. "
    "Cônjuges e companheiros também podem. Amigos só são autorizados quando a pessoa presa não tem visita de "
    "cônjuge, companheiro ou parente.")

heading(doc, "Prazo")
para(doc, "30 dias úteis.")

heading(doc, "Custos")
para(doc, "Sem custos")

heading(doc, "Etapas")

with numbered(doc) as n:
    n([("text", "Assista ", True), ("text", "aos vídeos informativos conforme seu vínculo:", False)])
    n([("link", VIDEO_CONJ, "Cônjuges e companheiros")], sub=True)
    n([("link", VIDEO_DEP, "Dependentes")], sub=True)
    n([("link", VIDEO_PAIS, "Pais, mães, irmãos e outros")], sub=True)
    n([
        ("text", "Acesse ", True),
        ("text", "o ", False),
        ("link", SIAPEN, "SIAPEN — Sistema Integrado de Administração do Sistema Penitenciário"),
        ("text", " e clique em Novo.", False),
    ])
    n([("text", "Preencha ", True), ("text", "a aba Formulário com:", False)])
    n([("text", "Tipo de emissão (primeira via ou renovação)", False)], sub=True)
    n([("text", "Nacionalidade", False)], sub=True)
    n([("text", "Seus dados: CPF, nome completo, data de nascimento, telefone e e-mail válido (a resposta vai por e-mail)", False)], sub=True)
    n([("text", "Dados da pessoa presa: nome completo, unidade prisional, cidade e grau de parentesco. Repita para cada pessoa que for visitar.", False)], sub=True)
    n([("text", "Anexe ", True), ("text", "cada documento na lista que aparece ao clicar na seta. O sistema avisa se faltar algum.", False)])
    n([("text", "Envie ", True), ("text", "o cadastro clicando em ENVIAR CADASTRO e depois em SIM para confirmar. Guarde o número de protocolo — você usa ele para acompanhar o pedido no SIAPEN.", False)])
    n([("text", "Baixe e imprima ", True), ("text", "o cartão colorido quando ficar pronto e plastifique. O cartão traz foto, dados pessoais, código de barras e QR Code. Só o cartão impresso é aceito na entrada — celular não vale.", False)])

heading(doc, "Outras Informações")

para_rich(doc, [("text", "Canais de atendimento:", True)])
bullet(doc, [("text", "Site: ", False), ("link", AGEPEN, "www.agepen.ms.gov.br")])
bullet(doc, [("text", "Sistema: ", False), ("link", SIAPEN_CANAL, "www.siapen.ms.gov.br/visitante")])
bullet(doc, [("text", "Presencial: Patronatos Penitenciários ou, onde não houver, a unidade prisional da cidade", False)])
bullet(doc, [("text", "WhatsApp: [FALTA: número não informado no material]", False)])

para_rich(doc, [("text", "Tutorial:", True)])
bullet(doc, [("link", TUTORIAL, "Como preencher o requerimento do Cartão de Visitante")])

para_rich(doc, [("text", "Legislação:", True)])
bullet(doc, [("link", LEP, "Lei Federal 7.210, de 11 de julho de 1984 — Lei de Execução Penal")])
bullet(doc, [("link", DEC_12131, "Decreto 12.131, de 4 de agosto de 2006 — cria a Unidade Assistencial Patronato AGEPEN")])
bullet(doc, [("link", DEC_12140, "Decreto 12.140, de 17 de agosto de 2006 — regimento básico das unidades prisionais de MS")])
bullet(doc, [("link", PORTARIA, "Portaria Normativa AGEPEN 50, de 9 de agosto de 2022 — disciplina o direito de visita")])

para_rich(doc, [
    ("text", "Órgão responsável: ", True),
    ("text", "Agência Estadual de Administração do Sistema Penitenciário — AGEPEN", False),
])

salvar(doc, SLUG)
