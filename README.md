# Agente Construtor de Carta de Serviço — Padrão MS

Agente de IA para Claude Code que transforma material bruto sobre um serviço público estadual (normativas, tutoriais, formulários) em uma **Carta de Serviço** no padrão de Mato Grosso do Sul, escrita em **linguagem simples**.

Base legal: **Lei Federal 15.263/2025** (linguagem simples), **Decreto Estadual 16.744/2026 (MS)**, **Lei Federal 13.460/2017** (Código de Defesa do Usuário do Serviço Público).

---

## Estrutura do repositório

```
.
├── agents/
│   └── carta-servico-ms.md              # Subagent Claude Code
├── exemplos/
│   ├── entrada/                         # Material bruto (uma pasta por serviço)
│   │   ├── cartao-visitante-sistema-prisional/
│   │   │   └── cartao-visitante-sistema-prisional.md
│   │   └── emitir-contracheque/
│   │       └── emitir-contracheque.md
│   └── saida/                           # Carta refatorada + docx (uma pasta por serviço)
│       ├── cartao-visitante-sistema-prisional/
│       │   ├── cartao-visitante-sistema-prisional.md
│       │   └── cartao-visitante-sistema-prisional.docx
│       └── emitir-contracheque/
│           ├── emitir-contracheque.md
│           └── emitir-contracheque.docx
├── manual/
│   └── Manual_de_Carta_de_Servicos.pdf  # Referência metodológica (Gov Acre)
├── scripts/
│   ├── gerar_docx.py                    # Conversor docx AGEPEN (Arial 12, hiperlinks)
│   └── gerar_docx_contracheque.py       # Conversor docx SAD Contracheque
├── CLAUDE.md                            # Instruções do projeto para Claude Code
└── README.md
```

---

## O que o agente faz

Recebe material bruto (texto colado, PDF transcrito, e-mail) e devolve **markdown pronto para colar no portal** com as 8 seções obrigatórias:

1. **Título** — verbo no infinitivo + objeto direto
2. **O QUE É?** — 2 a 4 frases
3. **Exigências** — documentos e condições em lista
4. **Quem pode utilizar?** — público-alvo em 1 a 3 frases
5. **Prazo** — número + unidade
6. **Custos** — "Sem custo" ou valor + forma de pagamento
7. **Etapas** — passo a passo numerado, verbos no imperativo
8. **Outras Informações** — canais, tutoriais, legislação, órgão responsável

Aplica linguagem simples: frases ≤20 palavras, voz ativa, "você" (nunca "requerente"), substituições léxicas automáticas, siglas expandidas na 1ª ocorrência.

Marca lacunas com `[FALTA: ...]` — **não inventa informação**.

---

## Como usar

### 1. Instalar o agente no Claude Code

Copie `agents/carta-servico-ms.md` para o diretório de agentes:

```powershell
Copy-Item agents/carta-servico-ms.md $env:USERPROFILE\.claude\agents\
```

Reinicie a sessão do Claude Code.

### 2. Rodar o agente

Cole o material bruto e peça:

> Cria a carta de serviço desse material: [cola texto]

Ou invoque explicitamente:

```
Agent(subagent_type="carta-servico-ms")
```

O agente devolve:
- **Bloco 1** — carta em markdown pronta para o portal
- **Bloco 2** — diagnóstico com lacunas encontradas, substituições feitas e próximos passos

### 3. Gerar .docx (opcional)

O script `scripts/gerar_docx.py` converte a carta em `.docx` com **Arial 12** e **hiperlinks clicáveis**:

```powershell
python scripts/gerar_docx.py
```

Requisito: `pip install python-docx`.

O script atual está parametrizado com o exemplo AGEPEN — adapte o conteúdo para outros serviços ou generalize para ler o markdown de entrada dinamicamente.

---

## Convenção de pastas

Cada serviço fica em **pasta própria** dentro de `entrada/` e `saida/`:

```
exemplos/entrada/{slug-servico}/{slug-servico}.md
exemplos/saida/{slug-servico}/{slug-servico}.md
exemplos/saida/{slug-servico}/{slug-servico}.docx
```

Assim, prints, PDFs de referência e outros anexos do serviço ficam junto do `.md`, sem poluir a raiz.

## Exemplos incluídos

**1. Solicitar Carteira de Visitante do Sistema Prisional (AGEPEN MS)**
- Entrada: `exemplos/entrada/cartao-visitante-sistema-prisional/cartao-visitante-sistema-prisional.md`
- Saída: `exemplos/saida/cartao-visitante-sistema-prisional/cartao-visitante-sistema-prisional.md` (+ `.docx`)

**2. Emitir Contracheque (SAD MS)**
- Entrada: `exemplos/entrada/emitir-contracheque/emitir-contracheque.md`
- Saída: `exemplos/saida/emitir-contracheque/emitir-contracheque.md` (+ `.docx`)
- Piloto do padrão de dois canais (App MS Digital + Portal do Servidor). Replicável para os outros 6 serviços SAD.

Comparativo:
- Frases: 34 → 68 (todas ≤20 palavras)
- "Requerente" removido (~15 ocorrências) → "você" / "responsável legal"
- Juridiquês eliminado: "impetração do pleito", "no âmbito de", "documentação hábil" etc.
- Links renomeados de "clique aqui" para texto descritivo

---

## Handoff com agentes existentes

Após gerar a carta, o agente sugere revisão de conformidade com:

- **`linguagem-simples-revisor`** — audita conformidade com Lei 15.263/2025 e pontua

---

## Referências

- [Manual para a Produção da Carta de Serviço — Governo do Acre](manual/Manual_de_Carta_de_Servicos.pdf) (metodologia base)
- Lei Federal 15.263/2025 — Linguagem Simples
- Decreto Estadual 16.744/2026 (MS) — Regulamenta linguagem simples em MS
- Lei Federal 13.460/2017 — Código de Defesa do Usuário do Serviço Público
- [Padrão Digital do Governo Federal — Cartas de Serviço](https://www.gov.br/ds/pt-br)

---

## Contribuindo

Este repositório é um exemplo/piloto da SETDIG (Secretaria-Executiva de Transformação Digital — MS). Sugestões de melhoria no agente, novos exemplos de serviços refatorados e melhorias no script de conversão são bem-vindos via issue ou PR.

---

## Licença

Uso público. Adaptação livre para órgãos estaduais e municipais que queiram padronizar suas Cartas de Serviço.
