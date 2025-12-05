# Especificação Técnica - Arquitetura do Robô

> **⚠️ IMPORTANTE:** Ao criar o arquivo final, replique apenas a estrutura do template. Remova todas as anotações, exemplos e informações de ajuda. Mantenha apenas as informações reais do processo.

**Este é o arquivo principal do projeto.** Define a arquitetura completa e o que cada parte do código deve fazer.

---

## Arquitetura de Robôs

> **Nota:** Esta seção define se este robô é standalone ou parte de uma arquitetura com múltiplos robôs (dispatcher/performer).

- **Tipo:** [Standalone / Dispatcher / Performer]
- **Este robô é:** [Descrição breve do papel deste robô]
- **Recebe dados de:** [Nome do robô anterior ou "N/A"]
- **Alimenta:** [Nome do robô seguinte ou "N/A"]
- **Ordem na cadeia:** [Número sequencial ou "1"]
- **Nome da pasta do robô:** [robot1 / robot2 / raiz]

**Observações sobre arquitetura:**
- [Detalhes sobre filas compartilhadas, criação de itens vazios (se Dispatcher), etc.]

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

**Estimativa de Desenvolvimento (FEFP):**
- **Pontuação Total:** [Soma dos pontos FEFP]
- **Nível:** [Muito Baixa/Baixa/Média/Alta]
- **Tempo Estimado:** [X horas] (Baseado no cálculo FEFP: Tempo Base * 1.35)

---

## INIT: Inicialização (T2CInitAllApplications.execute)

### Sistemas a Inicializar

> **Regra:** Apenas sistemas com Interface Gráfica (UI) e login devem ser inicializados aqui. APIs, Bancos de Dados e Arquivos são acessados sob demanda.

1. **[Nome do Sistema 1]**
   - **Tipo:** [Web/Desktop]
   - **URL/Caminho:** [URL ou caminho do executável]
   - **Credenciais:** [Referência ao Config.xlsx ou "N/A"]
   - **Estado Esperado:** [Tela onde deve estar após login]

---

## FILA: Preenchimento da Fila (T2CInitAllApplications.add_to_queue)

> **Regra:** A fila é a ÚNICA fonte de dados para o Loop Station. Todos os dados necessários (leitura de Excel, API, etc.) devem ser consolidados aqui no objeto `info_adicionais`.

**Fonte de Dados:**
- [ ] Arquivo Excel/CSV
- [ ] API/Sistema
- [ ] Outro: [Especificar]

**Estrutura do Item da Fila (Payload):**
```json
{
  "referencia": "[Campo chave - ex: CPF, ID]",
  "info_adicionais": {
    "campo1": "valor1",
    "campo2": "valor2"
  }
}
```

**Lógica de Preenchimento:**
[Descreva como os dados são lidos e transformados para a fila]

---

## LOOP STATION: Processamento Principal (T2CProcess.execute)

> **Regra:** Use APENAS `var_dictItem['info_adicionais']` como fonte de dados. Não leia arquivos externos aqui.

### Etapas de Execução

> **Links:** Use `[selectors.md#nome-secao]` e `[business-rules.md#exc001]` para referências.

#### Etapa 1: [Nome da Ação]
- **Descrição:** [Ação específica a ser realizada]
- **Seletores:** Ver [`selectors.md#nome-secao`](./selectors.md)
- **Exceções:** Ver [`business-rules.md#exc001`](./business-rules.md)
- **Observações:** [Timeouts, validações específicas, etc.]

#### Etapa 2: [Nome da Ação]
- **Descrição:** [Ação específica a ser realizada]
- **Seletores:** Ver [`selectors.md#nome-secao`](./selectors.md)
- **Exceções:** Ver [`business-rules.md#exc001`](./business-rules.md)
- **Observações:** [Timeouts, validações específicas, etc.]

[Adicione mais etapas conforme necessário...]

---

## END PROCESS: Finalização (T2CCloseAllApplications.execute)

### Sistemas a Fechar

> **Regra:** Apenas feche os sistemas que foram abertos no INIT.

1. **[Nome do Sistema 1]**
   - **Ação:** [Logout / Fechar Janela / Kill Process]

### E-mail Final

**Assunto:** [Padrão do Assunto]
**Corpo:**
```text
[Template do e-mail final]
```

---

## Integrações e Configurações

- [ ] **Maestro:** [SIM/NÃO]
- [ ] **T2CTracker:** [SIM/NÃO]
- [ ] **Clicknium:** [SIM/NÃO]
- [ ] **E-mail:** [SIM/NÃO]

---

## Observações Gerais
[Pontos de atenção, riscos ou dependências externas]
