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
- **Acessar item atual via `GetTransaction.var_dictQueueItem`**
- **Atualizar status corretamente:**
  - `SUCESSO` - Processamento bem-sucedido
  - `BUSINESS ERROR` - Erro de regra de negócio
  - `APP ERROR` - Erro de sistema/aplicação
- **Exemplo:**
  ```python
  from {{PROJECT_NAME}}.classes_t2c.framework.T2CGetTransaction import T2CGetTransaction as GetTransaction
  from {{PROJECT_NAME}}.classes_t2c.queue.T2CQueueManager import T2CQueueManager as QueueManager
  
  var_dictItem = GetTransaction.var_dictQueueItem
  var_strReferencia = var_dictItem['referencia']
  var_dictInfoAdicional = var_dictItem['info_adicionais']
  ```

### 8. Integrações
- **Tracker:** Usar apenas se `config/base.md` indicar `Usar T2CTracker: SIM`
- **Maestro:** Usar apenas se `config/base.md` indicar `Usar Maestro: SIM`
- **Clicknium:** Usar apenas se `config/base.md` indicar `Usar Clicknium: SIM`
- **Email:** Usar apenas se `config/base.md` indicar `Usar E-mail: SIM`
- **Sempre verificar configuração antes de usar integrações**

### 9. Código Limpo
- **Seguir padrão de nomenclatura do framework:**
  - `var_str*` - Variáveis string
  - `var_int*` - Variáveis inteiras
  - `var_dict*` - Variáveis dicionário
  - `var_bool*` - Variáveis booleanas
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

### 12. Inicialização de Aplicações
- **Usar `InitAllSettings.initiate_web_manipulator()`** para navegadores
- **Usar `InitAllSettings.var_botWebbot`** para manipular navegador
- **Usar `InitAllSettings.var_botDesktopbot`** para manipular desktop
- **Implementar loop de tentativas** conforme padrão do framework

### 13. Finalização de Aplicações
- **Fechar navegador:** `InitAllSettings.var_botWebbot.stop_browser()`
- **Fechar aplicações desktop** conforme necessário
- **Implementar loop de tentativas** para fechamento

### 14. Acessar Item da Fila
- **Sempre usar `GetTransaction.var_dictQueueItem`** no método `T2CProcess.execute()`
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

### 15. Adicionar Itens à Fila
- **Usar `QueueManager.insert_new_queue_item()`** no método `T2CInitAllApplications.add_to_queue()`
- **Sempre fornecer `arg_strReferencia`** (identificador único)
- **Sempre fornecer `arg_dictInfAdicional`** (dicionário com dados)

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
    """
    Método principal para execução do código.
    Acesse o item a ser processado usando GetTransaction.var_dictQueueItem
    """
    # Acesse o item atual da fila
    var_dictItem = GetTransaction.var_dictQueueItem
    
    # Dados disponíveis:
    # - var_dictItem['id'] → ID do item na fila
    # - var_dictItem['referencia'] → Referência do item (seu identificador)
    # - var_dictItem['info_adicionais'] → Dicionário com informações adicionais
    
    # Exemplo de uso:
    var_strReferencia = var_dictItem['referencia']
    var_dictInfoAdicional = var_dictItem['info_adicionais']
    
    # SEU CÓDIGO AQUI
    Maestro.write_log(f'Processando item: {var_strReferencia}')
    
    # Exemplo: abrir navegador e processar
    chrome_browser = cc.chrome.open("https://exemplo.com")
    # ... seu código de automação ...
    chrome_browser.close()
    
    Maestro.write_log('Process Finished')
```

**Importante:**
- Este método é chamado automaticamente para cada item da fila
- O framework já gerencia tentativas e tratamento de erros
- Use `BusinessRuleException` para erros de negócio (não tenta novamente)
- Use `Exception` genérica para erros de sistema (tenta novamente)

#### 2. T2CInitAllApplications.add_to_queue() - Preencher Fila

**Localização:** `{{PROJECT_NAME}}/classes_t2c/framework/T2CInitAllApplications.py`

**O que é:** Método chamado apenas uma vez no início para adicionar itens à fila de processamento.

**Como usar:**
```python
@classmethod
def add_to_queue(cls):
    """
    Adiciona itens à fila no início do processo.
    """
    # Exemplo: Ler de um arquivo Excel
    import pandas as pd
    df = pd.read_excel('dados.xlsx')
    
    for index, row in df.iterrows():
        var_dictInfoAdicional = {
            'campo1': row['campo1'],
            'campo2': row['campo2'],
            # ... outros campos
        }
        
        QueueManager.insert_new_queue_item(
            arg_strReferencia=str(row['id']),  # Identificador único
            arg_dictInfAdicional=var_dictInfoAdicional
        )
