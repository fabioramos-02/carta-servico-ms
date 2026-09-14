# CLAUDE.md — Instruções do projeto

Este repositório mantém o **agente Claude Code para construir Cartas de Serviço no padrão MS**, exemplos e scripts auxiliares.

## Ao trabalhar neste repo

- **Idioma:** pt-BR com acentuação completa. Nunca escrever "servico", "cidadao", "nao".
- **Nome oficial:** "Secretaria-Executiva de Transformação Digital — SETDIG". Nunca "Governo Digital".
- **Padrão fixo das 8 seções da carta**: Título | O QUE É? | Exigências | Quem pode utilizar? | Prazo | Custos | Etapas | Outras Informações. Nesta ordem, sem inventar seção nova.
- **Base legal citada:** Lei Federal 15.263/2025, Decreto Estadual 16.744/2026 (MS), Lei Federal 13.460/2017.

## Ao editar o agente (`agents/carta-servico-ms.md`)

- Manter frontmatter `name:` e `description:` compatível com Claude Code subagents.
- Preservar as regras de linguagem simples (frases ≤20 palavras, voz ativa, "você", substituições léxicas).
- Preservar marcadores anti-alucinação (`[FALTA: ...]`, `[VERIFICAR: ...]`).
- Ao mudar o agente aqui, replicar em `~/.claude/agents/carta-servico-ms.md` para ativar localmente.

## Ao criar novo exemplo

Cada serviço vive em **pasta própria** dentro de `entrada/` e `saida/`, com o slug repetido no nome do arquivo:

```
exemplos/
├── entrada/{slug-servico}/{slug-servico}.md
└── saida/{slug-servico}/
    ├── {slug-servico}.md
    └── {slug-servico}.docx
```

- Slug: kebab-case, sem prefixo "carta-" (a pasta já indica o tipo)
- Ativos adicionais do serviço (prints, PDFs de referência, fluxogramas) ficam ao lado do `.md` na mesma pasta
- Ao gerar `.docx`, criar um script dedicado em `scripts/gerar_docx_{slug}.py` até o conversor ser generalizado

## Ao gerar `.docx`

- Fonte: **Arial 12** (obrigatório para docs SETDIG).
- Hiperlinks: azul `#0563C1`, sublinhados, com texto descritivo (nunca "clique aqui").
- Listas numeradas para etapas e exigências.
- Script atual está hardcoded no exemplo AGEPEN — ao generalizar, ler markdown de entrada e parsear seções.

## Convenção de commits

- Formato: `tipo: descrição curta em pt-BR`
- Tipos: `feat`, `fix`, `docs`, `refactor`, `chore`, `exemplo`
- Exemplos:
  - `feat: adiciona agente carta-servico-ms`
  - `exemplo: refatora carta cartão de visitante AGEPEN`
  - `docs: atualiza README com instruções de handoff`
- **Nunca** incluir `Co-Authored-By: Claude` ou assinaturas de IA.

## Ao rodar scripts

- Python 3.10+ (testado em 3.14).
- Dependência única: `python-docx`.
- Não commitar `__pycache__/`, `.venv/`, arquivos temporários (`~$*.docx`).

## Handoff entre agentes

Fluxo recomendado ao produzir uma carta:

1. `carta-servico-ms` — gera a carta
2. `linguagem-simples-revisor` — audita conformidade Lei 15.263/2025
3. Ajustar lacunas marcadas `[FALTA: ...]` manualmente
4. Gerar `.docx` via `scripts/gerar_docx.py` (se necessário publicar em Word)
5. Publicar no portal do órgão
