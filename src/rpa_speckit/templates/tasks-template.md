# Breakdown de Tarefas

> **⚠️ IMPORTANTE:** Ao criar o arquivo final, replique apenas a estrutura do template. Remova todas as anotações, exemplos e informações de ajuda. Mantenha apenas as informações reais do processo.

**Baseado em:** `spec.md` (ou `robot*/spec.md`)

---

## 📊 Visão Geral de Estimativas (FEFP)

### Resumo Executivo

| Métrica | Valor |
|---------|-------|
| **Total de Tasks** | [X] |
| **Tempo Total Estimado** | [X horas] |
| **Tasks por Robô** | Robot1: [X] / Robot2: [X] |

### Top 5 Tasks (Maior Esforço)

| Task | Descrição | Robô | Estimativa (FEFP) |
|------|-----------|------|-------------------|
| [Task X.X] | [Descrição resumida] | [robot1] | [X h] |

---

## Fase 1: INIT - Inicialização

> **Nota:** Seguir a ordem EXATA das etapas do spec.md.

### Task 1.1: [Nome da Etapa]
- **Robô:** [robot1 / robot2]
- **Consolida:** INIT: Etapa [X]
- **Arquivo:** T2CInitAllApplications.py
- **Classe Especialista (Sugerida):** `classes_t2c/[sistema]/[NomeClasse].py`
- **Descrição:** [O que deve ser feito. Ex: "Criar classe LoginSAP e chamar método de login no Init."]
- **Estimativa:** [X horas] - [Base x Complexidade x 1.35]
- **Status:** [ ] Pendente

---

## Fase 1.5: FILA - Preenchimento (Se aplicável)

### Task 1.X: [Nome da Etapa]
- **Robô:** [robot1]
- **Consolida:** FILA: Etapa [X]
- **Arquivo:** T2CInitAllApplications.py (add_to_queue)
- **Classe Especialista (Sugerida):** `classes_t2c/[sistema]/[NomeClasse].py`
- **Descrição:** [Ex: "Criar classe LeitorExcel, ler input.xlsx e popular fila."]
- **Estimativa:** [X horas] - [Base x Complexidade x 1.35]
- **Status:** [ ] Pendente

---

## Fase 2: LOOP STATION - Processamento

> **⚠️ CRÍTICO:** Seguir a ordem EXATA do LOOP STATION no spec.md.

### Task 2.1: [Nome da Etapa]
- **Robô:** [robot1]
- **Consolida:** LOOP STATION: Etapa [1]
- **Arquivo:** T2CProcess.py
- **Classe Especialista (Sugerida):** `classes_t2c/[sistema]/[NomeClasse].py`
- **Descrição:** [Ex: "Criar método validar_cpf na classe Validador."]
- **Estimativa:** [X horas] - [Base x Complexidade x 1.35]
- **Status:** [ ] Pendente

[Adicione todas as tasks do Loop Station...]

---

## Fase 3: END PROCESS - Finalização

### Task 3.1: [Nome da Etapa]
- **Robô:** [robot1]
- **Consolida:** END PROCESS: Etapa [X]
- **Arquivo:** T2CCloseAllApplications.py
- **Classe Especialista (Sugerida):** `classes_t2c/[sistema]/[NomeClasse].py`
- **Descrição:** [Ex: "Chamar método logout na classe LoginSAP."]
- **Estimativa:** [X horas] - [Base x Complexidade x 1.35]
- **Status:** [ ] Pendente
