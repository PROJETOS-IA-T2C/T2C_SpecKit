# Constituição do Framework T2C

Este documento define TODAS as regras, especificações, padrões, exemplos e templates que a IA deve seguir ao gerar código para o framework T2C.

**IMPORTANTE:** Este documento é exclusivamente para uso da IA durante a geração de código. O desenvolvedor humano não precisa consultá-lo diretamente.

---

## 🚨 REGRA FUNDAMENTAL - LEITURA CUIDADOSA DO DDP

**⚠️ EXTREMAMENTE CRÍTICO - SEM ISSO TUDO ESTARÁ ERRADO:**

**A leitura cuidadosa e completa do DDP é a BASE de todo o trabalho. Se a LLM não ler o DDP com atenção total e não considerar TUDO que está mapeado, TODAS as especificações estarão incorretas.**

**⚠️ OBRIGATÓRIO - ANTES DE QUALQUER OUTRA AÇÃO:**

1. **Ler o DDP COMPLETO** - palavra por palavra, do início ao fim
2. **NÃO pular NENHUMA seção** - mesmo que pareça irrelevante
3. **NÃO fazer suposições** - se algo não está claro, revisar o DDP
4. **Identificar TUDO** - TODAS as etapas, TODOS os sistemas, TODAS as exceções
5. **Contar EXATAMENTE** - não estimar, contar cada etapa do LOOP STATION
6. **Verificar TUDO** - garantir que NADA foi esquecido antes de criar arquivos

**⚠️ CONSEQUÊNCIAS DE NÃO SEGUIR ESTA REGRA:**
- ❌ Etapas serão esquecidas
- ❌ Sistemas não serão identificados
- ❌ Exceções de negócio não serão mapeadas
- ❌ Arquitetura estará incompleta
- ❌ Especificações estarão incorretas
- ❌ Código gerado não funcionará corretamente

**⚠️ REGRA DE OURO:**
- **Se o DDP menciona, DEVE estar contemplado**
- **Se não está contemplado, REVISAR o DDP novamente**
- **NENHUMA informação do DDP pode ser ignorada ou esquecida**

**👉 Ver seção "📖 LEITURA E ANÁLISE CUIDADOSA DO DDP - OBRIGATÓRIO" na seção 13 para checklist completo.**

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

**⚠️ IMPORTANTE:** O framework JÁ gerencia tratamento de erros automaticamente. A LLM deve gerar código simples e direto, sem adicionar validações ou tratativas desnecessárias.

**APENAS usar exceções quando:**
- **BusinessRuleException:** Para exceções de negócio mapeadas no business-rules.md (EXC*)
  ```python
  from {{PROJECT_NAME}}.classes_t2c.utils.T2CExceptions import BusinessRuleException
  raise BusinessRuleException("Mensagem de erro de negócio")
  ```
  - **SOMENTE** se a exceção estiver mapeada no business-rules.md
  - **NÃO** adicionar validações que não estão mapeadas

- **TerminateException:** Para finalização antecipada com sucesso (quando item já foi processado)
  ```python
  from {{PROJECT_NAME}}.classes_t2c.utils.T2CExceptions import TerminateException
  raise TerminateException("Item já processado")
  ```

**O que NÃO fazer:**
- ❌ **NÃO adicionar try/except genéricos** - o framework já trata
- ❌ **NÃO adicionar validações desnecessárias** - apenas as mapeadas no business-rules.md
- ❌ **NÃO adicionar verificações de "se existe", "se é válido"** que não estão no DDP
- ❌ **NÃO adicionar tratamento de Exception genérica** - o framework gerencia automaticamente

**Exception genérica:** Para erros de sistema (permite retentativa)
- O framework gerencia automaticamente as retentativas
- **NÃO é necessário** adicionar código para isso

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

**⚠️ REGRA OBRIGATÓRIA - Sistemas que NÃO Precisam de Seletores:**

**CRÍTICO:** Sistemas que manipulam arquivos diretamente (Office365, Google Workspace, etc.) **NÃO precisam de seletores**, pois são tratados em background. **Ver seção 12.5 - REGRA 2 e REGRA 5** para detalhes completos sobre manipulação de arquivos em background.

**Sistemas que NÃO precisam de seletores:**
- **Office365, Google Workspace, OneDrive e sistemas similares** - Ver seção 12.5 - REGRA 5
- **Qualquer sistema que manipula arquivos diretamente** - tratado em background, sem necessidade de seletores

**Sistemas que PRECISAM de seletores:**
- **Aplicações Web:** Navegadores (Chrome, Edge, Firefox) que precisam interagir com elementos da página
- **Aplicações Desktop:** Programas com interface gráfica que precisam ser automatizados (SAP, TOTVS, etc.)
- **Qualquer sistema que exija interação visual** com elementos da interface

**Regras Gerais:**
- **Sempre usar locators do Clicknium** quando disponível
- **Referenciar seletores conforme `selectors/selectors.md`**
- **Nunca usar seletores hardcodados**
- **Exemplo:**
  ```python
  from clicknium import clicknium as cc, locator
  
  cc.find_element(locator.login.botao_entrar).click()
  ```

### 6. Exceções de Negócio
- **Sempre aplicar exceções conforme `business-rules.md`** (localizado em `specs/001-[nome]/business-rules.md` ou `specs/001-[nome]/robot*/business-rules.md`)
- **Todas as regras de negócio são consolidadas como Exceções de Negócio** (EXC*)
- **Inclui:** validações, condições especiais, regras de processamento - tudo que pode gerar uma exceção ou regra específica
- **Usar BusinessRuleException ou TerminateException** conforme especificado nas exceções

### 7. Fila de Processamento

**⚠️ IMPORTANTE:** Consulte a **seção 12.5 - REGRA 1 e REGRA 4** para entender:
- Ordem correta de execução (FILA antes de aplicações) - REGRA 1
- Princípio de fila como fonte única de dados - REGRA 4
- Como especificar fonte de dados ao preencher a fila - REGRA 4

**Resumo:**
- **Sempre usar `QueueManager`** para gerenciar fila
- **Acessar item atual via `GetTransaction.var_dictQueueItem`** no método `T2CProcess.execute()`
- **Estrutura do item:**
  ```python
  {
      'id': int,
      'referencia': str,
      'info_adicionais': dict,  # JSON parseado - FONTE ÚNICA DE DADOS
      'status': str,
      'obs': str
  }
  ```
- **Adicionar itens:** Usar `QueueManager.insert_new_queue_item()` em `T2CInitAllApplications.add_to_queue()`
- **Status possíveis:** `SUCESSO`, `BUSINESS ERROR`, `APP ERROR`
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
- **Substituir variáveis:** `{{PROJECT_NAME}}`, `{{IMPORTS}}`, `{{EXCECOES_NEGOCIO}}`, etc.
- **Gerar em diretório separado:** Framework gerado em `generated/<nome-automacao>/`

#### 🚨 REGRA CRÍTICA - Geração de Código Simples e Direto

**⚠️ EXTREMAMENTE IMPORTANTE:** Ao gerar código através das tasks (comando `/t2c.implement`), a LLM DEVE seguir estas regras rigorosamente:

**1. Código Simples e Direto:**
- ✅ **GERAR código simples, direto e fácil de entender**
- ✅ **SEGUIR boas práticas de nomenclatura** (conforme PARTE 8)
- ✅ **ESCREVER código limpo e legível**
- ❌ **NÃO adicionar validações desnecessárias**
- ❌ **NÃO adicionar tratativas de erros desnecessárias**
- ❌ **NÃO adicionar try/except desnecessários**
- ❌ **NÃO adicionar verificações que não estão no DDP**

**2. Tratamento de Erros - APENAS Exceções de Negócio:**
- ✅ **ÚNICA tratativa obrigatória:** Quando houver uma **exceção de negócio mapeada no business-rules.md**, lançar `BusinessRuleException`
- ✅ **Aplicar exceções conforme business-rules.md** (EXC001, EXC002, etc.)
- ❌ **NÃO adicionar validações que não estão no business-rules.md**
- ❌ **NÃO adicionar try/except genéricos**
- ❌ **NÃO adicionar verificações de "se existe", "se é válido", etc. que não estão mapeadas**

**3. O que o Framework Já Faz:**
- O framework **JÁ gerencia** tratamento de erros de sistema automaticamente
- O framework **JÁ faz** retentativas automaticamente
- O framework **JÁ trata** exceções genéricas
- **NÃO é necessário** adicionar código para isso

**4. Exemplo de Código CORRETO (Simples):**
```python
@classmethod
def execute(cls):
    var_dictItem = GetTransaction.var_dictQueueItem
    var_strReferencia = var_dictItem['referencia']
    var_dictInfoAdicional = var_dictItem['info_adicionais']
    
    Maestro.write_log(f'Processando item: {var_strReferencia}')

    # EXC001 - Exceção de negócio mapeada no business-rules.md
    if not var_dictInfoAdicional.get('cpf'):
        raise BusinessRuleException("CPF não informado")

    # Código simples e direto - sem validações desnecessárias
    cc.find_element(locator.login.campo_usuario).set_text(var_dictInfoAdicional.get('usuario', ''))
    cc.find_element(locator.login.botao_entrar).click()
    cc.find_element(locator.tela.campo_cpf).set_text(var_dictInfoAdicional.get('cpf', ''))
    cc.find_element(locator.tela.botao_consultar).click()
    
    Maestro.write_log('Process Finished')
```

