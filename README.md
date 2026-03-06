# T2C SpecKit

**Crie projetos de automação RPA de forma estruturada, usando especificações que guiam a IA na geração de código.**

O T2C SpecKit é uma ferramenta de linha de comando que monta toda a estrutura de um projeto de automação RPA seguindo a metodologia **Spec-Driven Development** — você escreve especificações em Markdown e a IA (Cursor ou GitHub Copilot) gera o código baseado nelas, integrado ao Framework T2C.

---

## Índice

1. [Pré-requisitos](#1-pré-requisitos)
2. [Instalação do UV](#2-instalação-do-uv)
3. [Criando seu primeiro projeto](#3-criando-seu-primeiro-projeto)
4. [Entendendo a estrutura do projeto](#4-entendendo-a-estrutura-do-projeto)
5. [Fluxo de trabalho completo (passo a passo)](#5-fluxo-de-trabalho-completo-passo-a-passo)
6. [Tipos de arquitetura de robôs](#6-tipos-de-arquitetura-de-robôs)
7. [Referência rápida de comandos](#7-referência-rápida-de-comandos)
8. [Formatos de arquivo aceitos](#8-formatos-de-arquivo-aceitos)
9. [Solução de problemas](#9-solução-de-problemas)
10. [Links úteis](#10-links-úteis)

---

## 1. Pré-requisitos

Antes de começar, você vai precisar de três coisas:

### Python 3.8 ou superior

Verifique se já tem o Python instalado abrindo um terminal e digitando:

```bash
python --version
```

Se aparecer algo como `Python 3.10.x` (qualquer versão 3.8+), está tudo certo.

Se não tiver, baixe em [python.org/downloads](https://www.python.org/downloads/) e instale marcando a opção **"Add Python to PATH"** durante a instalação.

### UV (gerenciador de pacotes Python)

O UV é um gerenciador de pacotes moderno e rápido para Python. Ele permite executar o SpecKit com um único comando, sem precisar instalar nada permanentemente. A instalação é explicada na próxima seção.

### Editor de código com IA

O SpecKit funciona com dois editores. Escolha o que preferir:

| Editor | IA integrada | Observação |
|--------|-------------|------------|
| **Cursor** | IA nativa | Comandos slash funcionam nativamente em `.cursor/commands/` |
| **VS Code** | GitHub Copilot | Comandos slash via `.github/prompts/` (requer extensão Copilot) |

> **Dica:** Ambos oferecem a mesma experiência de comandos slash. A escolha é pessoal.

---

## 2. Instalação do UV

O UV precisa ser instalado apenas uma vez na sua máquina.

### Windows (PowerShell)

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### macOS / Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Verificando a instalação

Após instalar, feche e reabra o terminal, depois execute:

```bash
uv --version
```

Se aparecer a versão (ex: `uv 0.6.x`), a instalação foi bem-sucedida.

> **Nota:** Após instalar o UV, pode ser necessário reiniciar o terminal ou o computador para que o comando `uv` seja reconhecido.

---

## 3. Criando seu primeiro projeto

### Via uvx (recomendado)

Com o UV instalado, basta um único comando para criar o projeto:

```bash
uvx --from git+https://github.com/PROJETOS-IA-T2C/T2C_SpecKit.git t2c init meu-projeto
```

Substitua `meu-projeto` pelo nome que quiser dar ao seu projeto.

### Via pip (alternativa)

Se preferir instalar o pacote globalmente:

```bash
pip install git+https://github.com/PROJETOS-IA-T2C/T2C_SpecKit.git
t2c init meu-projeto
```

### O que acontece ao executar o `init`

O comando é interativo e vai te guiar em dois passos:

**1. Escolha do AI Assistant:**

```
Selecione seu AI Assistant:
  1. Cursor
  2. VS Code + GitHub Copilot

Escolha (1-2):
```

Selecione o editor que você usa. Isso define onde os comandos slash serão criados.

**2. Confirmação:**

```
Confirmação:
  Projeto: meu-projeto
  AI Assistant: cursor

Criar projeto? (s/N):
```

Digite `s` e pressione Enter. O SpecKit vai criar toda a estrutura de pastas, copiar templates, constitution e scripts.

**3. Resultado:**

```
✓ Projeto meu-projeto criado com sucesso!

Próximos passos:
  1. Abra o projeto no editor escolhido
  2. Coloque o DDP (PPTX ou DOCX) em specs/001-[nome]/DDP/
  3. Execute o comando /t2c.extract-ddp para extrair informações
  4. Complete os arquivos .md conforme necessário
  5. Execute /t2c.implement para gerar o framework T2C
```

---

## 4. Entendendo a estrutura do projeto

Após criar o projeto, você terá a seguinte estrutura:

```
meu-projeto/
│
├── .specify/                  # Configurações internas do SpecKit
│   ├── memory/
│   │   └── constitution.md    # Regras e padrões do framework T2C (usado pela IA)
│   ├── templates/             # Templates dos arquivos de especificação
│   │   ├── spec-template.md
│   │   ├── tests-template.md
│   │   ├── selectors-template.md
│   │   ├── business-rules-template.md
│   │   ├── tasks-template.md
│   │   └── Estimativa de Esforco - Template.xlsx
│   └── scripts/               # Scripts prontos (não precisa modificar)
│       ├── extract-ddp.py     # Extração de DDP (PPTX/DOCX)
│       └── excel_exporter.py  # Exportação de tasks para Excel
│
├── .cursor/commands/          # Se escolheu Cursor
│   ├── t2c.extract-ddp.md
│   ├── t2c.tasks.md
│   ├── t2c.tasks-export.md
│   ├── t2c.implement.md
│   └── t2c.validate.md
│
├── .github/prompts/           # Se escolheu VS Code + Copilot
│   ├── t2c.extract-ddp.prompt.md
│   ├── t2c.tasks.prompt.md
│   ├── t2c.tasks-export.prompt.md
│   ├── t2c.implement.prompt.md
│   └── t2c.validate.prompt.md
│
├── .vscode/                   # Se escolheu VS Code + Copilot
│   ├── settings.json
│   └── tasks.json
│
├── specs/                     # Suas especificações de automação
├── generated/                 # Código gerado pela IA (saída)
├── DDP/                       # DDPs gerais (Documentos de Design de Processo)
├── requirements.txt           # Dependências dos scripts
├── .gitignore
└── README.md
```

### O que é cada pasta

| Pasta | O que é | Você mexe? |
|-------|---------|------------|
| `.specify/` | Configurações internas, templates e scripts do SpecKit | Não (apenas consulta) |
| `.cursor/` ou `.github/prompts/` | Comandos slash que a IA lê para saber o que fazer | Não |
| `specs/` | Onde você coloca as especificações das automações | **Sim** |
| `generated/` | Onde o código gerado pela IA é salvo | Apenas leitura/teste |
| `DDP/` | Onde você coloca os documentos de design de processo | **Sim** |

---

## 5. Fluxo de trabalho completo (passo a passo)

O fluxo completo para criar uma automação RPA com o SpecKit segue 7 passos:

```
Criar projeto → Colocar DDP → Extrair DDP → Revisar specs → Gerar tasks → Gerar código → Validar
```

### Passo 1 — Criar o projeto

Já foi feito na seção anterior com `t2c init`. Abra a pasta do projeto no seu editor (Cursor ou VS Code).

---

### Passo 2 — Colocar o DDP no projeto

O **DDP (Documento de Design de Processo)** é o documento que descreve o que a automação deve fazer. Geralmente é um PowerPoint ou Word fornecido pelo cliente ou analista de processos.

**Onde colocar o arquivo:**

Coloque o arquivo `.pptx` ou `.docx` em uma destas pastas (o SpecKit procura automaticamente):

```
meu-projeto/
├── DDP/
│   └── ddp.pptx          ← Opção 1: pasta DDP/ na raiz
│
└── specs/
    └── 001-minha-automacao/
        └── DDP/
            └── ddp.pptx   ← Opção 2: dentro de specs/[nome]/DDP/
```

> **Formatos aceitos:** `.pptx` (PowerPoint) e `.docx` (Word)

---

### Passo 3 — Extrair informações do DDP

Este comando faz a IA ler o DDP e criar os arquivos de especificação do seu projeto.

**No Cursor:**

Abra o chat da IA e digite:

```
/t2c.extract-ddp
```

Ou especificando o caminho do arquivo:

```
/t2c.extract-ddp specs/001-minha-automacao/DDP/ddp.pptx
```

**No VS Code + GitHub Copilot:**

No chat do Copilot, use exatamente o mesmo comando:

```
/t2c.extract-ddp
```

**O que acontece por trás:**

1. O script `.specify/scripts/extract-ddp.py` é executado (ele já existe no projeto, não é criado nenhum script novo)
2. O texto do DDP é extraído e apresentado à IA
3. A IA lê o DDP **completo**, identifica etapas, sistemas, exceções e integrações
4. A IA **propõe uma arquitetura** (quantos robôs, tipo de cada um, justificativa)
5. A IA **aguarda sua aprovação** antes de criar qualquer arquivo
6. Após aprovação, a IA cria os arquivos de especificação (`spec.md`, `tests.md`, `selectors.md`, `business-rules.md`)

> **Importante:** A IA nunca cria arquivos sem sua aprovação. Ela sempre apresenta a proposta de arquitetura primeiro e espera seu OK.

---

### Passo 4 — Revisar e completar as especificações

Após a extração, a IA cria os seguintes arquivos dentro de `specs/`:

| Arquivo | O que contém | O que fazer |
|---------|-------------|-------------|
| `spec.md` | **Arquivo principal.** Arquitetura completa do robô: INIT, FILA, LOOP STATION, END PROCESS, stack tecnológica e integrações | Revisar se todas as etapas do DDP estão contempladas |
| `tests.md` | Cenários de teste e validações | Revisar e adicionar cenários específicos |
| `selectors.md` | Seletores de elementos de interface (Clicknium) — botões, campos, tabelas | Completar com seletores reais da aplicação |
| `business-rules.md` | Regras de negócio e exceções (EXC001, EXC002...) | Verificar se todas as exceções do DDP estão listadas |

**Dica:** Os arquivos são criados seguindo os templates em `.specify/templates/`. Se quiser ver a estrutura esperada, consulte esses templates.

---

### Passo 5 — Gerar tasks (opcional)

Este comando cria um breakdown de tarefas com estimativas de tempo, útil para planejamento.

**No Cursor ou VS Code:**

```
/t2c.tasks specs/001-minha-automacao
```

**O que é gerado:**

Um arquivo `tasks.md` contendo:
- Tabela de visão geral com resumo executivo
- Tasks organizadas por fase (INIT → FILA → LOOP STATION → END PROCESS)
- Estimativa de esforço para cada task seguindo o método **FEFP** (Framework de Estimativa de Esforço Padronizado)
- Resumo com tempo total estimado

> **Nota:** As estimativas já incluem uma margem de 30% embutida em cada task individual. O tempo total é a soma exata das estimativas.

---

### Passo 5b — Exportar tasks para Excel (opcional)

Se quiser as estimativas em formato planilha:

**No Cursor ou VS Code:**

```
/t2c.tasks-export
```

A IA vai:
1. Ler o `tasks.md`
2. Criar um JSON com os dados
3. Executar o script `.specify/scripts/excel_exporter.py`
4. Gerar um arquivo `.xlsx` formatado usando o template de estimativas

---

### Passo 6 — Gerar código

Este é o comando que gera o código Python real da automação.

**No Cursor ou VS Code:**

```
/t2c.implement specs/001-minha-automacao
```

**O que é gerado:**

O comando gera **classes especialistas** (não o framework core) dentro da pasta `generated/`:

```
generated/
└── sap/
    ├── sap_login.py           # Page Object para login no SAP
    └── sap_process.py         # Lógica de processamento no SAP
└── utils/
    └── data_validator.py      # Funções utilitárias
```

- O código segue as regras da `constitution.md` (nomenclatura, padrões, etc.)
- Classes em `PascalCase`, arquivos em `snake_case`
- O framework core (bot.py, T2CProcess.py, etc.) **não é gerado** — ele vem do repositório do Framework T2C separadamente

---

### Passo 7 — Validar especificações

Antes de gerar código, ou a qualquer momento, você pode validar se as specs estão completas:

**No Cursor ou VS Code:**

```
/t2c.validate specs/001-minha-automacao
```

**O que verifica:**

- Se todos os arquivos necessários existem (`spec.md`, `selectors.md`, `business-rules.md`, `tasks.md`)
- Se os campos obrigatórios estão preenchidos
- Se a estrutura dos arquivos segue os templates

O resultado é um relatório com ✓ (ok) e ✗ (pendente).

---

## 6. Tipos de arquitetura de robôs

O SpecKit suporta três tipos de arquitetura. A IA sugere a melhor opção com base no DDP, mas é importante entender cada uma:

### Standalone (1 robô)

Um único robô que executa todo o processo do início ao fim.

```
INIT → FILA → LOOP STATION → END PROCESS
```

**Quando usar:** Processos simples que interagem com poucos sistemas e não precisam de execução em etapas separadas.

**Estrutura de pastas:**

```
specs/
└── prj_Cliente_ID01_NomeAutomacao/
    ├── spec.md
    ├── tests.md
    ├── selectors.md
    └── business-rules.md
```

### Dispatcher + Performer (2+ robôs)

Um robô prepara os dados (Dispatcher) e outro processa (Performer).

```
Dispatcher: INIT → FILA → LOOP (prepara dados) → END
                                    ↓
Performer:  INIT → FILA (lê dados) → LOOP (processa) → END
```

**Quando usar:** Processos onde a coleta de dados e o processamento são etapas distintas, ou quando há necessidade de execução retroativa (reprocessar itens sem coletar novamente).

**Estrutura de pastas:**

```
specs/
├── prj_Cliente_ID01_Dispatcher/
│   ├── spec.md
│   ├── tests.md
│   ├── selectors.md
│   └── business-rules.md
└── prj_Cliente_ID01_Performer/
    ├── spec.md
    ├── tests.md
    ├── selectors.md
    └── business-rules.md
```

### Performer + Performer (cadeia)

Múltiplos performers em sequência, onde um processa e alimenta a fila do próximo.

```
Performer 1: INIT → FILA → LOOP (processa e alimenta próximo) → END
                                         ↓
Performer 2: INIT → FILA (lê dados) → LOOP (processa) → END
```

**Quando usar:** Processos com múltiplas etapas que envolvem sistemas diferentes ou lógicas complexas que se beneficiam de isolamento.

> **Nota:** A IA analisa o DDP e sugere a arquitetura mais adequada. Se as regras obrigatórias da Constitution indicarem separação, ela será recomendada. Você sempre pode aceitar ou ajustar a proposta.

---

## 7. Referência rápida de comandos

### Comandos slash (dentro do editor)

Estes comandos são usados no chat da IA (Cursor ou VS Code + Copilot):

| Comando | O que faz |
|---------|-----------|
| `/t2c.extract-ddp` | Extrai informações do DDP e cria as especificações |
| `/t2c.extract-ddp [caminho]` | Extrai de um arquivo específico |
| `/t2c.tasks [caminho]` | Gera `tasks.md` com breakdown e estimativas |
| `/t2c.tasks-export` | Exporta tasks para planilha Excel |
| `/t2c.implement [caminho]` | Gera código Python (classes especialistas) |
| `/t2c.validate [caminho]` | Valida estrutura e completude das specs |

> Os comandos funcionam de forma **idêntica** no Cursor e no VS Code + Copilot.

### Comandos CLI (no terminal)

| Comando | O que faz |
|---------|-----------|
| `t2c init [nome]` | Cria um novo projeto SpecKit |
| `t2c extract-ddp [caminho]` | Extrai texto de um DDP (PPTX/DOCX) no terminal |

**Exemplo com uvx (sem instalar):**

```bash
uvx --from git+https://github.com/PROJETOS-IA-T2C/T2C_SpecKit.git t2c init meu-projeto
```

### Alternativas no VS Code

Se preferir não usar comandos slash, o VS Code oferece outras formas:

- **Tasks:** `Ctrl+Shift+P` → "Tasks: Run Task" → selecione a task desejada (ex: "T2C: Extract DDP")
- **Scripts direto no terminal:**

```bash
python .specify/scripts/extract-ddp.py
python .specify/scripts/extract-ddp.py DDP/ddp.pptx
```

---

## 8. Formatos de arquivo aceitos

### Entrada (DDP)

| Formato | Extensão | Descrição |
|---------|----------|-----------|
| PowerPoint | `.pptx` | Formato mais comum para DDPs |
| Word | `.docx` | Alternativa em documento de texto |

O script de extração procura automaticamente por esses arquivos nas pastas `DDP/` e `specs/*/DDP/`.

### Saída (especificações)

| Arquivo | Formato | Descrição |
|---------|---------|-----------|
| `spec.md` | Markdown | Arquivo principal — arquitetura completa do robô |
| `tests.md` | Markdown | Cenários de teste e validações |
| `selectors.md` | Markdown | Seletores de elementos de interface (Clicknium) |
| `business-rules.md` | Markdown | Regras de negócio e exceções |
| `tasks.md` | Markdown | Breakdown de tarefas com estimativas (gerado pelo `/t2c.tasks`) |

### Exportação

| Formato | Extensão | Descrição |
|---------|----------|-----------|
| Excel | `.xlsx` | Planilha de estimativas (gerada pelo `/t2c.tasks-export`) |

---

## 9. Solução de problemas

### "uv não é reconhecido como comando"

O UV não está no PATH do sistema. Tente:

1. Fechar e reabrir o terminal
2. Reiniciar o computador
3. Reinstalar o UV seguindo a [seção de instalação](#2-instalação-do-uv)

### "python não é reconhecido como comando"

Python não está instalado ou não está no PATH:

1. Baixe em [python.org/downloads](https://www.python.org/downloads/)
2. Durante a instalação, marque **"Add Python to PATH"**
3. Reinicie o terminal

### "Nenhum arquivo DDP encontrado"

O script não encontrou nenhum `.pptx` ou `.docx`. Verifique:

1. Se o arquivo está em `DDP/` ou `specs/[nome]/DDP/`
2. Se a extensão é `.pptx` ou `.docx` (outros formatos como `.pdf` não são suportados)
3. Se o nome do arquivo não tem caracteres especiais

### "Diretório já existe" ao executar `t2c init`

Já existe uma pasta com o mesmo nome do projeto. Escolha outro nome ou delete a pasta existente.

### Os comandos slash não aparecem no editor

- **Cursor:** Verifique se a pasta `.cursor/commands/` existe e contém os arquivos `.md`
- **VS Code + Copilot:** Verifique se a pasta `.github/prompts/` existe e contém os arquivos `.prompt.md`. Certifique-se de que a extensão GitHub Copilot está instalada e ativa.

### Erro ao extrair DDP (dependências)

O script instala dependências automaticamente (`python-pptx`, `python-docx`), mas se falhar:

```bash
pip install python-pptx>=0.6.21 python-docx>=1.1.0
```

---

## 10. Links úteis

| Recurso | Link |
|---------|------|
| Repositório do SpecKit | [github.com/PROJETOS-IA-T2C/T2C_SpecKit](https://github.com/PROJETOS-IA-T2C/T2C_SpecKit) |
| Framework T2C | [github.com/T2C-Consultoria/prj_botcity_framework_template](https://github.com/T2C-Consultoria/prj_botcity_framework_template) |
| Instalar UV | [docs.astral.sh/uv](https://docs.astral.sh/uv/) |
| Instalar Python | [python.org/downloads](https://www.python.org/downloads/) |
| Cursor Editor | [cursor.com](https://www.cursor.com/) |
| GitHub Copilot | [github.com/features/copilot](https://github.com/features/copilot) |

---

## Licença

Este projeto está licenciado sob a Licença MIT.

## Créditos

- [Framework T2C](https://github.com/T2C-Consultoria/prj_botcity_framework_template)
- [BotCity](https://www.botcity.dev/)
- [Clicknium](https://www.clicknium.com/)
