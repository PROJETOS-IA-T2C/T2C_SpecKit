# Especificação Técnica - Arquitetura do Robô

**Este é o arquivo principal do projeto.** Define a arquitetura completa e o que cada parte do código deve fazer.

---

## Stack Tecnológica

- **Framework:** T2C Framework (v2.2.3)
- **Automação Web:** Clicknium
- **Plataforma:** BotCity
- **Linguagem:** Python 3.8+

---

## Visão Geral do Fluxo

Este documento define o fluxo completo de execução do robô, dividido em 4 fases principais:

1. **INIT (Inicialização)**: Inicializa todos os sistemas/aplicações necessários e prepara o ambiente para processamento
2. **FILA (Preenchimento)**: Preenche a fila de processamento com os itens a serem processados (se aplicável)
3. **LOOP STATION (Processamento)**: Processa cada item da fila, executando todas as etapas do DDP
4. **END PROCESS (Finalização)**: Fecha sistemas, gera relatórios e envia e-mail de conclusão

**Fluxo de Execução:**
```
INIT → FILA → LOOP STATION (para cada item) → END PROCESS
```

**Tempo estimado de desenvolvimento:** [X horas/dias]

---

## INIT: Inicialização (T2CInitAllApplications.execute)

### Sistemas a Inicializar

Liste todos os sistemas/aplicações que precisam ser iniciados:

1. **[Nome do Sistema 1]**
   - **Tipo:** [Web/Desktop/API]
   - **URL/Tela Inicial:** [URL ou tela onde deve iniciar]
   - **Estado Esperado:** [Em qual tela/página o sistema deve estar para entrar no Loop Station]
   - **Credenciais:** [Como obter - Config.xlsx, Maestro, etc.]
   - **Observações:** [Qualquer informação relevante]

2. **[Nome do Sistema 2]**
   - **Tipo:** [Web/Desktop/API]
   - **URL/Tela Inicial:** [URL ou tela onde deve iniciar]
   - **Estado Esperado:** [Em qual tela/página o sistema deve estar para entrar no Loop Station]
   - **Credenciais:** [Como obter]
   - **Observações:** [Qualquer informação relevante]

### Integração T2CTracker

- [ ] **Step de Inicialização:** [Número do step no Tracker]
- [ ] **Mensagem:** [Mensagem a ser enviada ao Tracker]

---

## FILA: Preenchimento da Fila (T2CInitAllApplications.add_to_queue)

### Estrutura do Item da Fila

**Referência (identificador único):**
- Campo: `referencia`
- Tipo: `str`
- Exemplo: `"REF001"`, `"ID_12345"`, `"CPF_12345678901"`

**Info Adicionais (dados do item):**
- Tipo: `dict` (JSON)
- Estrutura:
```json
{
  "campo1": "valor1",
  "campo2": "valor2",
  "campo3": 123
}
```

### Como Desenvolver a Fila

**IMPORTANTE:** A lógica de preenchimento da fila deve ser **SIMPLE e DIRETA**:
- Normalmente é apenas uma leitura (Excel, CSV, API, Banco de Dados)
- Sem muitas funções ou lógica complexa
- Se precisar de lógica complexa, considere criar um robô separado (conceito de **Dispatcher** e **Performer**)

**Exemplos de fontes de dados:**
- [ ] Arquivo Excel/CSV
- [ ] Consulta SQL
- [ ] API REST
- [ ] Outro sistema
- [ ] Manual (lista fixa)

**Descrição da Implementação:**
[Descreva como os dados serão lidos e inseridos na fila. Se for mais complexo que uma simples leitura, considere criar um dispatcher separado.]

### Integração T2CTracker

- [ ] **Step de Preenchimento:** [Número do step no Tracker]
- [ ] **Mensagem:** [Mensagem a ser enviada ao Tracker]

---

## LOOP STATION: Processamento Principal (T2CProcess.execute)

**Este é o coração do robô.** Aqui deve estar TODO o código principal que processa cada item da fila.

### Etapas de Execução

**IMPORTANTE:** Todas as etapas do DDP devem estar documentadas aqui, sem exceção.

#### Exemplo de Etapa (Modelo a seguir)

**Etapa 1: Login no Sistema SAP**
- **Descrição:** Realizar login no sistema SAP usando credenciais obtidas do item da fila. Validar se o login foi bem-sucedido verificando a presença do menu principal.
- **Seletores utilizados:** Ver `selectors.md` - Seção "Login SAP" (campo_usuario, campo_senha, botao_entrar, menu_principal)
- **Validações aplicadas:** Ver `business-rules.md` - VAL001 (validar se usuário e senha não estão vazios), VAL002 (validar formato do usuário)
- **Regras de negócio:** Ver `business-rules.md` - REG001 (tentar login até 3 vezes em caso de erro de sistema)
- **Condições especiais:** Ver `business-rules.md` - COND001 (se usuário estiver bloqueado, pular item e registrar erro de negócio)
- **T2CTracker Step:** 10 - "Iniciando login no sistema SAP"
- **Observações:** 
  - Aguardar 3 segundos após clicar em entrar para garantir carregamento completo
  - Se login falhar após 3 tentativas, lançar Exception para permitir retentativa pelo framework
  - Se usuário bloqueado, lançar BusinessRuleException para não retentar