**5. Exemplo de Código INCORRETO (Complexo demais):**
```python
@classmethod
def execute(cls):
    var_dictItem = GetTransaction.var_dictQueueItem
    var_strReferencia = var_dictItem['referencia']
    var_dictInfoAdicional = var_dictItem['info_adicionais']
    
    # ❌ INCORRETO: Validação desnecessária
    if var_dictItem is None:
        raise Exception("Item não encontrado")
    
    # ❌ INCORRETO: Validação desnecessária
    if not var_strReferencia:
        raise Exception("Referência inválida")
    
    # ❌ INCORRETO: Try/except desnecessário
    try:
        Maestro.write_log(f'Processando item: {var_strReferencia}')
    except Exception as e:
        raise Exception(f"Erro ao logar: {e}")
    
    # ❌ INCORRETO: Validação que não está no business-rules.md
    if len(var_dictInfoAdicional.get('cpf', '')) != 11:
        raise BusinessRuleException("CPF inválido")  # Só se estiver mapeado no business-rules.md
    
    # ❌ INCORRETO: Try/except desnecessário - framework já trata
    try:
        cc.find_element(locator.login.campo_usuario).set_text(var_dictInfoAdicional.get('usuario', ''))
    except Exception as e:
        raise Exception(f"Erro ao preencher campo: {e}")
    
    # ... mais código complexo desnecessário
```

**6. Regra de Ouro:**
- **Se não está no DDP ou business-rules.md → NÃO adicionar**
- **Código deve ser o mais simples possível**
- **Fácil de entender e manter**
- **Seguir boas práticas de nomenclatura**
- **Deixar o framework fazer seu trabalho (tratamento de erros, retentativas, etc.)**

**⚠️ LEMBRE-SE:** O objetivo é gerar código **simples, direto e fácil de entender**. O framework já cuida da complexidade de tratamento de erros e retentativas. A LLM deve focar em implementar a lógica do processo de forma clara e objetiva.

### 12. Inicialização e Finalização de Aplicações

**⚠️ IMPORTANTE:** Antes de ler esta seção, consulte a **seção 12.5: 🚨 REGRAS CRÍTICAS DE ARQUITETURA DE EXECUÇÃO** para entender:
- Ordem correta de execução (FILA antes de aplicações) - REGRA 1
- Manipulação de arquivos em background - REGRA 2 e REGRA 5
- Login e acesso inicial no INIT - REGRA 3

**🚨 REGRA OBRIGATÓRIA - Sistemas que NÃO Precisam ser Inicializados:**

**⚠️ CRÍTICO:** Os seguintes sistemas **NÃO DEVEM** ser inicializados no método `T2CInitAllApplications.execute()`. Eles são tratados diretamente em background, manipulando arquivos diretamente, sem necessidade de inicialização prévia ou abertura de aplicações. **Ver seção 12.5 - REGRA 2 e REGRA 5** para detalhes completos sobre manipulação de arquivos em background.

**Sistemas que NÃO precisam de inicialização (SEM EXCEÇÃO):**

1. **Office365:**
   - Excel (arquivos .xlsx, .xls)
   - Word (arquivos .docx, .doc)
   - PowerPoint (arquivos .pptx, .ppt)
   - Outlook (aberto via e-mail ou link)
   - OneNote
   - Access
   - Qualquer outro aplicativo do Office365

2. **Google Workspace:**
   - Google Docs (aberto via link ou arquivo)
   - Google Sheets (aberto via link ou arquivo)
   - Google Slides (aberto via link ou arquivo)
   - Google Drive (acesso via link ou arquivo)

3. **OneDrive:**
   - Acesso via link ou arquivo
   - Não precisa inicialização

4. **Outros sistemas similares:**
   - Qualquer sistema que seja aberto diretamente por arquivo ou link
   - Sistemas baseados em nuvem acessados via link
   - Editores de documentos online acessados via link

**⚠️ REGRA DE OURO:**
- Se o sistema manipula arquivos diretamente (sem necessidade de interface gráfica), **NÃO inicializar** no INIT
- Arquivos devem ser lidos/manipulados em background usando bibliotecas Python (pandas, python-docx, etc.)
- Apenas sistemas que precisam ser **abertos programaticamente** (navegadores, SAP, TOTVS, etc.) devem ser inicializados
- **SEM EXCEÇÃO** - todos os sistemas similares seguem esta regra
- **Ver seção 12.5 - REGRA 2 e REGRA 5** para detalhes completos sobre manipulação de arquivos em background

**Inicialização de Sistemas que PRECISAM ser inicializados:**
- **Navegadores:** Usar `InitAllSettings.initiate_web_manipulator()` para navegadores
  - Usar `InitAllSettings.var_botWebbot` para manipular navegador
  - Usar `InitAllSettings.var_botDesktopbot` para manipular desktop
  - Implementar loop de tentativas conforme padrão do framework (ver PARTE 8)
- **Sistemas UI:** SAP, TOTVS, sistemas desktop que precisam ser abertos programaticamente
- **APIs:** Não precisam inicialização (são chamadas diretamente)

**Finalização:**
- Fechar navegador com `InitAllSettings.var_botWebbot.stop_browser()`
- Fechar aplicações desktop conforme necessário
- Implementar loop de tentativas para fechamento
- **Nota:** Sistemas abertos por arquivo/link geralmente não precisam ser fechados explicitamente (fecham com o arquivo)

- **Ver PARTE 2 e PARTE 5 para exemplos completos**

### 12.5. 🚨 REGRAS CRÍTICAS DE ARQUITETURA DE EXECUÇÃO

**⚠️ EXTREMAMENTE IMPORTANTE - OBRIGATÓRIO:**

Estas são regras fundamentais que definem a ordem e o comportamento correto de execução do framework. A LLM DEVE seguir estas regras rigorosamente ao criar especificações e código.

#### REGRA 1: Fila Deve Ser Populada ANTES de Inicializar Aplicações

**⚠️ OBRIGATÓRIO:** A fila DEVE ser preenchida ANTES de iniciar qualquer aplicação.

**Ordem correta de execução no INIT:**
1. **PRIMEIRO:** `add_to_queue()` - Preencher fila com todos os itens
2. **DEPOIS:** `execute()` - Inicializar aplicações (navegadores, sistemas UI, etc.)

**Por que isso é importante:**
- Garante que todos os dados estejam disponíveis antes de abrir sistemas
- Permite validação dos dados antes de consumir recursos de inicialização
- Facilita tratamento de erros na fase de preparação de dados

**Implementação no código:**
```python
@classmethod
def execute(cls, arg_boolFirstRun=False):
    # 1. PRIMEIRO: Preencher fila (se primeira execução)
    if(arg_boolFirstRun):
        cls.add_to_queue()  # ← SEMPRE ANTES de inicializar aplicações
    
    # 2. DEPOIS: Inicializar aplicações
    for var_intTentativa in range(var_intMaxTentativas):
        # {{INICIALIZACAO_APLICACOES}}
```

**❌ NÃO FAZER:**
- ❌ Inicializar aplicações antes de preencher a fila
- ❌ Preencher fila dentro do loop de inicialização de aplicações

#### REGRA 2: Arquivos São Lidos em Background (NÃO São Abertos)

**⚠️ OBRIGATÓRIO:** Arquivos (Excel, CSV, JSON, etc.) NÃO devem ser abertos através de aplicações. Eles devem ser lidos diretamente em background usando bibliotecas Python.

**O que isso significa:**
- **Excel/CSV:** Usar `pandas.read_excel()`, `pandas.read_csv()` - NÃO abrir Excel
- **Word:** Usar bibliotecas como `python-docx` - NÃO abrir Word
- **JSON:** Usar `json.load()` - NÃO abrir editor
- **PDF:** Usar bibliotecas como `PyPDF2`, `pdfplumber` - NÃO abrir leitor de PDF

**Exemplo correto:**
```python
# ✅ CORRETO: Ler Excel em background
import pandas as pd
df = pd.read_excel('dados.xlsx')  # Lê diretamente, sem abrir Excel

# ✅ CORRETO: Ler CSV em background
df = pd.read_csv('dados.csv')  # Lê diretamente, sem abrir aplicação

# ✅ CORRETO: Ler JSON em background
import json
with open('dados.json', 'r') as f:
    dados = json.load(f)  # Lê diretamente, sem abrir editor
```

**❌ NÃO FAZER:**
- ❌ Abrir Excel, Word ou qualquer aplicação para ler arquivos
- ❌ Usar seletores para interagir com aplicações de arquivos
- ❌ Inicializar aplicações Office365 para ler arquivos

**⚠️ IMPORTANTE:** Esta regra se aplica a TODOS os arquivos, não apenas Office365. Qualquer arquivo deve ser lido em background.

#### REGRA 3: Login, Abertura e Acesso Inicial ao Sistema Principal DEVEM Estar no INIT

**⚠️ OBRIGATÓRIO:** Qualquer etapa de abertura, login, acesso ou navegação inicial ao sistema principal (homepage, tela inicial) DEVE estar no INIT, NÃO no LOOP STATION.

**O que vai no INIT:**
- ✅ Abrir navegador e navegar para URL inicial
- ✅ Realizar login no sistema
- ✅ Navegar até a tela/homepage inicial do sistema
- ✅ Validar que o sistema está pronto para processamento
- ✅ Qualquer preparação inicial necessária antes do LOOP STATION

**O que vai no LOOP STATION:**
- ✅ Processar cada item da fila
- ✅ Navegação entre telas durante o processamento
- ✅ Ações específicas para cada item
- ❌ NÃO fazer login (já feito no INIT)
- ❌ NÃO navegar para homepage inicial (já feito no INIT)

**Exemplo correto:**
```python
# INIT (T2CInitAllApplications.execute)
# ✅ CORRETO: Login e navegação inicial no INIT
InitAllSettings.initiate_web_manipulator(...)
InitAllSettings.var_botWebbot.navigate_to("https://sistema.com")
cc.find_element(locator.login.campo_usuario).set_text(usuario)
cc.find_element(locator.login.campo_senha).set_text(senha)
cc.find_element(locator.login.botao_entrar).click()
# Validar que chegou na homepage/tela inicial
cc.wait_for_element(locator.homepage.menu_principal)

# LOOP STATION (T2CProcess.execute)
# ✅ CORRETO: Apenas processar itens (sistema já está logado)
var_dictItem = GetTransaction.var_dictQueueItem
# Processar item usando sistema já logado
```

**❌ NÃO FAZER:**
- ❌ Fazer login no LOOP STATION (deve estar no INIT)
- ❌ Navegar para homepage no LOOP STATION (deve estar no INIT)
- ❌ Abrir navegador no LOOP STATION (deve estar no INIT)