```

#### 3. T2CInitAllApplications.execute() - Inicializar Aplicações

**Localização:** `{{PROJECT_NAME}}/classes_t2c/framework/T2CInitAllApplications.py`

**O que é:** Método para inicializar todas as aplicações necessárias (navegadores, programas desktop, etc.).

**Como usar:**
```python
@classmethod
def execute(cls, arg_boolFirstRun=False):
    """
    Executa a inicialização dos aplicativos necessários.
    arg_boolFirstRun: True na primeira execução, False em retentativas
    """
    var_intMaxTentativas = cls._var_dictConfig["MaxRetryNumber"]
    
    for var_intTentativa in range(var_intMaxTentativas):
        try:
            # SEU CÓDIGO AQUI
            # Exemplo: Abrir navegador
            InitAllSettings.initiate_web_manipulator(
                arg_boolHeadless=False,
                arg_brwBrowserEscolhido=Browser.CHROME,
                arg_strPastaDownload=r"C:\Downloads"
            )
            
            # Exemplo: Abrir aplicação desktop
            # subprocess.Popen(['caminho\\aplicacao.exe'])
            
            break  # Sucesso, sai do loop
        except Exception as err:
            if(var_intTentativa+1 == var_intMaxTentativas):
                raise err  # Última tentativa falhou
            # Tenta novamente
            continue
```

**Importante:**
- Este método é chamado na inicialização e também após erros de sistema
- `arg_boolFirstRun=True` apenas na primeira vez
- Use `InitAllSettings.var_botWebbot` para manipular navegador
- Use `InitAllSettings.var_botDesktopbot` para manipular desktop

#### 4. T2CCloseAllApplications.execute() - Fechar Aplicações

**Localização:** `{{PROJECT_NAME}}/classes_t2c/framework/T2CCloseAllApplications.py`

**O que é:** Método para fechar todas as aplicações no final da execução.

**Como usar:**
```python
@classmethod
def execute(cls):
    """
    Executa o fechamento de todos os aplicativos.
    """
    var_intMaxTentativas = cls._var_dictConfig["MaxRetryNumber"]
    
    for var_intTentativa in range(var_intMaxTentativas):
        try:
            # SEU CÓDIGO AQUI
            # Exemplo: Fechar navegador
            if InitAllSettings.var_botWebbot is not None:
                InitAllSettings.var_botWebbot.stop_browser()
            
            # Exemplo: Fechar aplicação desktop
            # subprocess.run(['taskkill', '/F', '/IM', 'aplicacao.exe'])
            
            break
        except Exception as err:
            if(var_intTentativa+1 == var_intMaxTentativas):
                raise err
            continue
```

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

# No método execute() de T2CInitAllApplications
InitAllSettings.initiate_web_manipulator(
    arg_boolHeadless=False,  # True para modo headless
    arg_brwBrowserEscolhido=Browser.CHROME,  # CHROME, EDGE, FIREFOX, UNDETECTED_CHROME
    arg_strPastaDownload=r"C:\Downloads",  # Opcional
    arg_intWidhtResolution=1920,  # Opcional
    arg_intHeightResolution=1080  # Opcional
)

# Após inicializar, use:
InitAllSettings.var_botWebbot.navigate_to("https://exemplo.com")
```

**Browsers disponíveis:**
- `Browser.CHROME` - Chrome padrão
- `Browser.EDGE` - Microsoft Edge
- `Browser.FIREFOX` - Firefox
- `Browser.UNDETECTED_CHROME` - Chrome não detectável (undetected-chromedriver)

#### Clicknium

Se `AtivarClicknium=SIM` no Config.xlsx:

```python
from clicknium import clicknium as cc, locator

# No seu código
chrome_browser = cc.chrome.open("https://exemplo.com")
cc.find_element(locator.exemplo.botao).click()
```

**Configuração de Locators:**
- O framework detecta automaticamente a pasta `.locator`
- Se executando do VSCode: busca na raiz do projeto
- Se executando do Maestro: busca em `resources/.locator`

### Integrações

#### 1. Conexão com Maestro (BotCity)

**Classe:** `T2CMaestro`

**Localização:** `{{PROJECT_NAME}}/classes_t2c/utils/T2CMaestro.py`

**Métodos úteis:**

