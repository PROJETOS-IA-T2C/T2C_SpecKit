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
- `FilaProcessamento` - Nome da tabela de fila
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
        - Se o seu projeto precisa de mais do que um método simples para subir a sua fila, considere fazer um projeto dispatcher.

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

