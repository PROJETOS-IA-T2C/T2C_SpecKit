# Breakdown de Tarefas

> **⚠️ IMPORTANTE:** Ao criar o arquivo final, replique apenas a estrutura do template. Remova todas as anotações, exemplos e informações que não sejam do processo real. Mantenha apenas as informações reais do processo para reduzir a quantidade de informação no documento.

**Baseado em:** `spec.md` ou `robot*/spec.md` - Especificação Técnica

**Nota:** As tasks abaixo consolidam múltiplas etapas técnicas detalhadas no spec.md. 
Consulte o spec.md correspondente para todos os detalhes de implementação (seletores, validações, regras, T2CTracker, etc.).

> **⚠️ IMPORTANTE:** Se o projeto tiver múltiplos robôs, cada task deve indicar qual robô está trabalhando. As tasks devem ser organizadas agrupando primeiro todas as tasks de um robô, depois as do próximo.

## 🚨 REGRAS CRÍTICAS PARA TASKS

**⚠️ OBRIGATÓRIO - Seguir Ordem Exata do spec.md:**

1. **Tasks devem seguir a ordem EXATA das etapas no spec.md:**
   - INIT: Seguir a ordem exata das etapas listadas na seção INIT do spec.md
   - FILA: Seguir a ordem exata das etapas listadas na seção FILA do spec.md (se aplicável)
   - LOOP STATION: **Seguir a ordem EXATA das etapas listadas na seção LOOP STATION do spec.md**
   - END PROCESS: Seguir a ordem exata das etapas listadas na seção END PROCESS do spec.md

2. **Tasks devem ser mais detalhadas (quebradas em mais tasks menores):**
   - ❌ **NÃO criar tasks vagas** como "Processar item" ou "Inicializar sistemas"
   - ✅ **Criar tasks específicas** para cada etapa ou grupo lógico de etapas relacionadas
   - ✅ **Quebrar em mais tasks** para que a LLM consiga focar melhor ao gerar código
   - ✅ **Cada etapa do LOOP STATION** deve ter sua própria task (ou grupo lógico de etapas relacionadas)

3. **NÃO criar tasks para coisas que não precisam ser feitas:**
   - ❌ **NÃO criar task** para "Inicializar API" (APIs não precisam inicialização)
   - ❌ **NÃO criar task** para coisas que são automáticas ou não requerem código
   - ✅ **Criar tasks apenas** para ações que requerem implementação de código

4. **Descrições das tasks devem ser específicas:**
   - ❌ **NÃO usar descrições vagas** como "Processar dados" ou "Validar informações"
   - ✅ **Usar descrições específicas** como "Consultar CPF na API ReceitaWS", "Preencher formulário de cadastro", "Validar se CPF está na blacklist (EXC001)"

---

## 📊 Visão Geral de Estimativas

### Resumo Executivo

| Métrica | Valor |
|---------|-------|
| **Total de Tasks** | [X] |
| **Tempo Total Estimado** | [X horas / X dias] |
| **Tasks por Robô** | Robot1: [X] / Robot2: [X] / Standalone: [X] |
| **Maior Estimativa** | [Task X.X - X horas] |
| **Menor Estimativa** | [Task X.X - X horas] |

### Top 5 Tasks com Maior Estimativa

| Task | Descrição | Robô | Estimativa | % do Total |
|------|-----------|------|------------|------------|
| [Task X.X] | [Descrição resumida] | [robot1/robot2/raiz] | [X horas] | [X%] |
| [Task X.X] | [Descrição resumida] | [robot1/robot2/raiz] | [X horas] | [X%] |
| [Task X.X] | [Descrição resumida] | [robot1/robot2/raiz] | [X horas] | [X%] |
| [Task X.X] | [Descrição resumida] | [robot1/robot2/raiz] | [X horas] | [X%] |
| [Task X.X] | [Descrição resumida] | [robot1/robot2/raiz] | [X horas] | [X%] |