**⚠️ REGRA DE OURO:** O sistema deve estar completamente pronto (logado, na tela inicial) ANTES de entrar no LOOP STATION. O LOOP STATION apenas processa itens, não prepara o ambiente.

#### REGRA 4: Fila como Fonte Única - Especificar Fonte de Dados ao Preencher

**⚠️ OBRIGATÓRIO:** Ao preencher a fila, é necessário especificar qual a fonte de dados. A partir do momento que a fila é preenchida, qualquer outra fonte de informação não é necessária - apenas o item da fila.

**Ao preencher a fila (`add_to_queue()`):**
- ✅ **Especificar a fonte de dados:** Excel, CSV, API, Banco de Dados, etc.
- ✅ **Ler TODOS os dados necessários** da fonte
- ✅ **Fazer conciliações, validações, cálculos** se necessário
- ✅ **Criar itens na fila** com TODOS os dados necessários para processamento
- ✅ **Documentar no spec.md** qual é a fonte de dados

**No LOOP STATION (`execute()`):**
- ✅ **Usar APENAS** os dados do item da fila (`info_adicionais`)
- ✅ **NÃO ler** Excel, CSV, arquivos externos
- ✅ **NÃO fazer** conciliações complexas (já feitas na FILA)
- ✅ **NÃO consultar** outras fontes de dados (exceto sistemas para processamento)

**Exemplo correto:**
```python
# FILA (add_to_queue) - Especificar fonte e preparar dados
@classmethod
def add_to_queue(cls):
    # ✅ CORRETO: Especificar fonte de dados
    # Fonte: Arquivo Excel 'dados.xlsx'
    import pandas as pd
    df = pd.read_excel('dados.xlsx')  # Ler fonte
    
    # Preparar dados (conciliações, validações)
    for index, row in df.iterrows():
        # Criar item com TODOS os dados necessários
        QueueManager.insert_new_queue_item(
            arg_strReferencia=str(row['ID']),
            arg_dictInfAdicional={
                'cpf': str(row['CPF']),
                'nome': str(row['Nome']),
                'valor': float(row['Valor']),
                # TODOS os dados necessários para processamento
            }
        )

# LOOP STATION (execute) - Usar APENAS dados da fila
@classmethod
def execute(cls):
    var_dictItem = GetTransaction.var_dictQueueItem
    var_dictInfo = var_dictItem['info_adicionais']
    
    # ✅ CORRETO: Usar APENAS dados da fila
    cpf = var_dictInfo['cpf']  # Já está na fila
    nome = var_dictInfo['nome']  # Já está na fila
    valor = var_dictInfo['valor']  # Já está na fila
    
    # ❌ INCORRETO: Ler Excel novamente
    # df = pd.read_excel('dados.xlsx')  # NÃO FAZER ISSO!
```

**⚠️ PRINCÍPIO FUNDAMENTAL:** A fila é a fonte única de dados durante o LOOP STATION. Tudo que é necessário para processar um item deve estar no `info_adicionais` do item da fila.

#### REGRA 5: Office365 e Sistemas de Arquivos São Tratados em Background

**⚠️ OBRIGATÓRIO:** Excel, Word, Drive, Office365 ou qualquer outro sistema de arquivos NÃO deve ser INICIALIZADO ou ABERTO. Eles são tratados diretamente em background, manipulando os arquivos diretamente.

**Sistemas que NÃO devem ser inicializados/abertos:**
- **Office365:** Excel, Word, PowerPoint, Outlook, OneNote, Access, etc.
- **Google Workspace:** Google Docs, Google Sheets, Google Slides, Google Drive
- **OneDrive:** Acesso via link ou arquivo
- **Outros sistemas de arquivos:** Qualquer sistema que manipula arquivos diretamente

**Como tratar em background:**
- **Excel:** Usar `pandas.read_excel()`, `openpyxl` - manipular arquivo diretamente
- **Word:** Usar `python-docx` - manipular arquivo diretamente
- **CSV:** Usar `pandas.read_csv()` - manipular arquivo diretamente
- **JSON:** Usar `json.load()`, `json.dump()` - manipular arquivo diretamente
- **PDF:** Usar `PyPDF2`, `pdfplumber` - manipular arquivo diretamente

**Exemplo correto:**
```python
# ✅ CORRETO: Manipular Excel em background
import pandas as pd
df = pd.read_excel('dados.xlsx')  # Lê sem abrir Excel
df['novo_campo'] = df['campo1'] + df['campo2']  # Manipula dados
df.to_excel('resultado.xlsx', index=False)  # Salva sem abrir Excel

# ✅ CORRETO: Manipular Word em background
from docx import Document
doc = Document('documento.docx')  # Abre sem abrir Word
doc.add_paragraph('Novo parágrafo')  # Manipula documento
doc.save('documento_atualizado.docx')  # Salva sem abrir Word

# ✅ CORRETO: Ler CSV em background
df = pd.read_csv('dados.csv')  # Lê sem abrir aplicação
```

**❌ NÃO FAZER:**
- ❌ Inicializar Excel no INIT (`T2CInitAllApplications.execute()`)
- ❌ Abrir Word para ler/escrever documentos
- ❌ Usar seletores para interagir com Office365
- ❌ Abrir aplicações para manipular arquivos

**⚠️ REGRA DE OURO:** Se o sistema manipula arquivos diretamente (sem necessidade de interface gráfica), ele deve ser tratado em background usando bibliotecas Python, NÃO inicializado ou aberto como aplicação.

**⚠️ IMPORTANTE:** Esta regra se aplica a TODOS os sistemas de arquivos, não apenas Office365. Qualquer sistema que pode ser manipulado em background deve seguir esta regra.

### 13. Arquitetura de Robôs - Decisão e Estruturação

**⚠️ DECISÃO CRÍTICA:** Durante a análise do DDP (ao executar `/t2c.extract-ddp` e preencher as specs), a LLM DEVE decidir se o processo será:
- **Standalone**: Um único robô faz todo o processo
- **Múltiplos robôs**: Dispatcher + Performer ou Performer + Performer (ou mais combinações)

**🚨 IMPORTANTE - NÃO HÁ LIMITE DE ROBÔS:**
- A LLM pode criar **1, 2, 3, 4, 5 ou quantos robôs forem necessários** para organizar o processo da melhor forma possível
- A decisão de quantos robôs criar deve ser baseada na **complexidade, organização e manutenibilidade** do processo
- Não existe um limite máximo - o objetivo é criar a arquitetura mais organizada e manutenível possível
- Cada robô adicional segue o mesmo padrão de estrutura (robot1/, robot2/, robot3/, robot4/, robot5/, etc.)

#### 📖 LEITURA E ANÁLISE CUIDADOSA DO DDP - OBRIGATÓRIO

**🚨 REGRA FUNDAMENTAL - SEM ISSO TUDO ESTARÁ ERRADO:**

**⚠️ EXTREMAMENTE CRÍTICO - ANTES DE QUALQUER DECISÃO DE ARQUITETURA:**

A leitura cuidadosa e completa do DDP é a BASE FUNDAMENTAL de todo o trabalho. Se a LLM não ler o DDP com atenção total e não considerar TUDO que está mapeado, TODAS as especificações estarão incorretas e o processo não funcionará.

**A LLM DEVE ler o DDP com ATENÇÃO TOTAL e NÃO DEIXAR PASSAR NENHUMA ETAPA, REGRA, SISTEMA OU EXCEÇÃO mapeada no documento.**

**⚠️ PROCESSO OBRIGATÓRIO DE LEITURA:**

**PASSO 1 - Leitura Completa (OBRIGATÓRIO):**
- [ ] Ler o DDP **COMPLETO** do início ao fim, **palavra por palavra**
- [ ] **NÃO pular NENHUMA seção** - mesmo que pareça irrelevante
- [ ] **NÃO fazer suposições** - se algo não está claro, revisar o DDP
- [ ] Ler **múltiplas vezes** se necessário para garantir compreensão completa
- [ ] Identificar **TODAS as etapas** do processo (INIT, FILA, LOOP STATION, END PROCESS)
- [ ] Identificar **TODAS as exceções de negócio** (EXC* - tudo que pode gerar uma exceção ou regra específica)
- [ ] Identificar **TODOS os sistemas** envolvidos (APIs, UI, bancos de dados, Verifai, etc.)
- [ ] Identificar **TODAS as integrações** necessárias
- [ ] Identificar **TODAS as exceções** mapeadas

**PASSO 2 - Mapeamento Completo (OBRIGATÓRIO):**
- [ ] Criar uma lista escrita de **TODAS as etapas** identificadas
- [ ] Criar uma lista escrita de **TODAS as exceções de negócio** identificadas (EXC001, EXC002, etc.)
- [ ] Criar uma lista escrita de **TODOS os sistemas** identificados
- [ ] Criar uma lista escrita de **TODAS as integrações** identificadas
- [ ] **Contar EXATAMENTE** todas as etapas do LOOP STATION (não estimar, contar uma por uma)
- [ ] Garantir que **NENHUMA informação** foi perdida

**PASSO 3 - Verificação de Completude (OBRIGATÓRIO):**
- [ ] Verificar se **TODAS as etapas** do DDP foram contempladas na arquitetura
- [ ] Verificar se **TODAS as exceções de negócio** do DDP foram mapeadas nas business-rules.md
- [ ] Verificar se **TODOS os sistemas** foram identificados no spec.md
- [ ] Verificar se **TODAS as integrações** foram consideradas
- [ ] Verificar se **TODAS as exceções** foram mapeadas
- [ ] Verificar se **TODAS as etapas do LOOP STATION** foram contadas e estão no spec.md

**PASSO 4 - Arquitetura Deve Contemplar Tudo (OBRIGATÓRIO):**
- [ ] A arquitetura proposta **DEVE contemplar TODAS as etapas** do DDP
- [ ] A arquitetura proposta **DEVE contemplar TODAS as exceções de negócio** do DDP
- [ ] A arquitetura proposta **DEVE contemplar TODOS os sistemas** do DDP
- [ ] A arquitetura proposta **DEVE contemplar TODAS as integrações** do DDP
- [ ] Se alguma etapa/exceção/sistema/integração não foi contemplado → **REVISAR A ARQUITETURA** e **REVISAR O DDP**

