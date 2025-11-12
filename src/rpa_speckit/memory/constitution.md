# Constituição do Framework T2C

Este documento define TODAS as regras, especificações, padrões, exemplos e templates que a IA deve seguir ao gerar código para o framework T2C.

**IMPORTANTE:** Este documento é exclusivamente para uso da IA durante a geração de código. O desenvolvedor humano não precisa consultá-lo diretamente.

---

## 📋 PARTE 1: REGRAS FUNDAMENTAIS

### 1. Estrutura do Framework
- **Sempre usar as classes do framework** conforme especificação abaixo
- **Nunca modificar arquivos core do framework**
- **Usar apenas os pontos de entrada definidos:**
  - `T2CProcess.execute()` - Lógica principal de processamento
  - `T2CInitAllApplications.execute()` - Inicialização de aplicações
  - `T2CInitAllApplications.add_to_queue()` - Preencher fila
  - `T2CCloseAllApplications.execute()` - Fechar aplicações

### 2. Tratamento de Erros
- **BusinessRuleException:** Para erros de negócio (não tenta novamente)
  ```python
  from {{PROJECT_NAME}}.classes_t2c.utils.T2CExceptions import BusinessRuleException
  raise BusinessRuleException("Mensagem de erro de negócio")
  ```
- **TerminateException:** Para finalização antecipada com sucesso
  ```python
  from {{PROJECT_NAME}}.classes_t2c.utils.T2CExceptions import TerminateException
  raise TerminateException("Item já processado")
  ```
- **Exception genérica:** Para erros de sistema (permite retentativa)
  - O framework gerencia automaticamente as retentativas

### 3. Logging
- **Sempre usar `Maestro.write_log()`** para logs importantes
- **Incluir referência do item** quando disponível
- **Usar níveis de log apropriados:**
  - `LogLevel.INFO` - Informações gerais
  - `LogLevel.WARN` - Avisos
  - `LogLevel.ERROR` - Erros
  - `LogLevel.FATAL` - Erros fatais
- **Exemplo:**
  ```python
  from {{PROJECT_NAME}}.classes_t2c.utils.T2CMaestro import T2CMaestro as Maestro, LogLevel, ErrorType
  
  Maestro.write_log(
      arg_strMensagemLog="Processando item",
      arg_strReferencia=var_strReferencia,
      arg_enumLogLevel=LogLevel.INFO,
      arg_enumErrorType=ErrorType.NONE
  )
  ```