### Estimativas por Fase

| Fase | Tasks | Tempo Total | % do Total |
|------|-------|-------------|------------|
| INIT - Inicialização | [X] | [X horas] | [X%] |
| LOOP STATION - Processamento | [X] | [X horas] | [X%] |
| END PROCESS - Finalização | [X] | [X horas] | [X%] |

### Estimativas por Robô (se múltiplos robôs)

| Robô | Tasks | Tempo Total | % do Total |
|------|-------|-------------|------------|
| Robot1 | [X] | [X horas] | [X%] |
| Robot2 | [X] | [X horas] | [X%] |

---

## Fase 1: INIT - Inicialização

> **Nota:** As tasks abaixo devem seguir a ordem EXATA das etapas listadas na seção INIT do spec.md. Cada etapa ou grupo lógico de etapas relacionadas deve ter sua própria task específica.

### Task 1.1: [Nome Específico da Etapa - ex: "Abrir navegador Chrome e navegar para URL inicial"]
- **Robô:** [robot1 / robot2 / raiz se standalone]
- **Consolida etapas do spec:** `spec.md` ou `robot*/spec.md` - INIT: Etapa [X] - [Nome da etapa]
- **Arquivo:** T2CInitAllApplications.py
- **Método:** execute()
- **Descrição:** [Descrição específica do que esta etapa faz, ex: "Abrir navegador Chrome em modo headless=False e navegar para https://sistema.com"]
- **Estimativa:** [X horas] - [Justificativa breve da estimativa]
- **Status:** [ ] Pendente / [ ] Em Progresso / [ ] Concluído

### Task 1.2: [Nome Específico da Etapa - ex: "Realizar login no sistema"]
- **Robô:** [robot1 / robot2 / raiz se standalone]
- **Consolida etapas do spec:** `spec.md` ou `robot*/spec.md` - INIT: Etapa [Y] - [Nome da etapa]
- **Arquivo:** T2CInitAllApplications.py
- **Método:** execute()
- **Descrição:** [Descrição específica, ex: "Preencher campo usuário e senha, clicar em botão entrar, validar que chegou na homepage"]
- **Estimativa:** [X horas] - [Justificativa breve da estimativa]
- **Status:** [ ] Pendente / [ ] Em Progresso / [ ] Concluído

[Continue adicionando tasks específicas para cada etapa do INIT na ordem exata do spec.md...]

## Fase 1.5: FILA - Preenchimento da Fila (se aplicável)

> **Nota:** Se o robô preenche fila, as tasks abaixo devem seguir a ordem EXATA das etapas listadas na seção FILA do spec.md.

### Task 1.X: [Nome Específico da Etapa - ex: "Ler arquivo Excel e extrair dados"]
- **Robô:** [robot1 / robot2 / raiz se standalone]
- **Consolida etapas do spec:** `spec.md` ou `robot*/spec.md` - FILA: Etapa [X] - [Nome da etapa]
- **Arquivo:** T2CInitAllApplications.py
- **Método:** add_to_queue()
- **Descrição:** [Descrição específica, ex: "Ler arquivo dados.xlsx usando pandas, extrair colunas CPF, Nome e Valor"]
- **Estimativa:** [X horas] - [Justificativa breve da estimativa]
- **Status:** [ ] Pendente / [ ] Em Progresso / [ ] Concluído

[Continue adicionando tasks específicas para cada etapa da FILA na ordem exata do spec.md...]

---

## Fase 2: LOOP STATION - Processamento Principal

> **⚠️ CRÍTICO:** As tasks abaixo **DEVEM seguir a ordem EXATA** das etapas listadas na seção LOOP STATION do spec.md. Cada etapa ou grupo lógico de etapas relacionadas deve ter sua própria task específica.