**⚠️ REGRA DE OURO:** 
- **NENHUMA etapa, regra, sistema ou exceção do DDP pode ser ignorada ou esquecida**
- Se o DDP menciona algo, **DEVE** estar contemplado na arquitetura e nas specs
- Se houver dúvida se algo foi contemplado, **REVISAR** o DDP novamente
- A arquitetura final **DEVE** ser capaz de executar **TODAS as etapas** mapeadas no DDP
- **Se não está contemplado, REVISAR o DDP antes de criar os arquivos**

**⚠️ ATENÇÃO ESPECIAL:**
- Ler **palavra por palavra** seções críticas (LOOP STATION, exceções de negócio)
- **NÃO fazer suposições** - se algo não está claro no DDP, **NÃO inventar**, mas garantir que está contemplado
- Se o DDP menciona múltiplas etapas em sequência, **TODAS** devem estar no spec.md
- Se o DDP menciona exceções de negócio (validações, condições especiais, regras de processamento), **TODAS** devem estar no business-rules.md como exceções (EXC*)
- **NÃO pular etapas** mesmo que pareçam simples ou óbvias
- **NÃO assumir** que algo não é necessário - se está no DDP, está lá por um motivo

**⚠️ CONSEQUÊNCIAS DE NÃO SEGUIR ESTA REGRA:**
- ❌ Etapas serão esquecidas nas especificações
- ❌ Sistemas não serão identificados
- ❌ Exceções de negócio não serão mapeadas
- ❌ Arquitetura estará incompleta
- ❌ Especificações estarão incorretas
- ❌ Código gerado não funcionará corretamente
- ❌ Processo não executará todas as etapas necessárias

#### 🚨 REGRAS OBRIGATÓRIAS DE SEPARAÇÃO - VERIFICAR PRIMEIRO

**⚠️ ATENÇÃO CRÍTICA:** Antes de fazer qualquer análise contextual, a LLM DEVE verificar se o processo se enquadra em uma das regras obrigatórias abaixo. Se SIM, a separação é OBRIGATÓRIA, não opcional.

**REGRA OBRIGATÓRIA 1: LOOP STATION + Processamento Subsequente em Sistema Diferente**

**SEPARAR OBRIGATORIAMENTE quando:**
- ✅ Existe um LOOP STATION que processa múltiplos itens (cards, linhas, registros)
- ✅ Após o LOOP, há processamento em sistema diferente (SAP, TOTVS, outro sistema UI, ou outra fase distinta)
- ✅ O processamento subsequente pode ser executado de forma independente

**Checklist binário (SE TODAS AS RESPOSTAS FOREM SIM, SEPARAR É OBRIGATÓRIO):**
- [ ] O processo tem um LOOP que processa múltiplos itens?
- [ ] Após o LOOP, há outro processamento (em sistema diferente ou fase diferente)?
- [ ] Um erro em um item do LOOP pode comprometer outros itens se estiverem no mesmo robô?
- [ ] A separação permitiria execução retroativa (rodar robôs separadamente)?

**Se TODAS as respostas forem SIM → SEPARAR É OBRIGATÓRIO (Dispatcher + Performer)**

**Exemplos de casos que OBRIGAM separação:**
- Pipefy (API) → Consultar APIs (CNPJ, Sintegra) → SAP (UI) → **SEPARAR OBRIGATÓRIO**
- Excel → Processar linhas → Consultar APIs → TOTVS (UI) → **SEPARAR OBRIGATÓRIO**
- API → Enriquecer dados → Processar múltiplos itens → Sistema UI → **SEPARAR OBRIGATÓRIO**

**Exemplo detalhado - Caso Pipefy → APIs → SAP (CASO REAL):**
- **Processo:** Capturar cards do Pipefy via API → Consultar APIs (CNPJ, Sintegra, Suframa) → Consolidar dados → Lançar notas no SAP
- **Checklist REGRA OBRIGATÓRIA 1:**
  - [✅] O processo tem um LOOP que processa múltiplos itens? **SIM** - LOOP processa múltiplos cards do Pipefy
  - [✅] Após o LOOP, há outro processamento (em sistema diferente)? **SIM** - Processamento no SAP (sistema UI diferente)
  - [✅] Um erro em um item do LOOP pode comprometer outros? **SIM** - Se um card falhar, pode perder outros cards
  - [✅] A separação permitiria execução retroativa? **SIM** - Robot2 pode rodar depois que Robot1 populou a fila
- **RESULTADO:** **SEPARAR É OBRIGATÓRIO (Dispatcher + Performer)**
- **Estrutura obrigatória:**
  - `robot1/spec.md` - Dispatcher: Pipefy → APIs → consolidação → popula fila do performer
  - `robot2/spec.md` - Performer: Processa itens da fila no SAP (23 etapas)

**REGRA OBRIGATÓRIA 2: Sistemas Diferentes com LOOP Extenso**

**SEPARAR OBRIGATORIAMENTE quando:**
- ✅ O processo envolve sistemas diferentes (ex: APIs sem UI + Sistema UI)
- ✅ Há um LOOP STATION extenso (10+ etapas) em um dos sistemas
- ✅ A separação permitiria execução retroativa e isolamento de erros

**Checklist binário:**
- [ ] O processo envolve sistemas diferentes (ex: APIs + UI)?
- [ ] Há um LOOP STATION extenso (10+ etapas)?
- [ ] A separação permitiria rodar os robôs separadamente?

**Se TODAS as respostas forem SIM → SEPARAR É OBRIGATÓRIO**

**REGRA OBRIGATÓRIA 3: Preparação Complexa de Dados + Execução Simples**

**SEPARAR OBRIGATORIAMENTE quando:**
- ✅ A preparação de dados é complexa (múltiplas APIs, conciliações, validações extensas)
- ✅ A execução no sistema final é mais simples
- ✅ A preparação pode ser feita independentemente da execução

**Checklist binário:**
- [ ] A preparação envolve múltiplas fontes, APIs, conciliações ou validações extensas?
- [ ] A execução no sistema final é mais simples que a preparação?
- [ ] A preparação pode ser feita independentemente?

**Se TODAS as respostas forem SIM → SEPARAR É OBRIGATÓRIO (Dispatcher + Performer)**

**REGRA OBRIGATÓRIA 4: Preferência de API sobre Telas**

**⚠️ REGRA OBRIGATÓRIA:** Se no DDP está indicando que o processo deve ser via API mas está mapeado as telas, a LLM DEVE dar preferência a utilizar API para o processamento, em vez de usar as telas.

**APLICAR OBRIGATORIAMENTE quando:**
- ✅ O DDP indica que o processo deve ser via API
- ✅ O DDP também mapeia telas/interface do sistema
- ✅ A API está disponível e funcional

**Ação obrigatória:**
- **Usar API** para o processamento, mesmo que telas estejam mapeadas
- **NÃO usar** a interface/telas se a API estiver disponível
- **Documentar** no spec.md que a API foi escolhida sobre as telas
- **Justificar** a escolha na seção de arquitetura

**Exemplo:**
- **DDP indica:** "Processar via API do sistema X" e também mapeia telas do sistema X
- **Decisão:** Usar API do sistema X (não usar as telas)
- **Justificativa:** DDP indica preferência por API, mesmo com telas mapeadas

**⚠️ IMPORTANTE:** Esta é uma regra obrigatória. Se o DDP indica API, usar API, não telas.

**REGRA OBRIGATÓRIA 5: Extração de Documentos com Verifai**

**⚠️ REGRA CRÍTICA:** Quando o processo envolve extração de documentos usando Verifai, a separação é OBRIGATÓRIA.

**O que é Verifai:**
- Sistema de extração de documentos utilizado pela T2C
- Envia arquivos em PDF para o Verifai
- Retorna resultado da extração dos documentos
- Normalmente especificado no DDP quando há necessidade de extração de documentos

**SEPARAR OBRIGATORIAMENTE quando:**
- ✅ O processo envia documentos (PDFs) para o Verifai
- ✅ Após enviar para o Verifai, é necessário capturar o resultado da extração
- ✅ O resultado do Verifai será usado em processamento subsequente

**Checklist binário (SE TODAS AS RESPOSTAS FOREM SIM, SEPARAR É OBRIGATÓRIO):**
- [ ] O processo envia documentos para o Verifai?
- [ ] Após enviar para o Verifai, há necessidade de capturar o resultado?
- [ ] O resultado do Verifai será usado em processamento subsequente?

**Se TODAS as respostas forem SIM → SEPARAR É OBRIGATÓRIO**

**⚠️ REGRA FUNDAMENTAL:** Quando um robô envia um documento para o Verifai, ele DEVE encerrar sua atividade principal. Um outro robô será responsável por capturar o resultado do Verifai. Isso é uma regra essencial e pode resultar em múltiplos robôs no processo (2, 3, 4 ou quantos forem necessários para organizar o processo adequadamente).

**🚨 REGRA CRÍTICA - Envio e Captura do Verifai:**

**⚠️ OBRIGATÓRIO:**
- **O último passo do robô que envia** é o **envio do documento para o Verifai** (NÃO a captura)
- **A captura é realizada pelo robô seguinte** (OBRIGATÓRIO)
- **Por isso quebre os robôs** para que um envie e outro capture e continue o processamento

**Estrutura obrigatória com Verifai:**
- **Robot1 (Dispatcher):**
  - Prepara dados
  - **ÚLTIMO PASSO:** Envia documentos para o Verifai
  - **ENCERRA** após o envio (não captura)
  - Popula fila do Robot2 com referências dos documentos enviados

- **Robot2 (Performer):**
  - **PRIMEIRO PASSO:** Captura resultado do Verifai
  - Processa dados extraídos
  - Popula fila do Robot3 (se houver processamento subsequente)

- **Robot3+:** (Se necessário) Processamento adicional em outros sistemas ou fases

**⚠️ IMPORTANTE - Campos e Prompts para Captura:**

Ao criar o `robot2/spec.md` (robô que captura), a LLM DEVE:

1. **Indicar quais campos precisam ser capturados** do resultado do Verifai
2. **Sugerir prompts específicos** para cada campo que será capturado
3. **Formato dos prompts:** Perguntas ou pedidos para uma outra LLM capturar o campo específico

**Exemplo de campos e prompts no spec.md do Robot2:**
```markdown
## Campos a Capturar do Verifai

### Campo: CPF
- **Prompt sugerido:** "Qual o CPF desse documento?"
- **Tipo:** String
- **Validação:** (se necessário, conforme business-rules.md)

### Campo: Nome do Cliente
- **Prompt sugerido:** "Qual o nome completo do cliente nesse documento?"
- **Tipo:** String

### Campo: Valor Total
- **Prompt sugerido:** "Qual o valor total da nota fiscal?"
- **Tipo:** Decimal
```

**Estrutura típica com Verifai (exemplo - pode haver mais robôs se necessário):**
- **Robot1:** Prepara dados, **envia documentos para o Verifai** (último passo) → popula fila do Robot2
- **Robot2:** **Captura resultado do Verifai** (primeiro passo), processa dados extraídos → popula fila do Robot3 (se houver processamento subsequente)
- **Robot3:** (Opcional) Processa dados extraídos no sistema final (ex: SAP, TOTVS)
- **Robot4+:** (Se necessário) Processamento adicional em outros sistemas ou fases

**Exemplo detalhado - Caso com Verifai:**
- **Processo:** Ler Excel com referências → Enviar PDFs para Verifai → Capturar resultado da extração → Processar dados extraídos no SAP
- **Checklist REGRA OBRIGATÓRIA 5:**
  - [✅] O processo envia documentos para o Verifai? **SIM** - Envia PDFs para extração
  - [✅] Após enviar para o Verifai, há necessidade de capturar o resultado? **SIM** - Precisa capturar dados extraídos
  - [✅] O resultado do Verifai será usado em processamento subsequente? **SIM** - Dados extraídos serão processados no SAP
- **RESULTADO:** **SEPARAR É OBRIGATÓRIO (mínimo 2 robôs, podendo ser 3, 4 ou quantos forem necessários)**
- **Estrutura obrigatória (exemplo - pode haver mais robôs se necessário):**
  - `robot1/spec.md` - Dispatcher: 
    - Lê Excel com referências de documentos
    - **ÚLTIMO PASSO:** Envia PDFs para Verifai
    - **ENCERRA** após o envio (não captura)
    - Popula fila do robot2 com referências dos documentos enviados
  - `robot2/spec.md` - Performer: 
    - **PRIMEIRO PASSO:** Captura resultado do Verifai
    - **DEVE incluir seção "Campos a Capturar do Verifai"** com:
      - Lista de campos a capturar (CPF, Nome, Valor, etc.)
      - Prompts sugeridos para cada campo (ex: "Qual o CPF desse documento?")
    - Processa dados extraídos
    - Popula fila do robot3 (se houver)
  - `robot3/spec.md` - (Opcional) Performer: Processa dados no SAP
  - `robot4+/spec.md` - (Se necessário) Processamento adicional em outros sistemas ou fases

**⚠️ IMPORTANTE:** Se o processo se enquadrar em QUALQUER uma das regras obrigatórias acima (incluindo Verifai), a LLM DEVE separar em múltiplos robôs. Não é uma sugestão, é uma OBRIGAÇÃO.

**Se NENHUMA das regras obrigatórias se aplicar, então seguir para análise contextual abaixo.**

#### 📁 Estrutura Obrigatória Quando Separar em Múltiplos Robôs

**Quando uma regra obrigatória se aplicar, a LLM DEVE criar a seguinte estrutura:**

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
├── robot3/              # Robô 3 (Performer) - OPCIONAL, pode haver mais robôs
│   ├── spec.md          # ARQUIVO PRINCIPAL do robô 3
│   ├── selectors.md     # Seletores específicos do robô 3
│   ├── business-rules.md # Regras de negócio específicas do robô 3
│   └── tests.md         # Testes específicos do robô 3
├── tasks.md             # Compartilhado - lista plana com referência ao robô
└── DDP/                 # Compartilhado
```

**⚠️ IMPORTANTE:** 
- **NÃO HÁ LIMITE DE ROBÔS:** A LLM pode criar 1, 2, 3, 4, 5 ou quantos robôs forem necessários para organizar o processo da melhor forma possível
- A decisão de quantos robôs criar deve ser baseada na complexidade, organização e manutenibilidade do processo
- **Com Verifai:** Geralmente resulta em 2 ou 3 robôs (envio → captura → processamento), mas pode haver mais se necessário
- Cada robô adicional segue o mesmo padrão de estrutura (robot4/, robot5/, robot6/, etc.)

**⚠️ AÇÃO OBRIGATÓRIA:** Ao criar os arquivos `spec.md` de cada robô, a LLM DEVE:

1. **Criar `robot1/spec.md`** com:
   - Seção "Arquitetura de Robôs" no início indicando:
     - **Tipo:** Dispatcher
     - **Este robô é:** [Descrição do papel - ex: "Prepara dados do Pipefy, consulta APIs e popula fila do performer"]
     - **Recebe dados de:** N/A
     - **Alimenta:** robot2
     - **Ordem na cadeia:** 1
     - **Nome da pasta do robô:** robot1
   - Seção INIT com lógica de captura de dados
   - Seção FILA com lógica de preenchimento da própria fila (se Padrão 2) ou fila do performer (se Padrão 1)
   - Seção LOOP STATION com lógica de processamento de cada item
   - Seção END PROCESS

2. **Criar `robot2/spec.md`** com:
   - Seção "Arquitetura de Robôs" no início indicando:
     - **Tipo:** Performer
     - **Este robô é:** [Descrição do papel - ex: "Processa itens da fila no SAP"]
     - **Recebe dados de:** robot1
     - **Alimenta:** N/A
     - **Ordem na cadeia:** 2
     - **Nome da pasta do robô:** robot2
   - Seção INIT com lógica de inicialização do sistema final (ex: SAP)
   - Seção FILA indicando que não preenche (já populada pelo robot1)
   - Seção LOOP STATION com lógica de processamento no sistema final
   - Seção END PROCESS

3. **Criar `tasks.md` na raiz** com:
   - Tabela de visão geral de estimativas
   - Tasks do robot1 com campo "Robô: robot1"
   - Tasks do robot2 com campo "Robô: robot2"
   - Organização: todas tasks do robot1 primeiro, depois robot2

**⚠️ NÃO criar `spec.md` na raiz quando houver múltiplos robôs. Cada robô tem seu próprio `spec.md` dentro de sua pasta.**

#### Critérios para Análise de Arquitetura (Quando Não Há Regra Obrigatória)

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

7. **Isolamento de Erros no LOOP STATION e Execução Retroativa:**
   - **⚠️ CRITÉRIO PRIORITÁRIO:** Sempre que houver um LOOP STATION que processa múltiplos itens e, em seguida, outro processamento (em sistema diferente ou fase diferente), considerar separar em múltiplos robôs
   - Quando um erro em um item do LOOP pode comprometer o processamento dos demais itens se estiverem no mesmo robô
   - A separação permite que o framework trate erros automaticamente no LOOP STATION, mantendo a execução dos outros itens mesmo se um falhar
   - Quando uma fase pode ser executada de forma retroativa/independente após a outra (execução retroativa)
   - Quando diferentes fases precisam de estratégias de retry diferenciadas
   - **Padrão típico:** LOOP que processa múltiplos itens (preparação/consolidação) → processamento subsequente em sistema diferente
   - **Benefícios:**
     - Isolamento de falhas: erro em um item não compromete outros
     - Execução retroativa: robôs podem rodar separadamente
     - Retry control diferenciado: cada fase pode ter estratégias próprias
     - Modularização por objetivo: cada robô tem responsabilidade clara

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
  - **Estrutura completa:** INIT → FILA → LOOP STATION → END PROCESS
  - **Nomenclatura:** `prj_AFYA_ID15_01_SAP_DISP` (usar sufixo `_DISP`)
  - **Padrões possíveis:**
    - **Padrão 1 (Linear):** INIT popula fila do performer diretamente (sem LOOP próprio)
      - **OBRIGATÓRIO:** Criar item vazio na própria fila para executar (framework precisa de pelo menos 1 item)
      - INIT → FILA (cria item vazio + popula fila do performer) → LOOP STATION (processa item vazio) → END PROCESS
    - **Padrão 2 (LOOP próprio):** INIT popula própria fila, LOOP STATION processa itens e popula fila do performer
      - INIT → FILA (captura dados externos, ex: cards do Pipefy, e sobe para própria fila)
      - LOOP STATION → Para cada item da própria fila: processa (ex: consulta APIs, consolida dados) → sobe item preparado para fila do performer
      - END PROCESS → Finaliza com e-mail
  - **Características:**
    - Lógica de preenchimento da fila pode ser complexa (múltiplas fontes, conciliações, validações extensas)
    - Pode ter LOOP STATION próprio para processar múltiplos itens antes de popular fila do performer
    - Usa framework para preparar dados e popular fila do performer
    - **Benefício do Padrão 2:** Isolamento de erros - se um item falhar no LOOP, outros itens continuam sendo processados
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
├── robot3/              # Robô 3 (Performer) - OPCIONAL, pode haver mais robôs
│   ├── spec.md          # ARQUIVO PRINCIPAL do robô 3
│   ├── selectors.md     # Seletores específicos do robô 3
│   ├── business-rules.md # Regras de negócio específicas do robô 3
│   └── tests.md         # Testes específicos do robô 3
├── tasks.md             # Compartilhado - lista plana com referência ao robô
└── DDP/                 # Compartilhado
```

**⚠️ NOTA IMPORTANTE:** 
- **NÃO HÁ LIMITE DE ROBÔS:** A LLM pode criar 1, 2, 3, 4, 5 ou quantos robôs forem necessários para organizar o processo da melhor forma possível
- A decisão de quantos robôs criar deve ser baseada na complexidade, organização e manutenibilidade do processo
- Com Verifai, geralmente resulta em 2 ou 3 robôs (envio → captura → processamento subsequente), mas pode haver mais se necessário