```python
from {{PROJECT_NAME}}.classes_t2c.utils.T2CMaestro import T2CMaestro as Maestro

# Escrever log
Maestro.write_log(
    arg_strMensagemLog="Mensagem do log",
    arg_strReferencia="REF001",  # Opcional
    arg_enumLogLevel=LogLevel.INFO,  # INFO, WARN, ERROR, FATAL
    arg_enumErrorType=ErrorType.NONE  # NONE, APP_ERROR, BUSINESS_ERROR
)

# Obter credencial
var_strCredencial = Maestro.get_credential(
    arg_strLabel="NomeProcesso",  # Label da credencial
    arg_strKey="USER"  # Key da credencial
)

# Verificar se foi interrompido
if Maestro.is_interrupted():
    # Parar processamento
    pass

# Finalizar task
Maestro.finish_task(
    arg_boolSucesso=True,
    arg_strMensagem="Task finalizada com sucesso"
)
```

#### 2. Conexão com T2CTracker

**Classe:** `T2CTracker`

**Localização:** `{{PROJECT_NAME}}/classes_t2c/utils/T2CTracker.py`

**Uso automático:** O framework configura e usa o Tracker automaticamente se `AtivarT2CTracker=SIM`.

**Métodos úteis (geralmente não precisa usar diretamente):**

```python
from {{PROJECT_NAME}}.classes_t2c.utils.T2CTracker import T2CTracker as Tracker

# Avançar step (framework faz automaticamente)
Tracker.next_step(arg_intStep=14, arg_strMessage="Mensagem")

# Obter asset do Tracker
var_dictAsset = Tracker.get_asset(
    arg_strFolderName="Pasta",
    arg_strAssetName="NomeAsset"
)
var_strValor = var_dictAsset['value']
```

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

### Padrões de Nomenclatura

**Variáveis:**
- `var_str*` - Variáveis string
- `var_int*` - Variáveis inteiras
- `var_dict*` - Variáveis dicionário
- `var_bool*` - Variáveis booleanas
- `var_list*` - Variáveis lista
- `var_tpl*` - Variáveis tupla

**Classes:**
- Prefixo `T2C` para todas as classes do framework
- Nomes em PascalCase
- Exemplo: `T2CProcess`, `T2CQueueManager`

**Métodos:**
- Nomes em snake_case
- Verbos no infinitivo
- Exemplo: `execute()`, `add_to_queue()`, `close_all_applications()`

### Padrões de Código

#### 1. Imports
```python
# Sempre nesta ordem:
# 1. Imports dos módulos T2C
from {{PROJECT_NAME}}.classes_t2c.framework.T2CInitAllSettings import T2CInitAllSettings as InitAllSettings

# 2. Imports dos pacotes externos
from botcity.web import WebBot
```

#### 2. Acesso a Configurações
```python
# Sempre via InitAllSettings
var_strNomeProcesso = InitAllSettings.var_dictConfig["NomeProcesso"]
```

#### 3. Acesso ao Item da Fila
```python
# Sempre via GetTransaction
var_dictItem = GetTransaction.var_dictQueueItem
var_strReferencia = var_dictItem['referencia']
var_dictInfoAdicional = var_dictItem['info_adicionais']
```

#### 4. Logging
```python
# Sempre usar Maestro.write_log()
Maestro.write_log("Mensagem do log")
Maestro.write_log(
    arg_strMensagemLog="Mensagem",
    arg_strReferencia="REF001",
    arg_enumLogLevel=LogLevel.INFO,
    arg_enumErrorType=ErrorType.NONE
)
```

#### 5. Tratamento de Erros
```python
# BusinessRuleException - não tenta novamente
if condicao_erro_negocio:
    raise BusinessRuleException("Mensagem de erro de negócio")

# TerminateException - finalização antecipada com sucesso
if item_ja_processado:
    raise TerminateException("Item já processado")

# Exception genérica - permite retentativa
try:
    # código
except Exception as err:
    raise Exception(f"Erro: {str(err)}")
```

#### 6. Loop de Tentativas
```python
var_intMaxTentativas = cls._var_dictConfig["MaxRetryNumber"]

for var_intTentativa in range(var_intMaxTentativas):
    try:
        # código
        break
    except Exception as err:
        if(var_intTentativa+1 == var_intMaxTentativas):
            raise err
        continue
```

#### 7. Uso de Seletores Clicknium
```python
from clicknium import clicknium as cc, locator

# Clicar
cc.find_element(locator.pasta.elemento).click()

# Preencher
cc.find_element(locator.pasta.elemento).set_text("texto")

# Ler
texto = cc.find_element(locator.pasta.elemento).get_text()
```