### Task 2.1: [Nome Específico da Etapa - ex: "Validar CPF na blacklist (EXC001)"]
- **Robô:** [robot1 / robot2 / raiz se standalone]
- **Consolida etapas do spec:** `spec.md` ou `robot*/spec.md` - LOOP STATION: Etapa [1] - [Nome da etapa]
- **Arquivo:** T2CProcess.py
- **Método:** execute()
- **Descrição:** [Descrição específica, ex: "Validar se CPF do item está na blacklist, se estiver lançar BusinessRuleException com mensagem 'CPF na blacklist (EXC001)'"]
- **Estimativa:** [X horas] - [Justificativa breve da estimativa]
- **Status:** [ ] Pendente / [ ] Em Progresso / [ ] Concluído

### Task 2.2: [Nome Específico da Etapa - ex: "Consultar CPF na API ReceitaWS"]
- **Robô:** [robot1 / robot2 / raiz se standalone]
- **Consolida etapas do spec:** `spec.md` ou `robot*/spec.md` - LOOP STATION: Etapa [2] - [Nome da etapa]
- **Arquivo:** T2CProcess.py
- **Método:** execute()
- **Descrição:** [Descrição específica, ex: "Fazer requisição GET para API ReceitaWS com CPF do item, extrair dados de nome e situação cadastral"]
- **Estimativa:** [X horas] - [Justificativa breve da estimativa]
- **Status:** [ ] Pendente / [ ] Em Progresso / [ ] Concluído

### Task 2.3: [Nome Específico da Etapa - ex: "Preencher formulário de cadastro no sistema"]
- **Robô:** [robot1 / robot2 / raiz se standalone]
- **Consolida etapas do spec:** `spec.md` ou `robot*/spec.md` - LOOP STATION: Etapa [3] - [Nome da etapa]
- **Arquivo:** T2CProcess.py
- **Método:** execute()
- **Descrição:** [Descrição específica, ex: "Preencher campo CPF, nome, email e telefone no formulário, clicar em botão Salvar"]
- **Estimativa:** [X horas] - [Justificativa breve da estimativa]
- **Status:** [ ] Pendente / [ ] Em Progresso / [ ] Concluído

[Continue adicionando tasks específicas para cada etapa do LOOP STATION na ordem EXATA do spec.md...]

---

## Fase 3: END PROCESS - Finalização

> **Nota:** As tasks abaixo devem seguir a ordem EXATA das etapas listadas na seção END PROCESS do spec.md. Cada etapa ou grupo lógico de etapas relacionadas deve ter sua própria task específica.

### Task 3.1: [Nome Específico da Etapa - ex: "Fechar navegador Chrome"]
- **Robô:** [robot1 / robot2 / raiz se standalone]
- **Consolida etapas do spec:** `spec.md` ou `robot*/spec.md` - END PROCESS: Etapa [X] - [Nome da etapa]
- **Arquivo:** T2CCloseAllApplications.py
- **Método:** execute()
- **Descrição:** [Descrição específica, ex: "Fechar navegador Chrome usando InitAllSettings.var_botWebbot.stop_browser()"]
- **Estimativa:** [X horas] - [Justificativa breve da estimativa]
- **Status:** [ ] Pendente / [ ] Em Progresso / [ ] Concluído

### Task 3.2: [Nome Específico da Etapa - ex: "Enviar e-mail de conclusão"]
- **Robô:** [robot1 / robot2 / raiz se standalone]
- **Consolida etapas do spec:** `spec.md` ou `robot*/spec.md` - END PROCESS: Etapa [Y] - [Nome da etapa]
- **Arquivo:** T2CCloseAllApplications.py
- **Método:** execute()
- **Descrição:** [Descrição específica, ex: "Enviar e-mail para destinatários configurados com resumo de execução (total processado, sucessos, erros)"]
- **Estimativa:** [X horas] - [Justificativa breve da estimativa]
- **Status:** [ ] Pendente / [ ] Em Progresso / [ ] Concluído

[Continue adicionando tasks específicas para cada etapa do END PROCESS na ordem exata do spec.md...]