---

#### Etapa 1: [Nome da Etapa]
- **Descrição:** [O que esta etapa faz - seja específico e detalhado]
- **Seletores utilizados:** Ver `selectors.md` - [Seção específica] ([lista de seletores usados])
- **Validações aplicadas:** Ver `business-rules.md` - [VAL001, VAL002, etc.]
- **Regras de negócio:** Ver `business-rules.md` - [REG001, REG002, etc.]
- **Condições especiais:** Ver `business-rules.md` - [COND001, COND002, etc.]
- **T2CTracker Step:** [Número do step] - "[Mensagem descritiva]"
- **Observações:** 
  - [Aguardas necessárias, timeouts, etc.]
  - [Comportamento em caso de erro]
  - [Qualquer informação relevante para implementação]

#### Etapa 2: [Nome da Etapa]
- **Descrição:** [O que esta etapa faz - seja específico e detalhado]
- **Seletores utilizados:** Ver `selectors.md` - [Seção específica] ([lista de seletores usados])
- **Validações aplicadas:** Ver `business-rules.md` - [VAL003, etc.]
- **Regras de negócio:** Ver `business-rules.md` - [REG003, etc.]
- **Condições especiais:** Ver `business-rules.md` - [COND003, etc.]
- **T2CTracker Step:** [Número do step] - "[Mensagem descritiva]"
- **Observações:** 
  - [Aguardas necessárias, timeouts, etc.]
  - [Comportamento em caso de erro]
  - [Qualquer informação relevante para implementação]

#### Etapa 3: [Nome da Etapa]
- **Descrição:** [O que esta etapa faz - seja específico e detalhado]
- **Seletores utilizados:** Ver `selectors.md` - [Seção específica] ([lista de seletores usados])
- **Validações aplicadas:** Ver `business-rules.md` - [VAL004, etc.]
- **Regras de negócio:** Ver `business-rules.md` - [REG004, etc.]
- **T2CTracker Step:** [Número do step] - "[Mensagem descritiva]"
- **Observações:** 
  - [Aguardas necessárias, timeouts, etc.]
  - [Comportamento em caso de erro]
  - [Qualquer informação relevante para implementação]

[Continue adicionando todas as etapas do DDP seguindo o modelo acima...]

### Tratamento de Business Exceptions

**IMPORTANTE:** Todas as BusinessRuleException devem estar documentadas em `business-rules-template.md` e apenas referenciadas aqui.

- **Validações (VAL*):** Ver `business-rules-template.md`
- **Condições Especiais (COND*):** Ver `business-rules-template.md`
- **Regras de Processamento (REG*):** Ver `business-rules-template.md`

### Integração T2CTracker

Liste os steps do Tracker que serão utilizados durante o processamento:

- [ ] **Step [Número]:** [Nome/Mensagem] - [Quando é chamado]
- [ ] **Step [Número]:** [Nome/Mensagem] - [Quando é chamado]
- [ ] **Step [Número]:** [Nome/Mensagem] - [Quando é chamado]

---

## END PROCESS: Finalização (T2CCloseAllApplications.execute)

### Sistemas a Fechar

Liste todos os sistemas/aplicações que precisam ser fechados:

1. **[Nome do Sistema 1]**
   - **Método de fechamento:** [Como fechar - stop_browser(), taskkill, etc.]
   - **Observações:** [Qualquer informação relevante]

2. **[Nome do Sistema 2]**
   - **Método de fechamento:** [Como fechar]
   - **Observações:** [Qualquer informação relevante]

### E-mail Final

**IMPORTANTE:** O corpo do e-mail deve estar formatado e pronto para validação do desenvolvedor.

**Assunto:** [Assunto do e-mail]

**Corpo do E-mail:**
```
[Corpo do e-mail formatado aqui]

Exemplo:
Prezados,

O processamento foi finalizado com sucesso.

Total de itens processados: [quantidade]
Itens com sucesso: [quantidade]
Itens com erro: [quantidade]

Atenciosamente,
Robô [Nome do Robô]
```

**Destinatários:** [Lista de destinatários ou referência ao Config.xlsx]

### Integração T2CTracker

- [ ] **Step Final:** [Número do step no Tracker]
- [ ] **Mensagem:** [Mensagem final a ser enviada ao Tracker]

---

## Integrações do Projeto

- [ ] **Maestro (BotCity):** [SIM/NÃO] - [Observações]
- [ ] **T2CTracker:** [SIM/NÃO] - [Observações]
- [ ] **Clicknium:** [SIM/NÃO] - [Observações]
- [ ] **E-mail:** [SIM/NÃO] - [Observações]

---

## Observações Gerais

[Qualquer observação adicional sobre a arquitetura, fluxo, ou implementação]
