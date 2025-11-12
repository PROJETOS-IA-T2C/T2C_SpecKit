# Breakdown de Tarefas

> **⚠️ IMPORTANTE:** Ao criar o arquivo final, replique apenas a estrutura do template. Remova todas as anotações, exemplos e informações que não sejam do processo real. Mantenha apenas as informações reais do processo para reduzir a quantidade de informação no documento.

**Baseado em:** `spec.md` ou `robot*/spec.md` - Especificação Técnica

**Nota:** As tasks abaixo consolidam múltiplas etapas técnicas detalhadas no spec.md. 
Consulte o spec.md correspondente para todos os detalhes de implementação (seletores, validações, regras, T2CTracker, etc.).

> **⚠️ IMPORTANTE:** Se o projeto tiver múltiplos robôs, cada task deve indicar qual robô está trabalhando. As tasks devem ser organizadas agrupando primeiro todas as tasks de um robô, depois as do próximo.

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

### Task 1.1: Inicializar Sistemas
- **Robô:** [robot1 / robot2 / raiz se standalone]
- **Consolida etapas do spec:** `spec.md` ou `robot*/spec.md` - INIT: Sistemas a Inicializar (todos)
- **Arquivo:** T2CInitAllApplications.py
- **Método:** execute()
- **Descrição:** Inicializar todos os sistemas/aplicações necessários conforme especificado no spec
- **Estimativa:** [X horas] - [Justificativa breve da estimativa]
- **Status:** [ ] Pendente / [ ] Em Progresso / [ ] Concluído

### Task 1.2: Preencher Fila
- **Robô:** [robot1 / robot2 / raiz se standalone]
- **Consolida etapas do spec:** `spec.md` ou `robot*/spec.md` - FILA: Preenchimento da Fila
- **Arquivo:** T2CInitAllApplications.py
- **Método:** add_to_queue()
- **Descrição:** Preencher fila de processamento conforme especificado no spec
- **Estimativa:** [X horas] - [Justificativa breve da estimativa]
- **Status:** [ ] Pendente / [ ] Em Progresso / [ ] Concluído

---

## Fase 2: LOOP STATION - Processamento Principal

### Task 2.1: [Nome do Grupo Lógico de Etapas]
- **Robô:** [robot1 / robot2 / raiz se standalone]
- **Consolida etapas do spec:** `spec.md` ou `robot*/spec.md` - LOOP STATION: Etapas [X, Y, Z]
- **Arquivo:** T2CProcess.py
- **Método:** execute()
- **Descrição:** [Descrição resumida do que este grupo de etapas faz]
- **Estimativa:** [X horas] - [Justificativa breve da estimativa]
- **Status:** [ ] Pendente / [ ] Em Progresso / [ ] Concluído

### Task 2.2: [Nome do Grupo Lógico de Etapas]
- **Robô:** [robot1 / robot2 / raiz se standalone]
- **Consolida etapas do spec:** `spec.md` ou `robot*/spec.md` - LOOP STATION: Etapas [X, Y, Z]
- **Arquivo:** T2CProcess.py
- **Método:** execute()
- **Descrição:** [Descrição resumida do que este grupo de etapas faz]
- **Estimativa:** [X horas] - [Justificativa breve da estimativa]
- **Status:** [ ] Pendente / [ ] Em Progresso / [ ] Concluído

### Task 2.3: [Nome do Grupo Lógico de Etapas]
- **Robô:** [robot1 / robot2 / raiz se standalone]
- **Consolida etapas do spec:** `spec.md` ou `robot*/spec.md` - LOOP STATION: Etapas [X, Y, Z]
- **Arquivo:** T2CProcess.py
- **Método:** execute()
- **Descrição:** [Descrição resumida do que este grupo de etapas faz]
- **Estimativa:** [X horas] - [Justificativa breve da estimativa]
- **Status:** [ ] Pendente / [ ] Em Progresso / [ ] Concluído

[Continue adicionando tasks conforme necessário para agrupar as etapas do LOOP STATION...]

---

## Fase 3: END PROCESS - Finalização

### Task 3.1: Fechar Sistemas
- **Robô:** [robot1 / robot2 / raiz se standalone]
- **Consolida etapas do spec:** `spec.md` ou `robot*/spec.md` - END PROCESS: Sistemas a Fechar (todos)
- **Arquivo:** T2CCloseAllApplications.py
- **Método:** execute()
- **Descrição:** Fechar todos os sistemas/aplicações abertos conforme especificado no spec
- **Estimativa:** [X horas] - [Justificativa breve da estimativa]
- **Status:** [ ] Pendente / [ ] Em Progresso / [ ] Concluído

### Task 3.2: Enviar E-mail Final
- **Robô:** [robot1 / robot2 / raiz se standalone]
- **Consolida etapas do spec:** `spec.md` ou `robot*/spec.md` - END PROCESS: E-mail Final
- **Arquivo:** T2CCloseAllApplications.py
- **Método:** execute()
- **Descrição:** Enviar e-mail de conclusão conforme especificado no spec
- **Estimativa:** [X horas] - [Justificativa breve da estimativa]
- **Status:** [ ] Pendente / [ ] Em Progresso / [ ] Concluído