#### Regras Específicas por Tipo

**Para Dispatcher:**

**Padrão 1 (Linear - sem LOOP próprio):**
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

**Padrão 2 (LOOP próprio - processa múltiplos itens):**
- **INIT (`add_to_queue()`):** Capturar dados externos (ex: cards do Pipefy via API) e subir para própria fila:
  ```python
  @classmethod
  def add_to_queue(cls):
      # Capturar dados externos (ex: cards do Pipefy)
      cards = api_pipefy.get_cards()
      
      # Subir cada card para própria fila
      for card in cards:
          QueueManager.insert_new_queue_item(
              arg_strReferencia=card['id'],
              arg_dictInfAdicional={'card_data': card}
          )
  ```
- **LOOP STATION (`execute()`):** Para cada item da própria fila, processar e subir para fila do performer:
  ```python
  @classmethod
  def execute(cls):
      var_dictItem = GetTransaction.var_dictQueueItem
      var_strReferencia = var_dictItem['referencia']
      var_dictInfoAdicional = var_dictItem['info_adicionais']
      
      # Processar item (ex: consultar outras APIs, consolidar dados)
      # ... código de processamento ...
      
      # Subir item preparado para fila do performer
      # Usar FilaProcessamentoPerformer do Config.xlsx
      # ... código para popular fila do performer ...
  ```
- **Benefício:** Isolamento de erros - se um item falhar no LOOP, o framework trata automaticamente e continua com os outros itens
- **Fila compartilhada (para popular o performer):**
  - No Config.xlsx do dispatcher existe a configuração `FilaProcessamentoPerformer` (ou similar)
  - Essa é a fila que o dispatcher deve preencher para o performer processar
  - Usar o mesmo `CaminhoBancoSqlite` configurado no Config.xlsx
  - O dispatcher popula essa fila usando `FilaProcessamentoPerformer` como nome da tabela
- **Fila própria do dispatcher:**
  - O dispatcher tem sua própria `FilaProcessamento` no Config.xlsx
  - **Padrão 1:** Contém apenas item vazio (necessário para framework executar)
  - **Padrão 2:** Contém os itens reais capturados no INIT (ex: cards do Pipefy) que serão processados no LOOP STATION

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

**⚠️ PASSO 0 - OBRIGATÓRIO: Leitura Cuidadosa do DDP**

**PRIMEIRO, ANTES DE QUALQUER OUTRA AÇÃO, a LLM DEVE:**

1. **Seguir o processo completo da seção "📖 LEITURA E ANÁLISE CUIDADOSA DO DDP" acima**
   - Isso inclui ler o DDP **COMPLETO** do início ao fim, **palavra por palavra**
   - Identificar **TODAS as etapas** (INIT, FILA, LOOP STATION, END PROCESS)
   - Identificar **TODAS as exceções de negócio** (EXC* - validações, condições especiais, regras de processamento)
   - Identificar **TODOS os sistemas** (APIs, UI, Verifai, etc.)
   - Identificar **TODAS as integrações** necessárias
   - **Contar EXATAMENTE** todas as etapas do LOOP STATION (não estimar, contar uma por uma)
   - **Criar listas escritas** de TODAS as etapas, exceções, sistemas e integrações identificadas
   - **⚠️ CRÍTICO:** Estas listas escritas serão usadas nos passos seguintes para decidir a arquitetura. Sem elas, a decisão estará baseada em informações incompletas.

**⚠️ PASSO 1 - OBRIGATÓRIO: Verificar Regras Obrigatórias de Separação**

**APÓS ler o DDP completamente e criar as listas escritas, a LLM DEVE:**

1. **Ler a seção "🚨 REGRAS OBRIGATÓRIAS DE SEPARAÇÃO" acima**
2. **Usar as listas criadas no PASSO 0 para verificar as regras obrigatórias:**
   - **Lista de sistemas** → verificar REGRA OBRIGATÓRIA 2 (Sistemas Diferentes com LOOP Extenso)
   - **Lista de etapas** → verificar REGRA OBRIGATÓRIA 1 (LOOP STATION + Processamento Subsequente)
   - **Lista de etapas** → verificar REGRA OBRIGATÓRIA 3 (Preparação Complexa + Execução Simples)
   - **Lista de sistemas** → verificar REGRA OBRIGATÓRIA 4 (Preferência de API sobre Telas)
   - **Lista de sistemas/integrações** → verificar REGRA OBRIGATÓRIA 5 (Extração de Documentos com Verifai)
3. **Aplicar os checklists binários das 5 regras obrigatórias:**
   - REGRA OBRIGATÓRIA 1: LOOP STATION + Processamento Subsequente
   - REGRA OBRIGATÓRIA 2: Sistemas Diferentes com LOOP Extenso
   - REGRA OBRIGATÓRIA 3: Preparação Complexa + Execução Simples
   - **REGRA OBRIGATÓRIA 4: Preferência de API sobre Telas** ⚠️ OBRIGATÓRIA
   - **REGRA OBRIGATÓRIA 5: Extração de Documentos com Verifai** ⚠️ CRÍTICA
4. **Se QUALQUER regra obrigatória se aplicar → SEPARAR É OBRIGATÓRIO**
5. **Se NENHUMA regra obrigatória se aplicar → seguir para análise contextual abaixo**

**⚠️ CRÍTICO:** Se o processo se enquadrar em uma regra obrigatória, a LLM NÃO deve fazer análise contextual. Deve separar imediatamente e criar a estrutura de múltiplos robôs.

**⚠️ ATENÇÃO ESPECIAL - API sobre Telas:**
- Se o DDP indica que o processo deve ser via API mas também mapeia telas, a LLM DEVE usar API (não telas)
- Esta é uma regra obrigatória de escolha de tecnologia, não de separação de robôs
- Documentar no spec.md que a API foi escolhida sobre as telas

**⚠️ ATENÇÃO ESPECIAL - Verifai:**
- Se o DDP mencionar "Verifai", "extração de documentos", "envio de PDF para extração", ou similar, a LLM DEVE verificar imediatamente a REGRA OBRIGATÓRIA 5
- Quando um robô envia documento para o Verifai, ele DEVE encerrar após o envio (último passo) e um outro robô captura o resultado (primeiro passo)
- O robô que captura DEVE incluir seção "Campos a Capturar do Verifai" com campos e prompts sugeridos
- **NÃO HÁ LIMITE:** Isso pode resultar em 2, 3, 4, 5 ou quantos robôs forem necessários para organizar o processo adequadamente

**PASSO 2 - Análise Contextual (Apenas se NENHUMA regra obrigatória se aplicou):**

**⚠️ USAR AS LISTAS CRIADAS NO PASSO 0 (seção de leitura cuidadosa do DDP):**

A análise contextual **DEVE ser baseada nas listas escritas** criadas durante a leitura cuidadosa do DDP. Não fazer suposições - usar os dados reais das listas.

**⚠️ ANTES de fazer a análise contextual, verificar novamente:**
- [ ] As listas escritas do PASSO 0 estão completas?
- [ ] **TODAS as etapas** do DDP foram identificadas nas listas?
- [ ] **TODAS as exceções de negócio** do DDP foram identificadas nas listas?
- [ ] **TODOS os sistemas** do DDP foram identificados nas listas?
- [ ] Se alguma coisa foi esquecida → **REVISAR o DDP** e **ATUALIZAR as listas** antes de continuar

Ao analisar o DDP, a LLM deve realizar uma análise contextual **usando as listas criadas** e considerando os seguintes aspectos:

**1. Análise de Complexidade do LOOP STATION:**
   - **Usar a lista de etapas criada:** Quantas etapas o LOOP STATION possui? (número exato da lista, não estimar)
   - **Usar a lista de exceções criada:** Quantas exceções de negócio estão envolvidas? (número exato da lista - EXC* - validações, condições especiais, regras de processamento)
   - **Usar a lista de sistemas/integrações criada:** Quantas integrações diferentes são necessárias? (número exato da lista - sistemas UI, APIs, bancos de dados)
   - A complexidade é gerenciável em um único robô ou seria mais organizado dividir?
   - Existem fases logicamente distintas que poderiam ser separadas?

**2. Análise da Complexidade da Preparação de Dados (FILA):**
   - A lógica de preenchimento da fila é simples (leitura direta de Excel/CSV) ou complexa?
   - São necessárias conciliações entre múltiplas fontes de dados?
   - Há validações extensas ou enriquecimento de dados (APIs, consultas complexas)?
   - A preparação de dados é significativamente mais complexa que o processamento em si?
   - A preparação poderia ser feita de forma independente e assíncrona?

**3. Análise de Separação Lógica e Responsabilidades:**
   - **Usar a lista de sistemas criada:** O processo tem fases com responsabilidades claramente distintas? (verificar sistemas diferentes na lista)
   - **Usar a lista de etapas criada:** Um robô prepararia dados enquanto outro executaria ações em sistemas diferentes? (verificar etapas de preparação vs. execução)
   - **Usar a lista de sistemas criada:** A separação por sistema traria benefícios claros? (verificar quantos sistemas diferentes estão na lista)
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

**⚠️ VERIFICAÇÃO FINAL OBRIGATÓRIA - ANTES DE CRIAR OS ARQUIVOS:**

**A LLM DEVE verificar que a arquitetura proposta contempla TUDO do DDP:**

- [ ] **TODAS as etapas** do DDP estão contempladas na arquitetura?
- [ ] **TODAS as exceções de negócio** (EXC* - validações, condições especiais, regras de processamento) estão mapeadas no business-rules.md?
- [ ] **TODOS os sistemas** mencionados no DDP estão contemplados?
- [ ] **TODAS as integrações** necessárias estão consideradas?
- [ ] **TODAS as exceções** mapeadas no DDP estão contempladas?
- [ ] **TODAS as etapas do LOOP STATION** foram contadas e estão no spec.md?
- [ ] Se alguma coisa do DDP não foi contemplada → **REVISAR** e **CORRIGIR** antes de criar os arquivos