#### 8. Inicialização de Navegador
```python
from botcity.web import Browser

InitAllSettings.initiate_web_manipulator(
    arg_boolHeadless=False,
    arg_brwBrowserEscolhido=Browser.CHROME,
    arg_strPastaDownload=r"C:\Downloads"
)

# Usar navegador
InitAllSettings.var_botWebbot.navigate_to("https://exemplo.com")
```

---

## 💡 PARTE 5: EXEMPLOS PRÁTICOS

### Exemplo 1: T2CProcess.execute() - Validações e Processamento

```python
@classmethod
def execute(cls):
    # Obter item atual da fila
    var_dictItem = GetTransaction.var_dictQueueItem
    var_strReferencia = var_dictItem['referencia']
    var_dictInfoAdicional = var_dictItem['info_adicionais']
    
    Maestro.write_log(f'Processando item: {var_strReferencia}')

    # VAL001 - Validação de CPF
    var_strCpf = var_dictInfoAdicional.get('cpf', '')
    if len(var_strCpf) != 11 or not var_strCpf.isdigit():
        raise BusinessRuleException("CPF inválido ou incompleto. O CPF deve conter 11 dígitos numéricos.")

    # COND001 - Horário de Processamento
    from datetime import datetime
    var_intHoraAtual = datetime.now().hour
    if var_intHoraAtual < 8 or var_intHoraAtual > 18:
        raise BusinessRuleException(f"Processamento permitido apenas entre 8h e 18h. Horário atual: {var_intHoraAtual}h")

    # Processamento principal
    # Exemplo: Login
    cc.find_element(locator.login.campo_usuario).set_text(var_dictInfoAdicional.get('usuario', ''))
    cc.find_element(locator.login.campo_senha).set_text(var_dictInfoAdicional.get('senha', ''))
    cc.find_element(locator.login.botao_entrar).click()
    
    # Aguardar carregamento
    sleep(3)
    
    # Exemplo: Navegar e processar
    InitAllSettings.var_botWebbot.navigate_to("https://sistema.exemplo.com/processar")
    
    # REG002 - Verificar se há dados
    if not cc.find_element(locator.processamento.tabela_resultados).is_existing():
        raise BusinessRuleException("Nenhum dado encontrado para o CPF informado no sistema.")
    
    Maestro.write_log('Process Finished')
```

### Exemplo 2: T2CInitAllApplications.execute() - Inicialização

```python
@classmethod
def execute(cls, arg_boolFirstRun=False):
    # 14      Inicializando Aplicações
    if(InitAllSettings.var_dictConfig["AtivarT2CTracker"].upper() == "SIM"):
        Tracker.next_step(arg_intStep=14)

    Maestro.write_log("InitAllApplications Started")

    if(arg_boolFirstRun):
        cls.add_to_queue()

    var_intMaxTentativas = cls._var_dictConfig["MaxRetryNumber"]
    
    for var_intTentativa in range(var_intMaxTentativas):
        try:
            Maestro.write_log("Iniciando aplicativos, tentativa " + (var_intTentativa+1).__str__())
            
            # Inicializar navegador
            InitAllSettings.initiate_web_manipulator(
                arg_boolHeadless=False,
                arg_brwBrowserEscolhido=Browser.CHROME,
                arg_strPastaDownload=r"C:\Downloads"
            )
            
            # Navegar para página inicial
            InitAllSettings.var_botWebbot.navigate_to("https://sistema.exemplo.com")
            
            # Aguardar carregamento
            sleep(2)

        except BusinessRuleException as err:
            raise err
        except Exception as err:
            Maestro.write_log(GenericReusable.get_computer_usage())
            Maestro.write_log(
                arg_strMensagemLog="Erro, tentativa " + (var_intTentativa+1).__str__() + ": " + str(err),
                arg_enumLogLevel=LogLevel.ERROR,
                arg_enumErrorType=ErrorType.APP_ERROR
            )

            if(var_intTentativa+1 == var_intMaxTentativas): 
                raise err
            else: 
                continue
        else:
            Maestro.write_log("InitAllApplications Finished")
            break
```

### Exemplo 3: T2CInitAllApplications.add_to_queue() - Preencher Fila

```python
@classmethod
def add_to_queue(cls):
    # Exemplo: Ler de arquivo Excel
    import pandas as pd
    
    df = pd.read_excel('dados.xlsx')
    
    for index, row in df.iterrows():
        var_dictInfoAdicional = {
            'cpf': str(row['CPF']),
            'periodo': str(row['Periodo']),
            'usuario': str(row['Usuario']),
            'senha': str(row['Senha'])
        }
        
        QueueManager.insert_new_queue_item(
            arg_strReferencia=str(row['ID']),
            arg_dictInfAdicional=var_dictInfoAdicional
        )
    
    Maestro.write_log(f"Fila preenchida com {len(df)} itens")
```

