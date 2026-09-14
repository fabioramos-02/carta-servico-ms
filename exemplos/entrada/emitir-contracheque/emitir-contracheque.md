# Material bruto — Emitir Contracheque (SAD)

**Órgão responsável:** Secretaria de Estado de Administração — SAD
**Serviço:** Emitir Contracheque
**Público:** Servidor público estadual (ativo)
**Prazo:** Imediato após login
**Custo:** Gratuito
**Canais:** App MS Digital e Portal do Servidor (navegador)

## URLs

- Portal do Servidor (login): https://www.portaldoservidor.ms.gov.br/Entrar/Login
- Recuperação de senha: https://www.portaldoservidor.ms.gov.br/SenhaDeAcesso/EsqueciMinhaSenha
- App MS Digital: disponível na Google Play e App Store

## Exigências

- Matrícula funcional
- Senha de acesso ao Portal do Servidor
- Para uso via App: conta gov.br autenticada ou CPF + senha do Portal

## Fluxo pelo Portal do Servidor (navegador)

1. Acessar https://www.portaldoservidor.ms.gov.br/Entrar/Login
2. Preencher CPF, senha e desafio de verificação (captcha)
3. Menu: Serviços > Dados Financeiros > Emissão de Contracheque
4. Selecionar ano e mês
5. Consultar / baixar PDF

## Fluxo pelo App MS Digital

Fluxograma fornecido pelo usuário:

```
Início
  ↓
Acessar app MS Digital
  ↓
Realizar login Gov.br ou CPF/Senha
  ↓
Autenticar usuário
  ↓
Usuário identificado?
  ├── Não → Retornar para login
  └── Sim
       ↓
  Exibir serviços disponíveis
       ↓
  Selecionar "Servidor Público"
       ↓
  Selecionar "Portal do Servidor"
       ↓
  Usuário possui vínculo ativo?
       ├── Sim → Exibir usuários disponíveis → Selecionar usuário
       └── Não → Solicitar CPF e senha → Autenticar no Portal do Servidor
                 ↓
          Autenticação realizada?
            ├── Não → Exibir alerta → Tentar novamente
            └── Sim → Exibir menu do usuário
                       ↓
                Acessar "Contracheque"
                       ↓
                Selecionar ano e mês
                       ↓
                Consultar contracheque
                       ↓
                Contracheque localizado?
                  ├── Não → Exibir alerta → Nova consulta
                  └── Sim → Exibir dados
                            ↓
                       Baixar PDF?
                       ├── Não → Encerrar
                       └── Sim → Selecionar "Baixar PDF" → Gerar pré-visualização → Fim
```

## Base legal (referência geral)

- Lei Federal 15.263/2025 (linguagem simples no serviço público)
- Decreto Estadual 16.744/2026 (aplicação da Lei 15.263/2025 em MS)
- Lei Federal 13.460/2017 (Código de Defesa do Usuário do Serviço Público)

## Lacunas

- Telefone / e-mail / WhatsApp do canal de atendimento SAD para dúvidas sobre contracheque
- Portaria / decreto SAD específico sobre contracheque digital (se houver)
- Prazo para correção de divergências no contracheque
- Confirmação sobre pensionista, inativo e terceirizado (usuário respondeu apenas "servidor")