**⚠️ REGRA DE OURO FINAL:**
- A arquitetura final **DEVE** ser capaz de executar **TODAS as etapas** mapeadas no DDP
- **NENHUMA etapa, regra ou sistema do DDP pode ser ignorada ou esquecida**
- Se houver dúvida, **REVISAR o DDP** novamente antes de criar os arquivos

**⚠️ LEMBRE-SE:** Nem sempre ter 2 sistemas UI significa necessariamente 2 robôs. A decisão deve ser baseada na análise cuidadosa de todos os aspectos, não em regras rígidas. Mas **TODAS as etapas e regras do DDP DEVEM estar contempladas**.

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

**Exemplo 2.1: Dispatcher + Performer (LOOP + Processamento Subsequente) - CASO REAL**
- **Processo:** Capturar cards do Pipefy via API, consultar outras APIs para enriquecer dados, consolidar informações, lançar notas no SAP
- **Análise:**
  - **LOOP identificado:** Processamento de múltiplos cards do Pipefy
  - **Processamento subsequente:** Lançamento de notas no SAP (sistema diferente)
  - **Padrão:** LOOP que processa múltiplos itens → processamento em sistema diferente
  - **Benefícios críticos da separação:**
    - **Isolamento de erros:** Se um card do Pipefy falhar, não perde os outros cards. O framework trata o erro automaticamente no LOOP STATION e continua com os demais
    - **Execução retroativa:** Robot2 pode rodar independentemente após Robot1 ter populado a fila
    - **Retry control diferenciado:** Cada robô pode ter estratégias de retry próprias (APIs vs. SAP)
    - **Modularização por objetivo:** Robot1 prepara/consolida dados, Robot2 executa no sistema final
- **Decisão:** Dispatcher + Performer (obrigatório separar devido ao LOOP)
- **Estrutura:**
  - **Robot1 (Dispatcher):**
    - INIT: Capturar cards do Pipefy via API → subir para própria fila
    - LOOP STATION: Para cada card da fila → consultar outras APIs → consolidar informações → subir item para fila do performer
    - END PROCESS: Finalizar com e-mail
  - **Robot2 (Performer):**
    - INIT: Não subir fila (já populada), iniciar SAP e realizar login
    - LOOP STATION: Cadastrar nota (item da fila) no SAP
    - END PROCESS: Finalizar SAP e enviar e-mail
- **Justificativa:** Este é um caso típico onde a separação é obrigatória. Se um card falhar no mesmo robô que processa o SAP, todos os outros cards seriam perdidos. A separação garante isolamento de erros e execução retroativa.

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

**Exemplo 6: Dispatcher + Performer + Performer (Verifai - CASO OBRIGATÓRIO)**
- **Processo:** Ler Excel com referências de documentos → Enviar PDFs para Verifai → Capturar resultado da extração → Processar dados extraídos no SAP
- **Análise - REGRA OBRIGATÓRIA 5:**
  - **Checklist Verifai:**
    - [✅] O processo envia documentos para o Verifai? **SIM** - Envia PDFs para extração
    - [✅] Após enviar para o Verifai, há necessidade de capturar o resultado? **SIM** - Precisa capturar dados extraídos
    - [✅] O resultado do Verifai será usado em processamento subsequente? **SIM** - Dados extraídos serão processados no SAP
  - **RESULTADO:** **SEPARAR É OBRIGATÓRIO (mínimo 2 robôs, neste exemplo 3, mas pode haver mais se necessário)**
- **Decisão:** Dispatcher + Performer + Performer (3 robôs neste exemplo - pode haver mais se necessário)
- **Estrutura:**
  - **Robot1 (Dispatcher):**
    - INIT: Ler Excel com referências de documentos
    - FILA: Criar item vazio na própria fila + popular fila do robot2 com referências dos PDFs
    - LOOP STATION: Para cada item → **enviar PDF para Verifai** → **encerrar atividade principal** (último passo)
    - END PROCESS: Finalizar com e-mail
  - **Robot2 (Performer):**
    - INIT: Não subir fila (já populada pelo robot1)
    - LOOP STATION: Para cada item da fila → **capturar resultado do Verifai** (primeiro passo) → processar dados extraídos → popular fila do robot3
    - **DEVE incluir seção "Campos a Capturar do Verifai"** no spec.md com:
      - Lista de campos a capturar (CPF, Nome, Valor, etc.)
      - Prompts sugeridos para cada campo (ex: "Qual o CPF desse documento?")
    - END PROCESS: Finalizar com e-mail
  - **Robot3 (Performer):**
    - INIT: Não subir fila (já populada pelo robot2), iniciar SAP e realizar login
    - LOOP STATION: Para cada item da fila → processar dados extraídos no SAP
    - END PROCESS: Finalizar SAP e enviar e-mail
- **Justificativa:** Este é um caso OBRIGATÓRIO de separação devido ao Verifai. Quando um robô envia documento para o Verifai, ele DEVE encerrar após o envio (último passo). Um outro robô captura o resultado (primeiro passo) e deve incluir seção com campos e prompts sugeridos. Como há processamento subsequente no SAP, um terceiro robô é necessário. A separação garante isolamento de erros, execução retroativa e permite que cada robô tenha responsabilidade clara.

**⚠️ OBSERVAÇÃO IMPORTANTE:** Os exemplos 4 e 5 mostram que a decisão não é baseada em uma única característica (como "ter 2 sistemas UI"), mas sim na análise cuidadosa de todos os fatores do processo específico. O Exemplo 6 mostra que quando há Verifai, a separação é OBRIGATÓRIA e pode resultar em múltiplos robôs.

### 14. Estimativas de Tempo para Tasks

**⚠️ IMPORTANTE:** Ao gerar tasks.md (comando `/t2c.tasks`), a LLM DEVE incluir estimativas de tempo realistas para cada tarefa.

#### Base de Estimativa

- **Perfil considerado:** Desenvolvedor pleno (não mencionar isso no documento, apenas usar como referência interna)
- **Formato:** Horas (ex: "2 horas", "4 horas", "0.5 horas", "8 horas")
- **Precisão:** Usar valores inteiros ou meias horas (0.5, 1, 1.5, 2, etc.)

#### 🗄️ Base de Dados de Complexidade de Sistemas

**⚠️ OBRIGATÓRIO:** A LLM DEVE consultar a base de dados de complexidade de sistemas antes de fazer estimativas. Esta base contém multiplicadores objetivos baseados em dados reais, não em suposições.

**Localização:** `src/rpa_speckit/memory/system_complexity.json`

**Como usar a base de dados:**

1. **Identificar o sistema no DDP:**
   - Verificar se o sistema está listado na base de dados (sistemas conhecidos)
   - Se não estiver, classificar por categoria:
     - Portal do governo
     - Sistema legado
     - Sistema menos conhecido
     - Sistema customizado

2. **Aplicar multiplicadores:**
   - **Multiplicador do sistema:** Baseado na categoria ou sistema específico
   - **Multiplicador de interface:** Tipo de interface (Web Moderna, Web Legado, Desktop, Terminal)
   - **Multiplicador de documentação:** Disponibilidade de documentação
   - **Multiplicador de seletores:** Estabilidade dos seletores

3. **Calcular estimativa final:**
   ```
   Estimativa Final = Estimativa Base × Multiplicador Sistema × Multiplicador Interface × Multiplicador Documentação × Multiplicador Seletores
   ```

4. **Documentar na justificativa:**
   - Sempre mencionar os multiplicadores aplicados
   - Explicar por que cada multiplicador foi usado

**Multiplicadores Base (se sistema não estiver na base):**
- **Sistemas conhecidos (SAP, TOTVS, Oracle, etc.):** 1.0x
- **Sistemas menos conhecidos:** 1.4x
- **Portais do governo:** 1.7x (geralmente mais complexos)
- **Sistemas legados:** 1.6x
- **Sistemas customizados:** 1.4x

**Fatores Técnicos (aplicar adicionalmente):**
- **Tipo de Interface:**
  - Web Moderna: 1.0x
  - Web Legado: 1.3x
  - Desktop Moderno: 1.2x
  - Desktop Legado: 1.5x
  - Terminal/AS400: 1.8x
  - Mobile/App: 1.4x

- **Documentação:**
  - Completa: 1.0x
  - Parcial: 1.2x
  - Sem documentação: 1.5x

- **Estabilidade de Seletores:**
  - Estáveis: 1.0x
  - Instáveis: 1.4x
  - Dinâmicos necessários: 1.6x

**Exemplo de cálculo:**
- **Sistema:** e-CAC (Portal do governo)
- **Estimativa base:** 2 horas (para uma etapa simples)
- **Multiplicadores:**
  - Sistema (e-CAC): 1.8x
  - Interface (Web Legado): 1.3x
  - Seletores (Instáveis): 1.4x
- **Cálculo:** 2h × 1.8 × 1.3 × 1.4 = 6.55h ≈ 7 horas
- **Justificativa:** "Portal do governo (1.8x) + Interface legada (1.3x) + Seletores instáveis (1.4x) = 7 horas"

**⚠️ IMPORTANTE:**
- **SEMPRE consultar a base de dados** antes de fazer estimativas
- **NUNCA usar multiplicadores aleatórios** - usar apenas os da base de dados
- **Documentar claramente** quais multiplicadores foram aplicados
- Se o sistema não estiver na base, usar a categoria mais próxima e documentar

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

**4. Exceções de Negócio:**
- **Cada exceção de negócio (EXC*):** +0.5-3h (dependendo da complexidade)
  - Validações simples: +0.5-1h
  - Condições especiais: +1-2h
  - Regras de processamento complexas: +1-3h

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
- **Justificativa OBRIGATÓRIA deve incluir:**
  - Referência à base de dados (se sistema estiver listado) ou categoria aplicada
  - Multiplicadores aplicados (sistema, interface, documentação, seletores)
  - Cálculo básico mostrando como chegou ao valor
  - Complexidade, número de etapas, integrações, exceções de negócio

#### Exemplo de Estimativa