### Exemplo 4: T2CCloseAllApplications.execute() - Fechar Aplicações

```python
@classmethod
def execute(cls):
    var_intMaxTentativas = cls._var_dictConfig["MaxRetryNumber"]
    
    for var_intTentativa in range(var_intMaxTentativas):
        try:
            Maestro.write_log("Fechando aplicativos, tentativa " + (var_intTentativa+1).__str__())
            
            # Fechar navegador
            if InitAllSettings.var_botWebbot is not None:
                InitAllSettings.var_botWebbot.stop_browser()
            
            # Fechar aplicação desktop (se necessário)
            # subprocess.run(['taskkill', '/F', '/IM', 'aplicacao.exe'])

        except Exception as err:
            Maestro.write_log(GenericReusable.get_computer_usage())
            Maestro.write_log(
                arg_strMensagemLog="Erro ao fechar aplicativos, tentativa " + (var_intTentativa+1).__str__() + ": " + str(err),
                arg_enumLogLevel=LogLevel.ERROR,
                arg_enumErrorType=ErrorType.APP_ERROR
            )

            if(var_intTentativa+1 == var_intMaxTentativas): 
                raise err
            else: 
                continue
        else:
            Maestro.write_log("CloseAllApplications Finished")
            break
```

---

## 🔧 PARTE 6: GUIA DE IMPLEMENTAÇÃO

### Fluxo de Geração do Framework

#### 1. Validação de Pré-requisitos

Verificar se todos os arquivos necessários existem:
- `specs/001-*/spec.md`
- `specs/001-*/plan.md`
- `specs/001-*/tasks.md`
- `selectors/selectors.md`
- `business-rules/rules.md`
- `config/base.md`

#### 2. Leitura de Especificações

Ler todas as specs:
- `tasks.md` - Tarefas de implementação
- `spec.md` - Especificação completa
- `plan.md` - Plano técnico
- `selectors.md` - Seletores de UI
- `rules.md` - Regras de negócio
- `config/*.md` - Todas as configurações

#### 3. Determinar Nome do Projeto

Obter nome do projeto de `config/base.md` ou usar padrão.

#### 4. Criar Estrutura de Diretórios

Criar estrutura completa em `generated/<nome-automacao>/` conforme estrutura definida acima.

#### 5. Gerar Arquivos Customizados

**5.1. bot.py** - Usar template abaixo, substituir `{{PROJECT_NAME}}`

**5.2. T2CProcess.py** - Usar template abaixo, substituir:
- `{{PROJECT_NAME}}`
- `{{IMPORTS}}` - baseado em selectors e plan
- `{{VALIDACOES_ENTRADA}}` - baseado em rules.md (VAL*)
- `{{CONDICOES_ESPECIAIS}}` - baseado em rules.md (COND*)
- `{{PROCESSAMENTO_PRINCIPAL}}` - baseado em tasks.md e spec.md

**5.3. T2CInitAllApplications.py** - Usar template abaixo, substituir:
- `{{PROJECT_NAME}}`
- `{{IMPORTS}}` - baseado em plan.md
- `{{PREENCHIMENTO_FILA}}` - baseado em tasks.md (Task 2.2)
- `{{INICIALIZACAO_APLICACOES}}` - baseado em tasks.md (Task 2.1)

**5.4. T2CCloseAllApplications.py** - Usar template abaixo, substituir:
- `{{PROJECT_NAME}}`
- `{{IMPORTS}}` - baseado em plan.md
- `{{FECHAMENTO_APLICACOES}}` - baseado em tasks.md (Task 4.1)

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
# Imports dos modulos T2C 
# Carrega o InitAllSettingsSettings Precisa ser o primeiro a ser carregado
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
# Imports dos modulos T2C 
# Carrega o InitAllSettingsSettings Precisa ser o primeiro a ser carregado
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


    #Parte principal do código, deve ser preenchida pelo desenvolvedor
    #Acesse o item a ser processado pelo arg_tplQueueItem
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
# Imports dos modulos T2C 
# Carrega o InitAllSettingsSettings Precisa ser o primeiro a ser carregado
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
# Imports dos modulos T2C 
# Carrega o InitAllSettingsSettings Precisa ser o primeiro a ser carregado
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