### 4. Configurações
- **Sempre acessar configurações via `InitAllSettings.var_dictConfig`**
- **Nunca hardcodar valores**, usar Config.xlsx ou config/*.md
- **Exemplo:**
  ```python
  from {{PROJECT_NAME}}.classes_t2c.framework.T2CInitAllSettings import T2CInitAllSettings as InitAllSettings
  
  var_strNomeProcesso = InitAllSettings.var_dictConfig["NomeProcesso"]
  var_intMaxTentativas = InitAllSettings.var_dictConfig["MaxRetryNumber"]
  ```

### 5. Seletores
- **Sempre usar locators do Clicknium** quando disponível
- **Referenciar seletores conforme `selectors/selectors.md`**
- **Nunca usar seletores hardcodados**
- **Exemplo:**
  ```python
  from clicknium import clicknium as cc, locator
  
  cc.find_element(locator.login.botao_entrar).click()
  ```

### 6. Regras de Negócio
- **Sempre aplicar regras conforme `business-rules/rules.md`**
- **Validar dados de entrada** antes de processar
- **Aplicar condições especiais** quando necessário
- **Usar BusinessRuleException ou TerminateException** conforme especificado nas regras

### 7. Fila de Processamento
- **Sempre usar `QueueManager`** para gerenciar fila
- **Acessar item atual via `GetTransaction.var_dictQueueItem`** no método `T2CProcess.execute()`
- **Estrutura do item:**
  ```python
  {
      'id': int,
      'referencia': str,
      'info_adicionais': dict,  # JSON parseado
      'status': str,
      'obs': str
  }
  ```
- **Adicionar itens:** Usar `QueueManager.insert_new_queue_item()` em `T2CInitAllApplications.add_to_queue()`
  - Sempre fornecer `arg_strReferencia` (identificador único)
  - Sempre fornecer `arg_dictInfAdicional` (dicionário com dados)
- **Atualizar status corretamente:**
  - `SUCESSO` - Processamento bem-sucedido
  - `BUSINESS ERROR` - Erro de regra de negócio
  - `APP ERROR` - Erro de sistema/aplicação
- **Exemplo básico:**
  ```python
  from {{PROJECT_NAME}}.classes_t2c.framework.T2CGetTransaction import T2CGetTransaction as GetTransaction
  from {{PROJECT_NAME}}.classes_t2c.queue.T2CQueueManager import T2CQueueManager as QueueManager
  
  var_dictItem = GetTransaction.var_dictQueueItem
  var_strReferencia = var_dictItem['referencia']
  var_dictInfoAdicional = var_dictItem['info_adicionais']
  ```
- **Ver PARTE 2 para detalhes completos de gerenciamento de fila**

### 8. Integrações
- **Tracker:** Usar apenas se `config/base.md` indicar `Usar T2CTracker: SIM`
- **Maestro:** Usar apenas se `config/base.md` indicar `Usar Maestro: SIM`
- **Clicknium:** Usar apenas se `config/base.md` indicar `Usar Clicknium: SIM`
- **Email:** Usar apenas se `config/base.md` indicar `Usar E-mail: SIM`
- **Sempre verificar configuração antes de usar integrações**

### 9. Código Limpo
- **Seguir padrão de nomenclatura:** Ver PARTE 8 para nomenclatura completa
- **Comentar código complexo**
- **Manter funções pequenas e focadas**
- **Reutilizar código existente quando possível**

### 10. Testes
- **Não focar em testes neste momento** (conforme especificação)
- **Focar apenas em desenvolvimento da automação**

### 11. Geração do Framework Completo
- **Ao executar `/t2c.implement`, gerar TODO o framework do zero**
- **Estrutura completa:** Criar todos os diretórios e arquivos necessários
- **Arquivos customizados:** Gerar apenas T2CProcess, T2CInitAllApplications, T2CCloseAllApplications, bot.py, Config.xlsx
- **Arquivos do framework:** Copiar de referência do framework T2C (não modificar)
- **Templates:** Usar templates definidos abaixo
- **Substituir variáveis:** `{{PROJECT_NAME}}`, `{{IMPORTS}}`, `{{VALIDACOES_ENTRADA}}`, etc.
- **Gerar em diretório separado:** Framework gerado em `generated/<nome-automacao>/`

### 12. Inicialização e Finalização de Aplicações
- **Inicialização:** Usar `InitAllSettings.initiate_web_manipulator()` para navegadores
  - Usar `InitAllSettings.var_botWebbot` para manipular navegador
  - Usar `InitAllSettings.var_botDesktopbot` para manipular desktop
  - Implementar loop de tentativas conforme padrão do framework (ver PARTE 8)
- **Finalização:** Fechar navegador com `InitAllSettings.var_botWebbot.stop_browser()`
  - Fechar aplicações desktop conforme necessário
  - Implementar loop de tentativas para fechamento
- **Ver PARTE 2 e PARTE 5 para exemplos completos**

### 13. Arquitetura de Robôs - Decisão e Estruturação

**⚠️ DECISÃO CRÍTICA:** Durante a análise do DDP (ao executar `/t2c.extract-ddp` e preencher as specs), a LLM DEVE decidir se o processo será:
- **Standalone**: Um único robô faz todo o processo
- **Múltiplos robôs**: Dispatcher + Performer ou Performer + Performer

#### Critérios para Análise de Arquitetura

**⚠️ IMPORTANTE:** A decisão de separar ou não em múltiplos robôs NÃO é uma regra binária. A LLM deve analisar o contexto completo do processo e considerar múltiplos fatores antes de decidir. Nem sempre ter 2 sistemas UI significa necessariamente 2 robôs - a decisão deve ser baseada na análise cuidadosa de todos os aspectos do processo.

**Contextos que TENDEM a favorecer separação em múltiplos robôs:**

1. **Complexidade e Extensão do LOOP STATION:**
   - Analisar se o LOOP STATION é muito extenso (muitas etapas, muitas regras de negócio, múltiplas integrações)
   - Considerar se a complexidade justifica separação para melhor organização e manutenção
   - Avaliar se dividir em fases distintas facilitaria o entendimento e desenvolvimento

2. **Complexidade da Preparação de Dados:**
   - Processos que requerem preparação complexa de dados (conciliações entre múltiplas fontes, validações extensas, enriquecimento via APIs, transformações complexas)
   - Quando a lógica de preenchimento da fila é significativamente mais complexa que o processamento em si
   - Casos onde a preparação de dados pode ser feita de forma independente e assíncrona

3. **Separação Lógica por Responsabilidade:**
   - Processos com fases distintas que têm responsabilidades claramente diferentes
   - Quando um robô prepara dados e outro executa ações em sistemas diferentes
   - Separação por sistema quando há benefício claro em termos de manutenção, testes e evolução independente

4. **Benefícios de Organização e Manutenção:**
   - Quando a separação facilitaria significativamente a manutenção do código
   - Casos onde cada robô teria responsabilidades bem definidas e distintas
   - Processos que podem evoluir de forma independente em cada robô

5. **Processos Assíncronos ou com Verificação:**
   - Processos que envolvem etapas de verificação manual ou aguardar resposta de sistemas externos
   - Quando há necessidade de retry control diferenciado entre fases
   - Processos onde uma fase pode ser executada independentemente da outra

6. **Modularização de Etapas Opcionais:**
   - Quando certas etapas do processo são opcionais e podem ser habilitadas/desabilitadas sem modificar código
   - Separação que permite flexibilidade na execução de partes do processo

**Contextos que TENDEM a favorecer arquitetura Standalone:**

1. **Simplicidade do Processo:**
   - Processos diretos e lineares (leitura de Excel, validação simples, inserção em sistema)
   - Lógica que cabe confortavelmente em um único robô sem sobrecarga
   - Processos com poucas etapas e regras de negócio simples

2. **Cohesão Funcional:**
   - Quando todas as etapas do processo estão fortemente acopladas e fazem sentido juntas
   - Processos onde separar criaria dependências complexas sem benefício claro
   - Casos onde a lógica de negócio é indivisível

3. **Sem Benefício Claro de Separação:**
   - Quando não há ganho evidente em termos de manutenção, organização ou complexidade
   - Processos onde a separação adicionaria complexidade desnecessária
   - Casos onde o overhead de gerenciar múltiplos robôs não se justifica

**⚠️ REGRA DE OURO:** A decisão final deve ser baseada na análise cuidadosa do contexto completo do processo, considerando:
- Complexidade técnica vs. benefício de separação
- Manutenibilidade futura
- Clareza de responsabilidades
- Facilidade de testes e evolução
- Overhead de gerenciamento de múltiplos robôs

**NÃO existe uma regra absoluta.** A LLM deve pesar todos os fatores e tomar a decisão que faz mais sentido para o processo específico em análise.

#### Tipos de Arquitetura

**1. Standalone (1 robô)**
- **Estrutura:** `specs/001-[nome]/spec.md` (na raiz)
- Um único robô executa: INIT → FILA → LOOP STATION → END PROCESS
- Todos os arquivos na raiz: `spec.md`, `selectors.md`, `business-rules.md`, `tests.md`, `tasks.md`
- **Quando usar:** Processos simples, diretos, que não justificam separação

**2. Dispatcher + Performer**
- **Dispatcher** (`robot1/`):
  - **Função:** Prepara dados e popula a fila do performer
  - **OBRIGATÓRIO:** Criar item vazio na própria fila para executar (framework precisa de pelo menos 1 item)
  - **Estrutura completa:** INIT → FILA (cria item vazio + popula fila do performer) → LOOP STATION → END PROCESS
  - **Nomenclatura:** `prj_AFYA_ID15_01_SAP_DISP` (usar sufixo `_DISP`)
  - **Características:**
    - Lógica de preenchimento da fila é complexa (múltiplas fontes, conciliações, validações extensas)
    - Pode ser um robô mais simples que apenas prepara dados
    - Usa framework para preparar dados e popular fila do performer
- **Performer** (`robot2/`):
  - **Função:** Processa itens da fila populada pelo dispatcher
  - **Fila compartilhada:** 
    - O dispatcher popula usando `FilaProcessamentoPerformer` no seu Config.xlsx
    - O performer lê usando `FilaProcessamento` no seu Config.xlsx (mesma tabela, nomes diferentes)
    - Ambos usam o mesmo `CaminhoBancoSqlite` (mesmo banco SQLite)
  - **Nomenclatura:** `prj_AFYA_ID15_02_TOTVS_PERF` (usar sufixo `_PERF`)
  - **Características:**
    - Recebe dados já preparados do dispatcher
    - Foca apenas em processar os itens da fila

**3. Performer + Performer (Cadeia Sequencial)**
- **Performer 1** (`robot1/`):
  - **Função:** Processa itens e pode popular fila do Performer 2
  - **Nomenclatura:** `prj_AFYA_ID15_01_SAP` (apenas numeração sequencial, sem sufixo)
  - **Características:**
    - Processa seus próprios itens
    - Pode ter função de output que será usada no Performer 2
    - Pode popular diretamente a fila do Performer 2
- **Performer 2** (`robot2/`):
  - **Função:** Processa itens da fila do Performer 1
  - **Nomenclatura:** `prj_AFYA_ID15_02_TOTVS` (apenas numeração sequencial, sem sufixo)
  - **Características:**
    - Recebe dados do Performer 1
    - Executa processamento sequencial após o Performer 1
- **Nota importante:** Se Performer 1 tem função principal de alimentar Performer 2, ele se torna um Dispatcher (usar nomenclatura com `_DISP`)

#### Estrutura de Pastas e Arquivos

**Standalone:**
```
specs/001-[nome]/
├── spec.md              # ARQUIVO PRINCIPAL
├── selectors.md
├── business-rules.md
├── tests.md
├── tasks.md
└── DDP/
```

**Múltiplos Robôs:**
```
specs/001-[nome]/
├── robot1/              # Robô 1 (Dispatcher ou Performer)
│   ├── spec.md          # ARQUIVO PRINCIPAL do robô 1
│   ├── selectors.md     # Seletores específicos do robô 1
│   ├── business-rules.md # Regras de negócio específicas do robô 1
│   └── tests.md         # Testes específicos do robô 1
├── robot2/              # Robô 2 (Performer)
│   ├── spec.md          # ARQUIVO PRINCIPAL do robô 2
│   ├── selectors.md     # Seletores específicos do robô 2
│   ├── business-rules.md # Regras de negócio específicas do robô 2
│   └── tests.md         # Testes específicos do robô 2
├── tasks.md             # Compartilhado - lista plana com referência ao robô
└── DDP/                 # Compartilhado
```

#### Regras Específicas por Tipo

**Para Dispatcher:**
- **OBRIGATÓRIO:** No método `add_to_queue()`, criar um item vazio na própria fila ANTES de popular a fila do performer:
  ```python
  @classmethod
  def add_to_queue(cls):
      # OBRIGATÓRIO: Criar item vazio para que o framework execute
      # O framework precisa de pelo menos 1 item na fila para executar
      QueueManager.insert_new_queue_item(
          arg_strReferencia="DISPATCHER_INIT",
          arg_dictInfAdicional={}
      )
      
      # Depois, popular fila do performer
      # ... código para ler dados, fazer conciliações, validações ...
      # ... código para popular fila do performer usando fila compartilhada ...
  ```
- **Fila compartilhada (para popular o performer):**
  - No Config.xlsx do dispatcher existe a configuração `FilaProcessamentoPerformer` (ou similar)
  - Essa é a fila que o dispatcher deve preencher para o performer processar
  - Usar o mesmo `CaminhoBancoSqlite` configurado no Config.xlsx
  - O dispatcher popula essa fila usando `FilaProcessamentoPerformer` como nome da tabela
- **Fila própria do dispatcher:**
  - O dispatcher também tem sua própria `FilaProcessamento` no Config.xlsx (para o item vazio)
- **Item vazio:** Pode ter qualquer referência (ex: "DISPATCHER_INIT"), mas deve existir na fila própria do dispatcher para o framework executar

**Para Performer:**
- **Fila compartilhada (recebe do dispatcher/performer anterior):**
  - No Config.xlsx do performer, a configuração `FilaProcessamento` é a mesma fila que o dispatcher/performer anterior preencheu
  - O dispatcher/performer anterior preenche usando `FilaProcessamentoPerformer` (ou similar)
  - O performer lê usando `FilaProcessamento` (mesma tabela, nomes diferentes nos configs)
  - Usar o mesmo `CaminhoBancoSqlite` configurado no Config.xlsx (mesmo banco SQLite)
- **Configuração no Config.xlsx do Performer:**
  - `CaminhoBancoSqlite`: Mesmo caminho do dispatcher/performer anterior
  - `FilaProcessamento`: Nome da tabela que corresponde à `FilaProcessamentoPerformer` do dispatcher/performer anterior
- **Não precisa criar item vazio:** Recebe itens da fila compartilhada populada pelo robô anterior
- **Se recebe de outro Performer:** Pode receber dados diretamente do Performer anterior (função de output)

**Para Tasks.md (compartilhado):**
- **Estrutura:** Lista plana de tasks
- **Campo obrigatório:** Cada task deve ter campo "Robô:" indicando:
  - `robot1` - se a task é do robô 1
  - `robot2` - se a task é do robô 2
  - `raiz` - se standalone
- **Organização:** Agrupar visualmente - todas tasks do robot1 primeiro, depois robot2
- **Exemplo:**
  ```markdown
  ### Task 1.1: Inicializar Sistemas
  - **Robô:** robot1
  - **Descrição:** ...
  
  ### Task 1.2: Preencher Fila
  - **Robô:** robot1
  - **Descrição:** ...
  
  ### Task 2.1: Processar Item
  - **Robô:** robot2
  - **Descrição:** ...
  ```

**Para Spec.md (cada robô tem o seu):**
- **Seção obrigatória:** "Arquitetura de Robôs" no início do spec.md deve conter:
  - **Tipo:** Standalone / Dispatcher / Performer
  - **Este robô é:** [Descrição breve do papel deste robô]
  - **Recebe dados de:** [Nome do robô anterior que alimenta este robô, se Performer. Ex: "robot1" ou "N/A" se Standalone/Dispatcher]
  - **Alimenta:** [Nome do robô seguinte que este robô alimenta, se Dispatcher ou Performer que alimenta outro. Ex: "robot2" ou "N/A" se não alimenta nenhum]
  - **Ordem na cadeia:** [1/2/3... se parte de múltiplos robôs, ou "1" se Standalone]
  - **Nome da pasta do robô:** [robot1 / robot2 / etc. ou "raiz" se standalone]
- **Observações sobre arquitetura:**
  - Se Dispatcher: mencionar que precisa criar item vazio na própria fila para executar
  - Se Performer: mencionar de onde recebe os dados e como acessa a fila compartilhada
  - Se parte de cadeia: mencionar a ordem de execução e dependências

#### Nomenclatura de Projetos

**Dispatcher + Performer:**
- Usar sufixos `_DISP` e `_PERF`
- Exemplo: `prj_AFYA_ID15_01_SAP_DISP` → `prj_AFYA_ID15_02_TOTVS_PERF`

**Performer + Performer:**
- Apenas numeração sequencial (sem sufixos)
- Exemplo: `prj_AFYA_ID15_01_SAP` → `prj_AFYA_ID15_02_TOTVS`

**Standalone:**
- Nomenclatura normal sem sufixos especiais
- Exemplo: `prj_AFYA_ID15`

#### Geração de Framework

- **Standalone:** Gera em `generated/[nome-automacao]/`
- **Múltiplos:** Gera em `generated/[nome-automacao]-robot1/`, `generated/[nome-automacao]-robot2/`, etc.
- **Comando:** `/t2c.implement` detecta automaticamente a estrutura
- **Geração seletiva:** Pode gerar todos ou apenas um robô específico:
  - `/t2c.implement specs/001-[nome]` - Gera todos os robôs
  - `/t2c.implement specs/001-[nome] --robot robot1` - Gera apenas robot1

#### Guia de Análise para Decisão de Arquitetura

Ao analisar o DDP, a LLM deve realizar uma análise contextual considerando os seguintes aspectos:

**1. Análise de Complexidade do LOOP STATION:**
   - Quantas etapas o LOOP STATION possui? (contar etapas do DDP)
   - Quantas regras de negócio estão envolvidas? (VAL*, COND*, REG*)
   - Quantas integrações diferentes são necessárias? (sistemas UI, APIs, bancos de dados)
   - A complexidade é gerenciável em um único robô ou seria mais organizado dividir?
   - Existem fases logicamente distintas que poderiam ser separadas?

**2. Análise da Complexidade da Preparação de Dados (FILA):**
   - A lógica de preenchimento da fila é simples (leitura direta de Excel/CSV) ou complexa?
   - São necessárias conciliações entre múltiplas fontes de dados?
   - Há validações extensas ou enriquecimento de dados (APIs, consultas complexas)?
   - A preparação de dados é significativamente mais complexa que o processamento em si?
   - A preparação poderia ser feita de forma independente e assíncrona?

**3. Análise de Separação Lógica e Responsabilidades:**
   - O processo tem fases com responsabilidades claramente distintas?
   - Um robô prepararia dados enquanto outro executaria ações em sistemas diferentes?
   - A separação por sistema traria benefícios claros (manutenção, testes, evolução independente)?
   - As etapas estão fortemente acopladas ou podem ser separadas sem criar dependências complexas?

**4. Análise de Benefícios de Organização e Manutenção:**
   - A separação facilitaria significativamente a manutenção do código?
   - Cada robô teria responsabilidades bem definidas e distintas?
   - O processo pode evoluir de forma independente em cada robô?
   - A separação adicionaria complexidade desnecessária ou traria benefícios claros?

**5. Análise de Processos Assíncronos e Controle de Retry:**
   - O processo envolve etapas de verificação manual ou aguardar resposta de sistemas externos?
   - Há necessidade de retry control diferenciado entre fases?
   - Uma fase pode ser executada independentemente da outra?

**6. Análise de Modularização:**
   - Existem etapas opcionais que poderiam ser habilitadas/desabilitadas sem modificar código?
   - A separação permitiria flexibilidade na execução de partes do processo?

**7. Síntese e Decisão Final:**
   - **Pesar todos os fatores acima** - não há uma regra binária
   - Considerar o contexto completo do processo
   - Avaliar se os benefícios da separação superam o overhead de gerenciar múltiplos robôs
   - Decidir baseado no que faz mais sentido para este processo específico
   - Documentar a justificativa da decisão na seção "Arquitetura de Robôs" do spec.md

**⚠️ LEMBRE-SE:** Nem sempre ter 2 sistemas UI significa necessariamente 2 robôs. A decisão deve ser baseada na análise cuidadosa de todos os aspectos, não em regras rígidas.

#### Exemplos Práticos

**Exemplo 1: Standalone (Decisão Clara)**
- **Processo:** Ler Excel, validar CPF, inserir no sistema SAP
- **Análise:** 
  - LOOP STATION simples (3-4 etapas)
  - Preparação de fila direta (leitura Excel)
  - Processo linear e coeso
  - Sem benefício claro em separar
- **Decisão:** Standalone
- **Estrutura:** `specs/001-inserir-cpf/spec.md` (na raiz)

**Exemplo 2: Dispatcher + Performer (Decisão Clara)**
- **Processo:** Ler múltiplos Excels, fazer conciliação complexa entre eles, validar dados, enriquecer com API, depois processar no SAP
- **Análise:**
  - Preparação de dados muito complexa (múltiplas fontes, conciliações, validações, enriquecimento)
  - Processamento no SAP é mais simples que a preparação
  - Benefício claro: preparação pode ser feita independentemente
  - Manutenção facilitada: lógica de preparação separada da execução
- **Decisão:** Dispatcher + Performer
- **Estrutura:**
  - `specs/001-processo/robot1/` (Dispatcher - prepara dados)
  - `specs/001-processo/robot2/` (Performer - processa no SAP)

**Exemplo 3: Performer + Performer (Decisão Clara)**
- **Processo:** Processar notas fiscais no sistema A, depois processar no sistema B
- **Análise:**
  - Dois sistemas diferentes com responsabilidades distintas
  - Processamento sequencial claro
  - Benefício: cada robô foca em um sistema específico
  - Manutenção facilitada: mudanças em um sistema não afetam o outro
- **Decisão:** Performer + Performer
- **Estrutura:**
  - `specs/001-processo/robot1/` (Performer 1 - sistema A)
  - `specs/001-processo/robot2/` (Performer 2 - sistema B)

**Exemplo 4: Caso que Requer Análise Cuidadosa (2 Sistemas UI)**
- **Processo:** Consultar dados no sistema A, validar informações, inserir no sistema B
- **Análise Contextual:**
  - **Fator 1:** Dois sistemas UI diferentes
  - **Fator 2:** Processo linear e simples (3-4 etapas)
  - **Fator 3:** Lógica coesa - consulta e inserção fazem parte do mesmo fluxo
  - **Fator 4:** Sem necessidade de retry diferenciado
  - **Fator 5:** Separação adicionaria overhead sem benefício claro
- **Decisão:** Standalone (apesar de ter 2 sistemas UI)
- **Justificativa:** O processo é simples e coeso. Separar criaria complexidade desnecessária sem ganhos em manutenção ou organização.
- **Estrutura:** `specs/001-processo/spec.md` (na raiz)

**Exemplo 5: Caso que Requer Análise Cuidadosa (Processo Médio)**
- **Processo:** Ler Excel, validar dados, processar no sistema A (10 etapas), depois processar no sistema B (5 etapas)
- **Análise Contextual:**
  - **Fator 1:** LOOP STATION extenso (15 etapas no total)
  - **Fator 2:** Dois sistemas diferentes
  - **Fator 3:** Processamento no sistema A é significativamente mais complexo que no B
  - **Fator 4:** Separação facilitaria manutenção (cada robô foca em um sistema)
  - **Fator 5:** Benefício claro: mudanças no sistema A não afetam o B
- **Decisão:** Performer + Performer
- **Justificativa:** Apesar de ser um processo linear, a complexidade e a separação por sistema trazem benefícios claros de manutenção e organização.
- **Estrutura:**
  - `specs/001-processo/robot1/` (Performer 1 - sistema A, 10 etapas)
  - `specs/001-processo/robot2/` (Performer 2 - sistema B, 5 etapas)

**⚠️ OBSERVAÇÃO IMPORTANTE:** Os exemplos 4 e 5 mostram que a decisão não é baseada em uma única característica (como "ter 2 sistemas UI"), mas sim na análise cuidadosa de todos os fatores do processo específico.

### 14. Estimativas de Tempo para Tasks

**⚠️ IMPORTANTE:** Ao gerar tasks.md (comando `/t2c.tasks`), a LLM DEVE incluir estimativas de tempo realistas para cada tarefa.

#### Base de Estimativa

- **Perfil considerado:** Desenvolvedor pleno (não mencionar isso no documento, apenas usar como referência interna)
- **Formato:** Horas (ex: "2 horas", "4 horas", "0.5 horas", "8 horas")
- **Precisão:** Usar valores inteiros ou meias horas (0.5, 1, 1.5, 2, etc.)

#### Fatores a Considerar na Estimativa

**1. Complexidade da Tarefa:**
- **Simples (0.5-2h):** Leitura de arquivo, validação simples, configuração básica
- **Média (2-4h):** Integração com sistema, múltiplas validações, lógica de negócio moderada
- **Complexa (4-8h):** Conciliações, múltiplas integrações, lógica complexa, tratamento de erros extenso
- **Muito Complexa (8h+):** Arquitetura complexa, múltiplos sistemas, regras de negócio extensas

**2. Número de Etapas:**
- Cada etapa do DDP adiciona tempo
- Considerar: navegação, preenchimento de formulários, validações, tratamento de erros
- Estimativa base: 0.5-1h por etapa simples, 1-2h por etapa complexa

**3. Integrações:**
- **Clicknium/Seletores:** +0.5-1h (criação e teste de seletores)
- **APIs:** +1-2h (integração e tratamento de erros)
- **Banco de Dados:** +1-2h (queries e tratamento)
- **E-mail:** +0.5h (configuração e template)
- **T2CTracker:** +0.5-1h (configuração de steps)

**4. Regras de Negócio:**
- **Cada validação (VAL*):** +0.5-1h
- **Cada condição especial (COND*):** +1-2h
- **Cada regra de processamento (REG*):** +1-3h

**5. Tratamento de Erros:**
- Tratamento básico: +0.5h por tipo de erro
- Tratamento complexo: +1-2h por tipo de erro

**6. Testes e Ajustes:**
- Incluir 20-30% do tempo de desenvolvimento para testes e ajustes

#### Estimativas de Referência por Tipo de Task

**INIT - Inicialização:**
- **Inicializar 1 sistema simples:** 1-2h
- **Inicializar 1 sistema complexo:** 2-4h
- **Inicializar múltiplos sistemas:** 3-6h
- **Preencher fila simples (leitura Excel/CSV):** 1-2h
- **Preencher fila complexa (conciliações, validações):** 4-8h
- **Preencher fila dispatcher (item vazio + popular performer):** 2-4h

**LOOP STATION - Processamento:**
- **Etapa simples (1 ação):** 1-2h
- **Etapa média (2-3 ações):** 2-4h
- **Etapa complexa (4+ ações, validações):** 4-8h
- **Grupo lógico de etapas (3-5 etapas relacionadas):** 6-12h
- **Processamento completo com múltiplas regras:** 8-16h

**END PROCESS - Finalização:**
- **Fechar sistemas:** 0.5-1h
- **Enviar e-mail final:** 1-2h (incluindo template e formatação)

#### Estrutura do tasks.md com Estimativas

**1. Tabela de Visão Geral (no início):**
- Resumo executivo (total de tasks, tempo total, distribuição)
- Top 5 tasks com maior estimativa
- Estimativas por fase (INIT, LOOP STATION, END PROCESS)
- Estimativas por robô (se múltiplos robôs)

**2. Cada Task:**
- Campo "Estimativa:" com tempo e justificativa breve
- Justificativa deve mencionar: complexidade, número de etapas, integrações, regras de negócio

#### Exemplo de Estimativa

```markdown
### Task 2.1: Login e Navegação no Sistema SAP
- **Robô:** robot1
- **Consolida etapas do spec:** `robot1/spec.md` - LOOP STATION: Etapas 1-3
- **Arquivo:** T2CProcess.py
- **Método:** execute()
- **Descrição:** Realizar login no SAP, validar acesso, navegar até tela de processamento
- **Estimativa:** 3 horas - Login (1h) + Validação de acesso (0.5h) + Navegação com seletores Clicknium (1h) + Tratamento de erros (0.5h)
- **Status:** [ ] Pendente / [ ] Em Progresso / [ ] Concluído
```

#### Cálculo da Tabela de Visão Geral

Ao gerar tasks.md, calcular automaticamente:
- **Total de tasks:** Soma de todas as tasks
- **Tempo total:** Soma de todas as estimativas
- **Top 5 tasks:** Ordenar por estimativa (maior para menor)
- **Por fase:** Agrupar tasks por fase e somar estimativas
- **Por robô:** Agrupar tasks por robô e somar estimativas (se múltiplos robôs)
- **Percentuais:** Calcular % de cada task/fase/robô em relação ao total

---

## 📚 PARTE 2: ESPECIFICAÇÃO COMPLETA DO FRAMEWORK

### Visão Geral

O Framework T2C é uma estrutura completa para automação de processos (RPA) baseada em Python, utilizando BotCity como plataforma principal. O framework fornece uma arquitetura padronizada que gerencia automaticamente:

- **Ciclo de vida completo da execução** (inicialização, processamento, finalização)
- **Gerenciamento de fila** (SQLite)
- **Tratamento de erros** (business e system exceptions)
- **Geração de relatórios** (analítico e sintético)
- **Envio de e-mails** (inicial, final, erros)
- **Rastreamento de execuções** (T2CTracker)
- **Integração com Maestro** (BotCity)
- **Logging estruturado**

**Versão do Framework:** 2.2.3

### Arquitetura e Fluxo de Execução

```
┌─────────────────────────────────────────────────────────────┐
│                    PONTO DE ENTRADA                          │
│                    bot.py -> action()                        │
└───────────────────────────┬───────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│             1. INICIALIZAÇÃO (Initialization)               │
│  - Carrega configurações (Config.xlsx)                      │
│  - Conecta com Maestro/Tracker                              │
│  - Inicializa aplicações (InitAllApplications)              │
│  - Preenche fila (add_to_queue)                             │
│  - Envia e-mail inicial                                     │
└───────────────────────────┬───────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│             2. LOOP DE PROCESSAMENTO (LoopStation)          │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  while (existem itens na fila):                     │   │
│  │    - Captura próximo item (GetTransaction)          │   │
│  │    - Loop de tentativas (MaxRetryNumber)            │   │
│  │      ┌───────────────────────────────────────────┐ │   │
│  │      │  try:                                      │ │   │
│  │      │    - Process.execute() ← SEU CÓDIGO AQUI │ │   │
│  │      │    - Atualiza status (SUCESSO)            │ │   │
│  │      │  except BusinessRuleException:             │ │   │
│  │      │    - Trata erro de negócio                │ │   │
│  │      │  except Exception:                         │ │   │
│  │      │    - Trata erro de sistema                │ │   │
│  │      │    - Reinicia aplicações                   │ │   │
│  │      │    - Tenta novamente                       │ │   │
│  │      └───────────────────────────────────────────┘ │   │
│  └─────────────────────────────────────────────────────┘   │
└───────────────────────────┬───────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│             3. FINALIZAÇÃO (EndProcess)                     │
│  - Fecha aplicações (CloseAllApplications)                  │
│  - Gera relatórios (Analítico e Sintético)                  │
│  - Envia e-mail final                                       │
│  - Finaliza task no Maestro                                 │
└─────────────────────────────────────────────────────────────┘
```

### Pontos de Entrada para Código Personalizado

#### 1. T2CProcess.execute() - ⭐ PRINCIPAL PONTO DE ENTRADA

**Localização:** `{{PROJECT_NAME}}/classes_t2c/framework/T2CProcess.py`

**O que é:** Este é o método principal onde você deve colocar toda a lógica de processamento de cada item da fila.

**Como usar:**
```python
@classmethod
def execute(cls):
    var_dictItem = GetTransaction.var_dictQueueItem
    var_strReferencia = var_dictItem['referencia']
    var_dictInfoAdicional = var_dictItem['info_adicionais']
    
    Maestro.write_log(f'Processando item: {var_strReferencia}')
    # SEU CÓDIGO AQUI
    Maestro.write_log('Process Finished')
```

**Importante:**
- Chamado automaticamente para cada item da fila
- Framework gerencia tentativas e tratamento de erros
- Use `BusinessRuleException` para erros de negócio (não tenta novamente)
- Use `Exception` genérica para erros de sistema (tenta novamente)
- **Ver PARTE 5 para exemplo completo**

#### 2. T2CInitAllApplications.add_to_queue() - Preencher Fila

**Localização:** `{{PROJECT_NAME}}/classes_t2c/framework/T2CInitAllApplications.py`

**O que é:** Método chamado apenas uma vez no início para adicionar itens à fila de processamento.

**Como usar:**
```python
@classmethod
def add_to_queue(cls):
    # Ler dados e inserir na fila
    import pandas as pd
    df = pd.read_excel('dados.xlsx')
    
    for index, row in df.iterrows():
        QueueManager.insert_new_queue_item(
            arg_strReferencia=str(row['id']),
            arg_dictInfAdicional={'campo1': row['campo1'], 'campo2': row['campo2']}
        )
```
- **Ver PARTE 5 para exemplo completo**

#### 3. T2CInitAllApplications.execute() - Inicializar Aplicações

**Localização:** `{{PROJECT_NAME}}/classes_t2c/framework/T2CInitAllApplications.py`

**O que é:** Método para inicializar todas as aplicações necessárias (navegadores, programas desktop, etc.).

**Importante:**
- Este método é chamado na inicialização e também após erros de sistema
- `arg_boolFirstRun=True` apenas na primeira vez
- Use `InitAllSettings.var_botWebbot` para manipular navegador
- Use `InitAllSettings.var_botDesktopbot` para manipular desktop
- Implementar loop de tentativas (ver PARTE 8)
- **Ver PARTE 5 para exemplo completo**

#### 4. T2CCloseAllApplications.execute() - Fechar Aplicações

**Localização:** `{{PROJECT_NAME}}/classes_t2c/framework/T2CCloseAllApplications.py`

**O que é:** Método para fechar todas as aplicações no final da execução.

**Importante:**
- Fechar navegador: `InitAllSettings.var_botWebbot.stop_browser()`
- Fechar aplicações desktop conforme necessário
- Implementar loop de tentativas (ver PARTE 8)

### Configuração Inicial

#### Arquivo de Configuração: Config.xlsx

**Localização:** `{{PROJECT_NAME}}/resources/config/Config.xlsx`

Este arquivo Excel contém 4 abas com todas as configurações do framework:

**Aba "Settings":**
- `NomeCliente` - Nome do cliente
- `NomeProcesso` - Nome do processo/robô
- `DescricaoProcesso` - Descrição do processo
- `FilaProcessamento` - Nome da tabela de fila (fila própria do robô)
- `FilaProcessamentoPerformer` - (Opcional) Nome da tabela de fila do performer (usado por dispatcher para popular fila do performer)
- `NomeTabelaDadosExecucao` - Nome da tabela de execução
- `NomeTabelaDadosItens` - Nome da tabela de itens
- `CaminhoBancoSqlite` - Caminho do banco SQLite
- `CaminhoExceptionScreenshots` - Pasta para screenshots de erro
- `CaminhoPastaRelatorios` - Pasta para relatórios
- `MaxRetryNumber` - Número máximo de tentativas
- `MaxConsecutiveSystemExceptions` - Máximo de erros consecutivos
- `AtivarT2CTracker` - Ativar tracker (SIM/NÃO)
- `AtivarClicknium` - Ativar Clicknium (SIM/NÃO)
- `IniciarRobotStream` - Iniciar stream (SIM/NÃO)
- `GravarTela` - Gravar tela (SIM/NÃO)
- `CapturarScreenshot` - Capturar screenshot em erros (SIM/NÃO)
- `BackupSqlite` - Fazer backup SQLite (SIM/NÃO)
- `CaminhoBackupSqlite` - Caminho do backup
- `EmailInicial` - Enviar e-mail inicial (SIM/NÃO)
- `EmailFinal` - Enviar e-mail final (SIM/NÃO)
- `EmailCadaErro` - Enviar e-mail a cada erro (SIM/NÃO)
- `EmailErroInicializacao` - Enviar e-mail em erro de inicialização (SIM/NÃO)
- `EmailDestinatarios` - Destinatários (separados por ;)

**Aba "Constants":**
- Constantes utilizadas no processo (definidas pelo desenvolvedor)

**Aba "Credentials":**
- `MaestroLogin` - Login do Maestro
- `MaestroKey` - Chave do Maestro
- `MaestroServer` - Servidor do Maestro
- `CRED_CLICKNIUM` - Label da credencial Clicknium
- `CRED_KEY_CLICKNIUM` - Key da credencial Clicknium
- `CRED_LABEL_TRACKER` - Label da credencial Tracker
- `CRED_KEY_TOKEN_TRACKER` - Key do token Tracker
- `CRED_KEY_LAYOUT_TRACKER` - Key do layout Tracker

**Aba "Assets":**
- Assets do Tracker (pasta e nome do asset)

**Como acessar as configurações no código:**
```python
from {{PROJECT_NAME}}.classes_t2c.framework.T2CInitAllSettings import T2CInitAllSettings as InitAllSettings

# Acessar qualquer configuração
var_strNomeProcesso = InitAllSettings.var_dictConfig["NomeProcesso"]
var_intMaxTentativas = InitAllSettings.var_dictConfig["MaxRetryNumber"]
```

### Gerenciamento de Fila

#### Estrutura da Tabela de Fila

O framework espera uma tabela SQLite com a seguinte estrutura:

```sql
CREATE TABLE tbl_Fila_Processamento(
    id INTEGER PRIMARY KEY,
    referencia VARCHAR(200),
    datahora_criado VARCHAR(50),
    nome_maquina VARCHAR(200),
    info_adicionais TEXT,  -- JSON com informações adicionais
    status VARCHAR(100),   -- NEW, ON QUEUE, RUNNING, SUCESSO, BUSINESS ERROR, APP ERROR
    obs VARCHAR(500),
    ultima_atualizacao DATETIME
);
```

**Status possíveis:**
- `NEW` - Item novo, aguardando processamento
- `ON QUEUE` - Item reservado para processamento
- `RUNNING` - Item em processamento
- `SUCESSO` - Item processado com sucesso
- `BUSINESS ERROR` - Erro de regra de negócio
- `APP ERROR` - Erro de aplicação/sistema

#### Métodos Principais

**1. Inserir Item na Fila:**
```python
from {{PROJECT_NAME}}.classes_t2c.queue.T2CQueueManager import T2CQueueManager as QueueManager

# Criar dicionário com informações adicionais
var_dictInfoAdicional = {
    'campo1': 'valor1',
    'campo2': 'valor2',
    'ID_ITEM_TRACKER': '123'  # Se usar Tracker
}

# Inserir item
QueueManager.insert_new_queue_item(
    arg_strReferencia='REF001',  # Identificador único
    arg_dictInfAdicional=var_dictInfoAdicional
)
```

**2. Atualizar Status do Item:**
```python
# Sucesso (sem exceção)
QueueManager.update_status_item()

# Erro de negócio
from {{PROJECT_NAME}}.classes_t2c.utils.T2CExceptions import BusinessRuleException
try:
    # seu código
    pass
except BusinessRuleException as err:
    QueueManager.update_status_item(
        arg_excExcecao=err,
        arg_strObs=str(err)
    )

# Erro de sistema
except Exception as err:
    QueueManager.update_status_item(
        arg_excExcecao=err,
        arg_strObs=str(err)
    )
```

### Inicialização de Aplicações

#### Inicializar Navegador Web

```python
from botcity.web import Browser

InitAllSettings.initiate_web_manipulator(
    arg_boolHeadless=False,
    arg_brwBrowserEscolhido=Browser.CHROME,  # CHROME, EDGE, FIREFOX, UNDETECTED_CHROME
    arg_strPastaDownload=r"C:\Downloads"
)

InitAllSettings.var_botWebbot.navigate_to("https://exemplo.com")
```

**Browsers disponíveis:** `Browser.CHROME`, `Browser.EDGE`, `Browser.FIREFOX`, `Browser.UNDETECTED_CHROME`

#### Clicknium

Se `AtivarClicknium=SIM` no Config.xlsx (ver PARTE 4 para uso de seletores):
- Framework detecta automaticamente a pasta `.locator`
- VSCode: busca na raiz do projeto
- Maestro: busca em `resources/.locator`

### Integrações

#### 1. Conexão com Maestro (BotCity)

**Classe:** `T2CMaestro`

**Localização:** `{{PROJECT_NAME}}/classes_t2c/utils/T2CMaestro.py`

**Métodos úteis:**
- `Maestro.write_log()` - Escrever logs (ver PARTE 1)
- `Maestro.get_credential()` - Obter credenciais
- `Maestro.is_interrupted()` - Verificar interrupção
- `Maestro.finish_task()` - Finalizar task

#### 2. Conexão com T2CTracker

**Classe:** `T2CTracker`

**Localização:** `{{PROJECT_NAME}}/classes_t2c/utils/T2CTracker.py`

**Uso automático:** O framework configura e usa o Tracker automaticamente se `AtivarT2CTracker=SIM`.

**Métodos úteis (geralmente não precisa usar diretamente):**
- `Tracker.next_step()` - Avançar step (framework faz automaticamente)
- `Tracker.get_asset()` - Obter asset do Tracker

---

## 🏗️ PARTE 3: ESTRUTURA DO FRAMEWORK

### Estrutura de Diretórios

```
<nome-automacao>/
├── {{PROJECT_NAME}}/
│   ├── __init__.py
│   ├── __main__.py
│   ├── bot.py
│   └── classes_t2c/
│       ├── __init__.py
│       ├── framework/
│       │   ├── __init__.py
│       │   ├── T2CProcess.py                    # ⭐ GERADO com código customizado
│       │   ├── T2CInitAllApplications.py       # ⭐ GERADO com código customizado
│       │   ├── T2CCloseAllApplications.py     # ⭐ GERADO com código customizado
│       │   ├── T2CLoopStation.py               # Copiado do framework base
│       │   ├── T2CInitialization.py            # Copiado do framework base
│       │   ├── T2CEndProcess.py                # Copiado do framework base
│       │   ├── T2CInitAllSettings.py           # Copiado do framework base
│       │   ├── T2CGetTransaction.py            # Copiado do framework base
│       │   └── T2CKillAllProcesses.py          # Copiado do framework base
│       ├── queue/
│       │   └── T2CQueueManager.py              # Copiado do framework base
│       ├── dados_execucao/
│       │   └── T2CDadosExecucao.py             # Copiado do framework base
│       ├── relatorios/
│       │   └── T2CRelatorios.py                # Copiado do framework base
│       ├── email/
│       │   └── send/
│       │       └── T2CSendEmail.py              # Copiado do framework base
│       └── utils/
│           ├── T2CMaestro.py                   # Copiado do framework base
│           ├── T2CTracker.py                   # Copiado do framework base
│           ├── T2CExceptions.py               # Copiado do framework base
│           ├── T2CGenericReusable.py           # Copiado do framework base
│           ├── T2CBackupSqlite.py              # Copiado do framework base
│           ├── T2CRobotStream.py              # Copiado do framework base
│           └── T2CScreenRecorder.py            # Copiado do framework base
│   └── resources/
│       ├── config/
│       │   └── Config.xlsx                      # ⭐ GERADO baseado em config/*.md
│       ├── sqlite/
│       │   └── banco_dados.db                  # Criado automaticamente
│       ├── templates/
│       │   ├── Email_Inicio.txt                 # Copiado do framework base
│       │   ├── Email_Final.txt                  # Copiado do framework base
│       │   ├── Email_ErroEncontrado.txt         # Copiado do framework base
│       │   ├── Relatorio_Analitico.xlsx         # Copiado do framework base
│       │   └── Relatorio_Sintetico.xlsx         # Copiado do framework base
│       └── scripts/
│           └── analitico_sintetico/
│               ├── Script_Select_Analitico.sql  # Copiado do framework base
│               ├── Script_Select_Sintetico.sql  # Copiado do framework base
│               └── Script_Update_DadosExecucao.sql # Copiado do framework base
├── requirements.txt                             # ⭐ GERADO
├── setup.py                                     # ⭐ GERADO
├── README.md                                    # ⭐ GERADO
└── .gitignore                                   # ⭐ GERADO
```

### Arquivos Gerados vs Copiados

**Arquivos Gerados (com código customizado):**
- `{{PROJECT_NAME}}/bot.py` - Bot principal
- `{{PROJECT_NAME}}/classes_t2c/framework/T2CProcess.py` - Lógica principal
- `{{PROJECT_NAME}}/classes_t2c/framework/T2CInitAllApplications.py` - Inicialização
- `{{PROJECT_NAME}}/classes_t2c/framework/T2CCloseAllApplications.py` - Finalização
- `{{PROJECT_NAME}}/resources/config/Config.xlsx` - Configurações

**Arquivos Copiados (do framework base):**
- Todos os outros arquivos do framework são copiados de uma referência do framework T2C
- Não devem ser modificados
- São parte do framework core

### Variáveis de Template

Ao gerar os arquivos, substitua:
- `{{PROJECT_NAME}}` - Nome do projeto (ex: `projeto_ia_spec`)
- `{{IMPORTS}}` - Imports necessários baseados nas specs
- `{{VALIDACOES_ENTRADA}}` - Código de validações
- `{{CONDICOES_ESPECIAIS}}` - Código de condições especiais
- `{{PROCESSAMENTO_PRINCIPAL}}` - Código principal de processamento
- `{{PREENCHIMENTO_FILA}}` - Código para preencher fila
- `{{INICIALIZACAO_APLICACOES}}` - Código de inicialização
- `{{FECHAMENTO_APLICACOES}}` - Código de fechamento

---

## 📐 PARTE 4: PADRÕES DE CÓDIGO

**Nota:** Para nomenclatura completa, ver PARTE 8. Para tratamento de erros detalhado, ver PARTE 8. Para loops e outras boas práticas, ver PARTE 8.

### Padrões de Código

#### 1. Imports
```python
# Sempre nesta ordem:
# 1. Imports dos módulos T2C
from {{PROJECT_NAME}}.classes_t2c.framework.T2CInitAllSettings import T2CInitAllSettings as InitAllSettings

# 2. Imports dos pacotes externos
from botcity.web import WebBot
```

#### 2. Uso de Seletores Clicknium
```python
from clicknium import clicknium as cc, locator

# Clicar
cc.find_element(locator.pasta.elemento).click()

# Preencher
cc.find_element(locator.pasta.elemento).set_text("texto")

# Ler
texto = cc.find_element(locator.pasta.elemento).get_text()
```

---

## 💡 PARTE 5: EXEMPLOS PRÁTICOS

**Nota:** Estes exemplos focam em padrões únicos. Para conceitos básicos (logging, tratamento de erros, loops), ver PARTE 1 e PARTE 8.

### Exemplo 1: T2CProcess.execute() - Validações e Processamento

```python
@classmethod
def execute(cls):
    var_dictItem = GetTransaction.var_dictQueueItem
    var_strReferencia = var_dictItem['referencia']
    var_dictInfoAdicional = var_dictItem['info_adicionais']
    
    Maestro.write_log(f'Processando item: {var_strReferencia}')

    # VAL001 - Validação de CPF (ver PARTE 8 para uso de raise)
    var_strCpf = var_dictInfoAdicional.get('cpf', '')
    if len(var_strCpf) != 11 or not var_strCpf.isdigit():
        raise BusinessRuleException("CPF inválido ou incompleto")

    # Processamento principal com Clicknium (ver PARTE 4 para seletores)
    cc.find_element(locator.login.campo_usuario).set_text(var_dictInfoAdicional.get('usuario', ''))
    cc.find_element(locator.login.botao_entrar).click()
    
    Maestro.write_log('Process Finished')
```

### Exemplo 2: T2CInitAllApplications.add_to_queue() - Preencher Fila

```python
@classmethod
def add_to_queue(cls):
    import pandas as pd
    df = pd.read_excel('dados.xlsx')
    
    for index, row in df.iterrows():
        QueueManager.insert_new_queue_item(
            arg_strReferencia=str(row['ID']),
            arg_dictInfAdicional={
                'cpf': str(row['CPF']),
                'usuario': str(row['Usuario'])
            }
        )
```

---

## 🔧 PARTE 6: GUIA DE IMPLEMENTAÇÃO

### Fluxo de Geração do Framework

#### 1. Validação de Pré-requisitos

Verificar se todos os arquivos necessários existem:
- `specs/001-*/spec.md` - ARQUIVO PRINCIPAL (Arquitetura completa)
- `specs/001-*/tasks.md`
- `specs/001-*/selectors.md`
- `specs/001-*/business-rules.md`
- `config/*.md`

#### 2. Leitura de Especificações

Ler todas as specs:
- `spec.md` - ARQUIVO PRINCIPAL - Arquitetura completa (INIT, FILA, LOOP STATION, END PROCESS)
- `tasks.md` - Tarefas de implementação
- `selectors.md` - Seletores de UI
- `business-rules.md` - Regras de negócio
- `config/*.md` - Todas as configurações

#### 3. Determinar Nome do Projeto

Obter nome do projeto de `config/base.md` ou usar padrão.

#### 4. Criar Estrutura de Diretórios

Criar estrutura completa em `generated/<nome-automacao>/` conforme estrutura definida acima.

#### 5. Gerar Arquivos Customizados

**5.1. bot.py** - Usar template abaixo, substituir `{{PROJECT_NAME}}`

**5.2. T2CProcess.py** - Usar template abaixo, substituir:
- `{{PROJECT_NAME}}`
- `{{IMPORTS}}` - baseado em selectors.md e spec.md
- `{{VALIDACOES_ENTRADA}}` - baseado em business-rules.md (VAL*)
- `{{CONDICOES_ESPECIAIS}}` - baseado em business-rules.md (COND*)
- `{{PROCESSAMENTO_PRINCIPAL}}` - baseado em tasks.md e spec.md (LOOP STATION)

**5.3. T2CInitAllApplications.py** - Usar template abaixo, substituir:
- `{{PROJECT_NAME}}`
- `{{IMPORTS}}` - baseado em spec.md
- `{{PREENCHIMENTO_FILA}}` - baseado em spec.md (FILA) e tasks.md
- `{{INICIALIZACAO_APLICACOES}}` - baseado em spec.md (INIT) e tasks.md

**5.4. T2CCloseAllApplications.py** - Usar template abaixo, substituir:
- `{{PROJECT_NAME}}`
- `{{IMPORTS}}` - baseado em spec.md
- `{{FECHAMENTO_APLICACOES}}` - baseado em spec.md (END PROCESS) e tasks.md

**5.5. Config.xlsx** - Converter `config/*.md` para Excel (abas: Settings, Constants, Credentials, Assets)

#### 6. Copiar Arquivos do Framework Base

Copiar todos os arquivos do framework que não são customizados (T2CLoopStation.py, T2CInitialization.py, etc.)

#### 7. Gerar Arquivos de Projeto

- `requirements.txt` - Usar template abaixo
- `setup.py` - Gerar baseado no nome do projeto
- `README.md` - Gerar baseado nas specs
- `.gitignore` - Gerar padrão do framework

#### 8. Gerar __init__.py

Gerar todos os `__init__.py` necessários usando template abaixo.

---

## 📝 PARTE 7: TEMPLATES DE CÓDIGO

### Template: bot.py

```python
"""
VERSÃO FRAMEWORK: 2.2.3

AVISO:

Certifique-se de instalar o bot com `pip install -e .` para obter todas as dependências
em seu ambiente Python.

Além disso, se você estiver usando PyCharm ou outro IDE, certifique-se de usar o MESMO interpretador Python
como seu IDE.

Se você receber um erro como:
```
ModuleNotFoundError: No module named 'botcity'
```

Isso significa que você provavelmente está usando um interpretador Python diferente daquele usado para instalar o bot.
Para corrigir isso, você pode:
- Use o mesmo intérprete do seu IDE e instale seu bot com `pip install -e .`
- Use o mesmo intérprete usado para instalar o bot (`pip install -e .`)

Consulte a documentação para obter mais informações em https://documentation.botcity.dev/
"""
# Imports dos modulos T2C (InitAllSettings deve ser o primeiro)
from {{PROJECT_NAME}}.classes_t2c.framework.T2CInitAllSettings import T2CInitAllSettings as InitAllSettings
from {{PROJECT_NAME}}.classes_t2c.utils.T2CMaestro import T2CMaestro as Maestro
from {{PROJECT_NAME}}.classes_t2c.utils.T2CExceptions import *
from {{PROJECT_NAME}}.classes_t2c.framework.T2CInitialization import T2CInitialization as Initialization
from {{PROJECT_NAME}}.classes_t2c.framework.T2CLoopStation import T2CLoopStation as LoopStation
from {{PROJECT_NAME}}.classes_t2c.framework.T2CEndProcess import T2CEndProcess as EndProcess
from {{PROJECT_NAME}}.classes_t2c.dados_execucao.T2CDadosExecucao import T2CDadosExecucao as DadosExecucao
from {{PROJECT_NAME}}.classes_t2c.utils.T2CTracker import T2CTracker as Tracker

# Imports dos pacotes externos
import traceback, sys
from botcity.web import WebBot


class Bot(WebBot):
    """
    Classe que utiliza as funcionalidades da classe WebBot.
    
    Parâmetros:

    Retorna:
    """

    def action(self, execution=None):
        """
        Método principal para execução do bot.

        Parâmetros:
        - execution (objeto): objeto de execução (opcional, default=None).

        Retorna:
        """
        try:
            Maestro.create_conexao_maestro(execution)
            Maestro.write_log("Iniciando execução do processo: " + Maestro.var_strNomeProcesso)

            Initialization.execute()

            LoopStation.execute()
          
        except TerminateException as err:
            var_strTracebackErro = traceback.format_exc()
            print(var_strTracebackErro)
        except Exception as err:
            var_strTracebackErro = traceback.format_exc()
            if InitAllSettings.var_excExceptionInitialization is None:
                InitAllSettings.var_excExceptionProcess = err
            print(var_strTracebackErro)
        

        try:
            EndProcess.execute()
                                                
        except Exception as err:
            # 486 Fim do Processamento com Falha
            if (InitAllSettings.var_dictConfig["AtivarT2CTracker"].upper() == "SIM"): 
                Tracker.finish_process(arg_intStep=486)

            var_strTracebackErro = traceback.format_exc()
            print(var_strTracebackErro)
            Maestro.send_error(err)
            DadosExecucao.refresh_counting_items()
            Maestro.finish_task(arg_boolSucesso=False, arg_strMensagem=f"Task finalizada com erros. Motivo: {var_strTracebackErro}")
            

if __name__ == '__main__':
    if len(sys.argv) >= 5 and str(sys.argv[1]).lower() == "--execution".lower():
        Bot.action(None)
    else:
        Bot.main()
```

### Template: T2CProcess.py

```python
# Imports dos modulos T2C (InitAllSettings deve ser o primeiro)
from {{PROJECT_NAME}}.classes_t2c.framework.T2CInitAllSettings import T2CInitAllSettings as InitAllSettings
from {{PROJECT_NAME}}.classes_t2c.utils.T2CMaestro import T2CMaestro as Maestro, LogLevel, ErrorType
from {{PROJECT_NAME}}.classes_t2c.utils.T2CExceptions import BusinessRuleException, TerminateException
from {{PROJECT_NAME}}.classes_t2c.framework.T2CGetTransaction import T2CGetTransaction as GetTransaction

# Imports dos pacotes externos
{{IMPORTS}}


# Classe responsável pelo processamento principal, necessário preencher com o seu código no método execute
class T2CProcess:
    """
    Classe responsável pelo processamento principal.

    Parâmetros:
    
    Retorna:
    """
    _var_dictConfig = InitAllSettings.var_dictConfig
    _var_botWebbot = InitAllSettings.var_botWebbot
    _var_botDesktopbot = InitAllSettings.var_botDesktopbot


    @classmethod
    def execute(cls):
        """
        Método principal para execução do código.

        Parâmetros:


        Retorna:
        """
        # Obter item atual da fila
        var_dictItem = GetTransaction.var_dictQueueItem
        var_strReferencia = var_dictItem['referencia']
        var_dictInfoAdicional = var_dictItem['info_adicionais']
        
        Maestro.write_log(f'Processando item: {var_strReferencia}')

        # {{VALIDACOES_ENTRADA}}
        
        # {{CONDICOES_ESPECIAIS}}
        
        # {{PROCESSAMENTO_PRINCIPAL}}
        
        Maestro.write_log('Process Finished')
```

### Template: T2CInitAllApplications.py

```python
# Imports dos modulos T2C (InitAllSettings deve ser o primeiro)
from {{PROJECT_NAME}}.classes_t2c.framework.T2CInitAllSettings import T2CInitAllSettings as InitAllSettings
from {{PROJECT_NAME}}.classes_t2c.utils.T2CMaestro import T2CMaestro as Maestro, LogLevel, ErrorType
from {{PROJECT_NAME}}.classes_t2c.utils.T2CExceptions import BusinessRuleException
from {{PROJECT_NAME}}.classes_t2c.queue.T2CQueueManager import T2CQueueManager as QueueManager
from {{PROJECT_NAME}}.classes_t2c.utils.T2CTracker import T2CTracker as Tracker,Item,ItemUpdate
import {{PROJECT_NAME}}.classes_t2c.utils.T2CGenericReusable as GenericReusable

# Imports dos pacotes externos
{{IMPORTS}}

class T2CInitAllApplications:
    """
    Classe feita para Iniciar as aplicações de inicio de processo e também preencher a fila caso seja um processo simples para capturar
    itens que vão para a fila.
        
    Parâmetros:

    Retorna:
    """
    _var_dictConfig:dict = InitAllSettings.var_dictConfig


    @classmethod
    def add_to_queue(cls):
        """
        Adiciona itens à fila no início do processo, se necessário.

        Observação:
        - Código placeholder.
        - Se o seu projeto precisa de mais do que um método simples para subir a sua fila, considere fazer um projeto dispatcher (ver PARTE 1, seção 13 - Arquitetura de Robôs).

        Parâmetros:
        """
        # {{PREENCHIMENTO_FILA}}
        
    
    @classmethod
    def execute(cls, arg_boolFirstRun=False):
        """
        Executa a inicialização dos aplicativos necessários.

        
        Parâmetros:
        - arg_boolFirstRun (bool): indica se é a primeira execução (default=False).
        
        Observação:
        - Edite o valor da variável `var_intMaxTentativas` no arquivo Config.xlsx.
        
        Retorna:
        """
        # 14      Inicializando Aplicações
        if(InitAllSettings.var_dictConfig["AtivarT2CTracker"].upper() == "SIM"):
            Tracker.next_step(arg_intStep=14)

        Maestro.write_log("InitAllApplications Started")

        #Chama o método para subir a fila, apenas se for a primeira vez
        if(arg_boolFirstRun):
            cls.add_to_queue()

        #Edite o valor dessa variável a no arquivo Config.xlsx
        var_intMaxTentativas = cls._var_dictConfig["MaxRetryNumber"]
        
        for var_intTentativa in range(var_intMaxTentativas):
            try:
                Maestro.write_log("Iniciando aplicativos, tentativa " + (var_intTentativa+1).__str__())
                
                # {{INICIALIZACAO_APLICACOES}}

            except BusinessRuleException as err:
                raise err
            except Exception as err:
                Maestro.write_log(GenericReusable.get_computer_usage())
                Maestro.write_log(arg_strMensagemLog="Erro, tentativa " + (var_intTentativa+1).__str__() + ": " + str(err), arg_enumLogLevel=LogLevel.ERROR, arg_enumErrorType=ErrorType.APP_ERROR)

                if(var_intTentativa+1 == var_intMaxTentativas): 
                    raise err
                else: 
                    # Inclua aqui o código responsável para reiniciar ao estado indicado para iniciar as aplicações novamente
                    continue
            else:
                Maestro.write_log("InitAllApplications Finished")
                break
```

### Template: T2CCloseAllApplications.py

```python
# Imports dos modulos T2C (InitAllSettings deve ser o primeiro)
from {{PROJECT_NAME}}.classes_t2c.framework.T2CInitAllSettings import T2CInitAllSettings as InitAllSettings
from {{PROJECT_NAME}}.classes_t2c.utils.T2CMaestro import T2CMaestro as Maestro, LogLevel, ErrorType
import {{PROJECT_NAME}}.classes_t2c.utils.T2CGenericReusable as GenericReusable

# Imports dos pacotes externos
{{IMPORTS}}

class T2CCloseAllApplications:
    """
    Classe responsável pelo fechamento de todos os aplicativos.

    Parâmetros:

    Retorna:
    """
    _var_dictConfig = InitAllSettings.var_dictConfig

    @classmethod
    def execute(cls):
        """
        Executa o fechamento de todos os aplicativos.

        Parâmetros:

        Retorna:
        """
        var_intMaxTentativas = cls._var_dictConfig["MaxRetryNumber"]
        
        for var_intTentativa in range(var_intMaxTentativas):
            try:
                Maestro.write_log("Fechando aplicativos, tentativa " + (var_intTentativa+1).__str__())
                
                # {{FECHAMENTO_APLICACOES}}

            except Exception as err:
                Maestro.write_log(GenericReusable.get_computer_usage())
                Maestro.write_log(arg_strMensagemLog="Erro ao fechar aplicativos, tentativa " + (var_intTentativa+1).__str__() + ": " + str(err), arg_enumLogLevel=LogLevel.ERROR, arg_enumErrorType=ErrorType.APP_ERROR)

                if(var_intTentativa+1 == var_intMaxTentativas): 
                    raise err
                else: 
                    continue
            else:
                Maestro.write_log("CloseAllApplications Finished")
                break
```

### Template: __init__.py

```python
# {{PROJECT_NAME}} - Framework T2C
# Versão: 2.2.3

```

### Template: requirements.txt

```
botcity-framework-core>=1.0.0
botcity-framework-web>=1.0.0
botcity-framework-desktop>=1.0.0
clicknium>=1.0.0
pandas>=1.5.0
openpyxl>=3.0.0
python-dotenv>=0.19.0
```

---

## 📖 PARTE 8: BOAS PRÁTICAS DE DESENVOLVIMENTO

**IMPORTANTE:** Todo o desenvolvimento DEVE obrigatoriamente seguir as boas práticas definidas abaixo.

### Nomenclatura Padrão

#### Projeto

O nome do projeto deve conter:

- **Prefixo:** O prefixo padrão utilizado para o nome de projeto é "prj". Ele indica que se trata de um projeto.
- **Nome da empresa:** Empresa a qual o projeto está sendo desenvolvido
- **Sigla do Processo ou ID:** sigla do processo pode ser letras que identifiquem o processo, por exemplo, pegar as primeiras letras do nome do processo por extenso. Id do processo é quando o RO define um ID para o processo, caso tenha esse ID deverá dar prioridade a ele
- **Sub Sigla do Processo:** A sub sigla do processo refere-se a uma abreviação adicional que pode ser usada para identificar uma subdivisão ou aspecto específico do processo principal. Geralmente, é uma extensão da sigla do processo principal e é usada para diferenciar diferentes etapas, departamentos ou componentes dentro do processo.
- **Número Sequencial:** O número sequencial é uma numeração atribuída de forma consecutiva a cada instância ou ocorrência do processo. Geralmente, é usado para fins de rastreamento e controle, permitindo que as diferentes instâncias sejam identificadas e referenciadas de maneira única.
- **Nome do Sistema:** O nome do sistema refere-se ao nome dado ao conjunto de componentes e elementos que compõem um sistema em particular. Pode se referir a um software, aplicativo, plataforma ou infraestrutura tecnológica que está sendo desenvolvido.

**Estrutura:** `prj_<NomeEmpresa>_<Sigla Processo OU ID>_<SUB SIGLA SE NECESSARIO>_<NumeroSequencial>_<NomeSistema>`

**Exemplos (o sequencial indica a ordem de execução):**
- `prj_AFYA_ID15`
  - `prj_AFYA_ID15_01_SAP`
  - `prj_AFYA_ID15_02_TOTVS`
- `prj_AFYA_LCN`
  - `prj_AFYA_LCN_01_SAP`
  - `prj_AFYA_LCN_02_TOTVS`
- `prj_AFYA_LCN` [CASO NECESSITE DE SUB SIGLA, CASOS RAROS]
  - `prj_AFYA_LCN_PRN_01_TOTVS`
  - `prj_AFYA_LCN_PRN_02_TOTVS`
  - `prj_AFYA_LCN_LANC_01_SAP`

#### Pacotes (Pastas)

Os pacotes (pastas) devem conter:

**Estrutura:** `<nome_pacote>`

Nome do que representa: de preferência resumido.

Exemplo: `classes_t2c`, `framework`, `utils`, `queue`

#### Módulos (Arquivos)

Os módulos (arquivos) devem conter:

Nome do que representa: de preferência resumido.

**Estrutura:** `<nome_módulo>`

Exemplo: `T2CProcess.py`, `T2CQueueManager.py`, `T2CMaestro.py`

#### Classes

As classes devem conter:

Nome do que representa: de preferência resumido.

**Estrutura:** `<NomeClasse>` (PascalCase)

Exemplo: `T2CProcess`, `T2CQueueManager`, `T2CMaestro`

#### Variáveis

As variáveis devem conter:

**Estrutura:** `var_<tipo><ConteúdoNecessário>`

**Prefixo:** iniciar com `var_` para identificação visual

**Tipo da variável:** com no máximo quatro letras (observar principais correlações):
- `var_str*` - Variáveis string
- `var_int*` - Variáveis inteiras
- `var_dict*` - Variáveis dicionário
- `var_bool*` - Variáveis booleanas
- `var_list*` - Variáveis lista
- `var_tpl*` - Variáveis tupla

**Nome do que representa:** de preferência resumido

**TypeHint:** Utilizar TypeHint quando necessário

Exemplo:
```python
var_strReferencia: str = "REF001"
var_intMaxTentativas: int = 3
var_dictItem: dict = {}
var_boolSucesso: bool = True
```

#### Funções/Métodos

As funções/métodos devem conter:

**Estrutura:** `<nome_funcao()>` (snake_case)

Nome do que representa: de preferência resumido.

Exemplo: `execute()`, `add_to_queue()`, `close_all_applications()`

#### Parâmetros de Função/Método

Os parâmetros devem conter:

**Estrutura:** `arg_<tipo><ConteúdoNecessário>`

**Prefixo:** iniciar com `arg_` para identificação visual

**Tipo do parâmetro:** com no máximo quatro letras (observar principais correlações)

**Nome do que representa:** de preferência resumido

**TypeHint:** Utilizar TypeHint quando necessário

Exemplo:
```python
def processar_item(arg_strReferencia: str, arg_dictInfoAdicional: dict):
    pass
```

#### Constantes

As constantes devem conter:

**Estrutura:** `CONS_<TIPO>_<CONTEÚDO_NECESSÁRIO>` (UPPER_CASE)

**Tipo da constante:** com no máximo quatro letras

Nome do que representa: de preferência resumido

**TypeHint:** Utilizar TypeHint quando necessário

Exemplo:
```python
CONS_STR_URL_BASE: str = "https://exemplo.com"
CONS_INT_MAX_TENTATIVAS: int = 5
```

#### Exceções

As exceções devem conter:

**Estrutura:** `<TipoErro>` (PascalCase)

Exemplo: `BusinessRuleException`, `TerminateException`, `ValueError`

### Comentários de Código

#### A Importância dos Comentários no Código

Os comentários servem para explicar o código, ajudando o próprio desenvolvedor a lembrar do que se trata a função, como também outros desenvolvedores a darem manutenção no código.

#### Onde Comentar?

Comentários em códigos devem ser usados sempre com bom senso, alocados em partes que possuem lógicas mais complexas, ou em algumas outras em que algo mais específico está sendo realizado. Ou seja, não é necessário infestar o código de comentários, porém, na dúvida, é melhor ter o código bastante comentado do que pouco.

**Exemplo:**
```python
# VAL001 - Validação de CPF
var_strCpf = var_dictInfoAdicional.get('cpf', '')
if len(var_strCpf) != 11 or not var_strCpf.isdigit():
    raise BusinessRuleException("CPF inválido ou incompleto")
```

### Organização de Pastas

#### Estrutura de Pastas

As pastas devem ser separadas entre sistemas/aplicações.

As classes que não se encaixarem em uma das principais aplicações realizadas e que podem ser reutilizadas, deverá ser inserida em uma pasta de reutilizáveis.

**Estrutura recomendada:**
```
{{PROJECT_NAME}}/
├── classes_t2c/
│   ├── framework/          # Classes do framework
│   ├── queue/              # Classes de fila
│   ├── utils/              # Classes reutilizáveis
│   └── ...
```

#### Pastas Reutilizáveis

Todo projeto deve ter uma pasta chamada de "utils" que conterá arquivos como classes padronizadas e reutilizáveis.

Estas classes devem ter argumentos de entrada e saída (quando necessário) bem definidos.

### Loops

#### Tratativas para Não Gerar Loop Infinito

Definir dupla condição para loops como `while` e `do while` e qualquer outra possibilidade de repetições infinitas.

Nestes casos sempre utilizar juntamente da condição padrão uma condição de tentativas, permitindo dupla saída, evitando loops infinitos e problemas em processos. Caso realizado N vezes o loop, finalizá-lo.

No caso de etapas essenciais ao processo, após esgotamento das tentativas, captar esta ação e apontar o problema detalhadamente pela forma decidida em projeto (e-mail, relatório...), finalizando o item com a exceção desejada.

**Exemplo:**
```python
var_intMaxTentativas = 5
var_intTentativa = 0

while condicao and var_intTentativa < var_intMaxTentativas:
    try:
        # código
        break
    except Exception as err:
        var_intTentativa += 1
        if var_intTentativa >= var_intMaxTentativas:
            raise Exception(f"Erro após {var_intMaxTentativas} tentativas: {str(err)}")
```

### Seletores

- **Sempre usar locators do Clicknium** quando disponível (ver PARTE 1 e PARTE 4)
- **Referenciar seletores conforme `selectors/selectors.md`**
- **Nunca usar seletores hardcodados**
- **Todos os seletores devem ser criados no Clicknium Recorder**
- **Manter nomenclatura consistente**

### Tratativas de Erro

#### Importância da Tratativa de Erro

Muito importante saber utilizar o **raise**, é um aliado que nos salva em diversas situações, principalmente para não precisar colocar mil coisas dentro de um IF só porque você precisa encerrar um processo. O **raise** é a chamada de um erro, erro que você mesmo mapeia, tendo assim um controle próprio dos erros e conseguindo encerrar o processo para partir para o próximo item. Além de facilitar na questão de relatórios para facilitar o entendimento das operações realizadas e as respostas recebidas pelo robô.

#### Exemplo de Utilização

Vou inserir uma nota, através do CNPJ deverá retornar as informações básicas do cliente, mas o CNPJ não foi cadastrado. Inicialmente deve-se pensar que a melhor maneira é "Ah vou colocar um if, do lado verdadeiro encontrou o CNPJ e coloco tudo que deve ser feito para inserir a nota lá, e no lado falso deixo vazio para o robô não executar nada". Aí que começam os problemas coloca dentro do if aí daqui a pouco tem mais uma checagem e precisa de mais um if, e assim sucessivamente. Uma solução que deixaria o código limpo seria colocar um if, no lado falso (que não encontrou o CNPJ) colocaria um **raise** com um erro de negócio reportando que o CNPJ não foi encontrado, e todo o resto do código fica fora do if.

**Exemplo correto:**
```python
# Verificar se CNPJ existe
if not cnpj_encontrado:
    raise BusinessRuleException("CNPJ não encontrado no sistema")

# Resto do código continua normalmente
inserir_nota(cnpj, dados)
```

**Exemplo incorreto:**
```python
if cnpj_encontrado:
    # Todo o código dentro do if
    inserir_nota(cnpj, dados)
    processar_dados()
    # ... mais código
else:
    # Código vazio ou apenas log
    pass
```

#### Tipos de Erros Utilizados por Padrão no Framework

- **Exception:** Nativo do Python, é referente aos erros de aplicação.
  - Exemplo: Aplicação não abriu; Página não carregou; Erros desconhecidos.

- **BusinessRuleException:** Não nativo do Python, ou seja, tipo de erro personalizado desenvolvido para ser referente aos erros de negócios. Para ser utilizado, o mesmo deve ser importado.
  - Exemplo: CNPJ não encontrado; Erro contábil; E-mail inexistente.

- **TerminateException:** Para finalização antecipada com sucesso (quando item já foi processado, por exemplo).

Vale ressaltar que nada impede do desenvolvedor utilizar de outros erros, sejam nativos do Python ou não, para facilitar nas tratativas, desde que faça sentido com o contexto aplicado.

### TypeHint

#### Importância do TypeHint

O TypeHint é o responsável pela especificação de tipos de dados em uma linguagem fracamente tipada, para impor variáveis com um tipo específico. Ela é utilizada para facilitar a identificação dos tipos das variáveis, constantes, parâmetros e etc. Muitas vezes quando você está utilizando uma variável, ela pode não ter tipo definido inicialmente, sendo marcada como Any, ou seja, pode assumir qualquer tipo, e isso não é uma boa prática, uma vez que além de dificultar na questão do desenvolvimento (não demonstrando as propriedades e métodos de um determinado tipo), o tipo Any pode dificultar em alguns momentos de manutenção.

#### Quando Será Utilizado?

Não é necessário utilizar o TypeHint em todos os momentos, muitas vezes, quando a variável é atribuída por um valor, automaticamente já é possível estipular qual o seu tipo, ao mover o mouse para cima da variável, porém, no caso de variáveis que ficam com valor any, é necessário deixar definido o seu tipo.

**Exemplo:**
```python
# TypeHint necessário quando tipo não é óbvio
var_dictItem: dict = GetTransaction.var_dictQueueItem
var_strReferencia: str = var_dictItem['referencia']

# TypeHint opcional quando tipo é óbvio
var_intContador = 0  # Python infere como int
var_strNome = "Teste"  # Python infere como str
```

### Outras Menções Importantes

#### Evitar Loop Dentro de Loop

Existem casos e casos, pensar sempre se será necessário e não há outra maneira, pois **loop** dentro de **loop** é algo que deixa muito lento o processamento do robô. Imagine que exista uma lista e nela precisa se comparar item a item para saber se são iguais. Se utilizar **loop** dentro de **loop** você percorrerá a lista TamanhoLista² vezes, se a lista possuir 1000 itens, o **loop** percorrerá 1000*1000=1000000 vezes, algo que será muito lento. Solução: Caso não encontre uma saída, tenha uma segunda ideia, converse com alguém e tentem achar a solução juntos(as).

**Alternativas:**
- Usar dicionários para busca O(1) ao invés de loops O(n²)
- Usar sets para comparações
- Usar list comprehensions quando apropriado

#### Uso de Dicionário e Afins Como Parâmetros

Ao criar um método, caso o mesmo espere receber dois parâmetros ou mais que venham de um dicionário sugere-se enviar o dicionário todo como argumento.

**Exemplo:**
```python
# Preferível
def processar_item(arg_dictItem: dict):
    var_strReferencia = arg_dictItem['referencia']
    var_dictInfo = arg_dictItem['info_adicionais']

# Evitar
def processar_item(arg_strReferencia: str, arg_dictInfo: dict, arg_intId: int):
    pass
```

#### Cuidados com Camadas de Classes

Supondo que ao criar uma classe, você utiliza uma outra classe dentro dela, e assim acaba criando uma camada de correlações entre essas classes. Muitas camadas acabam sendo problemáticas no entendimento do projeto, logo, recomenda-se utilizar 4 camadas no máximo, para que não entre num mundo sem fim de camadas.

#### If Dentro de If Se Necessário

Verificar se realmente é necessário, pois IF dentro de IF pode ser um caminho sem volta, o projeto fica bagunçado e ruim de entender.

**Sugestões:**
- Adicionar múltiplas condições
- Uso do raise
- If para atribuição em uma única linha (ternário)
- Extrair lógica para funções separadas

**Exemplo:**
```python
# Evitar
if condicao1:
    if condicao2:
        if condicao3:
            # código

# Preferir
if condicao1 and condicao2 and condicao3:
    # código

# Ou usar raise
if not condicao1:
    raise BusinessRuleException("Condição 1 não atendida")
if not condicao2:
    raise BusinessRuleException("Condição 2 não atendida")
# código continua
```

#### Execuções Simultâneas

Podemos nos deparar com situações em que será necessário executar a mesma automação simultaneamente na mesma máquina ou em máquinas diferentes, então, segue algumas precauções que devemos ter:

**Você, arquiteto de soluções deve perguntar se poderá ocorrer da automação executar simultaneamente em algum momento, caso isso não seja previsto, deverá orientar o desenvolvedor dos possíveis problemas:**

- Verificar se a aplicação que está sendo automatizada aceita o acesso com o mesmo usuário mais de uma vez ao mesmo tempo
- Verificar se a aplicação que está sendo automatizada não terá um conflito quando executado na mesma máquina e na mesma sessão
- Verificar se não utiliza a mesma planilha ao mesmo tempo, pois, poderá ocorrer problema de planilha já estar aberta ou de sobrescrever os dados devido a sincronização
- Verificar se não haverá conflito no momento de envio de email

**Um ponto de atenção, muito importante, é que se executar na mesma máquina na mesma sessão, se o projeto não estiver bem desenvolvido pensando nisso, é a situação mais propícia para dar erro.**

---

## 🚫 O Que NÃO Fazer

1. ❌ **NÃO modificar arquivos core do framework**
2. ❌ **NÃO hardcodar valores** (usar configurações)
3. ❌ **NÃO usar seletores hardcodados** (usar Clicknium)
4. ❌ **NÃO ignorar tratamento de erros**
5. ❌ **NÃO pular validações de entrada**
6. ❌ **NÃO usar integrações sem verificar configuração**
7. ❌ **NÃO criar código fora dos pontos de entrada definidos**

---

## ✅ Checklist Antes de Implementar

- [ ] Li e entendi todas as especificações do framework
- [ ] Verifiquei `config/base.md` para integrações
- [ ] Verifiquei `selectors/selectors.md` para seletores
- [ ] Verifiquei `business-rules/rules.md` para regras
- [ ] Identifiquei os pontos de entrada necessários
- [ ] Planejei o tratamento de erros adequado
- [ ] Planejei o uso correto de logging
- [ ] Identifiquei os templates a usar
- [ ] Entendi a estrutura de diretórios a criar

---

**Última atualização:** 2024  
**Versão do Framework:** 2.2.3