**Exemplo 1: Sistema Conhecido (SAP)**
```markdown
### Task 2.1: Login e Navegação no Sistema SAP
- **Robô:** robot1
- **Consolida etapas do spec:** `robot1/spec.md` - LOOP STATION: Etapas 1-3
- **Arquivo:** T2CProcess.py
- **Método:** execute()
- **Descrição:** Realizar login no SAP, validar acesso, navegar até tela de processamento
- **Estimativa:** 3 horas - Login (1h) + Validação de acesso (0.5h) + Navegação com seletores Clicknium (1h) + Tratamento de erros (0.5h)
- **Justificativa:** Sistema conhecido (SAP - 1.0x), interface desktop estável, seletores estáveis. Base: 2h × 1.0 (sistema) × 1.0 (interface) × 1.0 (seletores) = 2h + 1h (tratamento erros) = 3h
- **Status:** [ ] Pendente / [ ] Em Progresso / [ ] Concluído
```

**Exemplo 2: Portal do Governo (e-CAC)**
```markdown
### Task 3.1: Consultar CNPJ no Portal e-CAC
- **Robô:** robot1
- **Consolida etapas do spec:** `robot1/spec.md` - LOOP STATION: Etapa 5
- **Arquivo:** T2CProcess.py
- **Método:** execute()
- **Descrição:** Acessar portal e-CAC, realizar login, consultar CNPJ e extrair dados
- **Estimativa:** 7 horas - Consulta base (2h) × Portal governo (1.8x) × Interface legada (1.3x) × Seletores instáveis (1.4x) = 6.55h ≈ 7h
- **Justificativa:** Portal do governo (e-CAC - 1.8x da base de dados) + Interface web legada (1.3x) + Seletores instáveis típicos de portais governo (1.4x). Base: 2h × 1.8 × 1.3 × 1.4 = 7h
- **Status:** [ ] Pendente / [ ] Em Progresso / [ ] Concluído
```

**Exemplo 3: Sistema Menos Conhecido**
```markdown
### Task 4.1: Processar Dados em Sistema Customizado
- **Robô:** robot2
- **Consolida etapas do spec:** `robot2/spec.md` - LOOP STATION: Etapas 2-4
- **Arquivo:** T2CProcess.py
- **Método:** execute()
- **Descrição:** Processar dados em sistema customizado interno, sem documentação disponível
- **Estimativa:** 6 horas - Processamento base (2h) × Sistema menos conhecido (1.4x) × Sem documentação (1.5x) = 4.2h ≈ 4h + 2h (análise e testes) = 6h
- **Justificativa:** Sistema customizado (1.4x) + Sem documentação técnica (1.5x) + Tempo adicional para análise reversa (2h). Base: 2h × 1.4 × 1.5 = 4.2h + 2h análise = 6h
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
│  - Preenche fila (add_to_queue) ← PRIMEIRO                  │
│  - Inicializa aplicações (InitAllApplications) ← DEPOIS     │
│  - Envia e-mail inicial                                     │
│                                                             │
│  ⚠️ IMPORTANTE: Ver seção 12.5 - REGRA 1 para ordem correta│
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

**⚠️ IMPORTANTE:** Ver **seção 12.5 - REGRA 1 e REGRA 4** para entender:
- Ordem correta de execução (FILA antes de aplicações) - REGRA 1
- Princípio de fila como fonte única de dados - REGRA 4
- Como especificar fonte de dados ao preencher a fila - REGRA 4

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

**⚠️ IMPORTANTE - Sistemas que NÃO Precisam ser Inicializados:**

**NÃO inicializar no INIT:** Office365 (Excel, Word, PowerPoint, etc.), Google Workspace (Google Docs, Sheets, etc.), OneDrive e sistemas similares que são tratados em background. Ver seção 12.5 - REGRA 2 e REGRA 5 para regra completa e detalhada.

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
- `{{EXCECOES_NEGOCIO}}` - Código de exceções de negócio (EXC* - validações, condições especiais, regras de processamento)
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

### Exemplo 1: T2CProcess.execute() - Exceções de Negócio e Processamento

**⚠️ IMPORTANTE:** Este exemplo mostra código SIMPLES e DIRETO. Apenas aplicar exceções que estão mapeadas no business-rules.md.

```python
@classmethod
def execute(cls):
    var_dictItem = GetTransaction.var_dictQueueItem
    var_strReferencia = var_dictItem['referencia']
    var_dictInfoAdicional = var_dictItem['info_adicionais']
    
    Maestro.write_log(f'Processando item: {var_strReferencia}')

    # EXC001 - Exceção de negócio mapeada no business-rules.md
    # APENAS aplicar se estiver mapeada no business-rules.md
    var_strCpf = var_dictInfoAdicional.get('cpf', '')
    if len(var_strCpf) != 11 or not var_strCpf.isdigit():
        raise BusinessRuleException("CPF inválido ou incompleto")

    # Código simples e direto - sem validações desnecessárias
    # Sem try/except - o framework já trata erros automaticamente
    cc.find_element(locator.login.campo_usuario).set_text(var_dictInfoAdicional.get('usuario', ''))
    cc.find_element(locator.login.botao_entrar).click()
    cc.find_element(locator.tela.campo_cpf).set_text(var_strCpf)
    cc.find_element(locator.tela.botao_consultar).click()
    
    Maestro.write_log('Process Finished')
```

**Observações:**
- ✅ Código simples, direto e fácil de entender
- ✅ Apenas uma exceção de negócio (se mapeada no business-rules.md)
- ✅ Sem try/except desnecessários
- ✅ Sem validações que não estão no DDP
- ✅ O framework cuida de tratamento de erros automaticamente

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
- `{{EXCECOES_NEGOCIO}}` - baseado em business-rules.md (EXC* - todas as exceções de negócio)
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

        # {{EXCECOES_NEGOCIO}}
        
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
# EXC001 - Exceção de negócio: CPF inválido
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

**⚠️ IMPORTANTE:** Esta seção explica o uso de `raise` para exceções de negócio. A LLM deve gerar código SIMPLES e usar `raise` APENAS para exceções mapeadas no business-rules.md.

#### Importância da Tratativa de Erro

Muito importante saber utilizar o **raise**, é um aliado que nos salva em diversas situações, principalmente para não precisar colocar mil coisas dentro de um IF só porque você precisa encerrar um processo. O **raise** é a chamada de um erro, erro que você mesmo mapeia, tendo assim um controle próprio dos erros e conseguindo encerrar o processo para partir para o próximo item. Além de facilitar na questão de relatórios para facilitar o entendimento das operações realizadas e as respostas recebidas pelo robô.

**⚠️ REGRA CRÍTICA:** 
- **APENAS usar `raise BusinessRuleException`** para exceções mapeadas no business-rules.md
- **NÃO adicionar validações/raises** que não estão mapeadas
- **Código deve ser simples** - usar raise apenas quando necessário (exceções mapeadas)

#### Exemplo de Utilização

**Exemplo correto (exceção mapeada no business-rules.md):**
```python
# EXC002 - Exceção mapeada no business-rules.md: CNPJ não encontrado
if not cnpj_encontrado:
    raise BusinessRuleException("CNPJ não encontrado no sistema")

# Resto do código continua normalmente - código simples e direto
inserir_nota(cnpj, dados)
```

**Exemplo incorreto (código complexo desnecessário):**
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

**Exemplo incorreto (validação não mapeada):**
```python
# ❌ INCORRETO: Validação que não está no business-rules.md
if not cnpj or len(cnpj) != 14:
    raise BusinessRuleException("CNPJ inválido")  # Só se estiver mapeado!
```

#### Tipos de Erros Utilizados por Padrão no Framework

- **BusinessRuleException:** Para exceções de negócio mapeadas no business-rules.md (EXC*)
  - **SOMENTE usar** se a exceção estiver mapeada no business-rules.md
  - Exemplo: CNPJ não encontrado (se EXC002 estiver mapeado); Erro contábil (se mapeado)
  - **NÃO adicionar** validações que não estão mapeadas

- **TerminateException:** Para finalização antecipada com sucesso (quando item já foi processado)

- **Exception genérica:** Para erros de sistema
  - **NÃO é necessário** adicionar código para isso
  - O framework gerencia automaticamente as retentativas
  - **NÃO adicionar** try/except genéricos

**⚠️ LEMBRE-SE:** O framework já cuida de tratamento de erros de sistema. A LLM deve focar em código simples e usar `raise` apenas para exceções de negócio mapeadas.

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
4. ❌ **NÃO adicionar validações desnecessárias** - apenas as mapeadas no business-rules.md
5. ❌ **NÃO adicionar try/except genéricos** - o framework já trata erros automaticamente
6. ❌ **NÃO adicionar verificações que não estão no DDP** - código deve ser simples e direto
7. ❌ **NÃO adicionar tratamento de erros complexo** - apenas BusinessRuleException para exceções mapeadas
8. ❌ **NÃO pular exceções de negócio mapeadas** (todas as exceções do business-rules.md devem ser implementadas)
9. ❌ **NÃO usar integrações sem verificar configuração**
10. ❌ **NÃO criar código fora dos pontos de entrada definidos**
11. ❌ **NÃO gerar código complexo** - código deve ser simples, direto e fácil de entender

---

## ✅ Checklist Antes de Implementar

- [ ] Li e entendi todas as especificações do framework
- [ ] Verifiquei `config/base.md` para integrações
- [ ] Verifiquei `selectors.md` para seletores
- [ ] Verifiquei `business-rules.md` para exceções de negócio
- [ ] Identifiquei os pontos de entrada necessários
- [ ] **⚠️ CRÍTICO:** Entendi que devo gerar código SIMPLES e DIRETO, sem validações/tratativas desnecessárias
- [ ] **⚠️ CRÍTICO:** Entendi que apenas devo aplicar exceções mapeadas no business-rules.md
- [ ] **⚠️ CRÍTICO:** Entendi que NÃO devo adicionar try/except genéricos (framework já trata)
- [ ] Planejei o uso correto de logging
- [ ] Identifiquei os templates a usar
- [ ] Entendi a estrutura de diretórios a criar

---

**Última atualização:** 2024  
**Versão do Framework:** 2.2.3
