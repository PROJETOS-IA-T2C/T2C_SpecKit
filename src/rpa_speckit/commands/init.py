"""
Comando init - Cria estrutura inicial do projeto
"""
import os
import shutil
from pathlib import Path
from rich.console import Console


def init_project(project_name: str, ai_assistant: str, console: Console):
    """
    Cria a estrutura inicial do projeto RPA Spec-Kit
    
    Args:
        project_name: Nome do projeto
        ai_assistant: AI assistant escolhido (cursor, vscode-copilot, vscode-claude, other)
        console: Console do rich para output
    """
    project_path = Path(project_name)
    
    if project_path.exists():
        raise ValueError(f"Diretório {project_name} já existe!")
    
    console.print(f"[cyan]Criando estrutura do projeto...[/cyan]")
    
    # Criar estrutura de diretórios
    directories = [
        ".specify/memory",
        ".specify/templates",
        ".specify/scripts/powershell",
        ".specify/scripts/bash",
        "specs",
        "generated",
        "DDP",
    ]
    
    # Adicionar diretórios específicos do AI assistant
    if ai_assistant == "cursor":
        directories.append(".cursor/commands")
    elif ai_assistant in ["vscode-copilot", "vscode-claude"]:
        directories.append(".vscode")
    
    for directory in directories:
        (project_path / directory).mkdir(parents=True, exist_ok=True)
    
    # Copiar constitution
    console.print("[cyan]Copiando constitution do framework T2C...[/cyan]")
    _copy_constitution(project_path)
    
    # Criar templates vazios
    console.print("[cyan]Criando templates...[/cyan]")
    _create_templates(project_path)
    
    # Criar comandos Cursor/VS Code
    if ai_assistant == "cursor":
        console.print("[cyan]Criando comandos Cursor...[/cyan]")
        _create_cursor_commands(project_path)
    elif ai_assistant in ["vscode-copilot", "vscode-claude"]:
        console.print("[cyan]Criando configurações VS Code...[/cyan]")
        _create_vscode_config(project_path, ai_assistant)
    
    # Criar scripts de automação
    console.print("[cyan]Criando scripts de automação...[/cyan]")
    _create_automation_scripts(project_path)
    
    # Criar arquivos iniciais
    console.print("[cyan]Criando arquivos iniciais...[/cyan]")
    _create_initial_files(project_path, project_name)
    
    console.print("[green]✓[/green] Estrutura criada com sucesso!")


def _copy_constitution(project_path: Path):
    """Copia a constitution do framework T2C do template interno"""
    constitution_path = project_path / ".specify/memory/constitution.md"
    
    # Obter caminho do template interno
    template_dir = Path(__file__).parent.parent.parent / "templates"
    template_constitution = template_dir / "constitution.md"
    
    if template_constitution.exists():
        # Copiar do template interno
        shutil.copy2(template_constitution, constitution_path)
    else:
        # Fallback: tentar do projeto de referência (para compatibilidade)
        ref_constitution = Path("C:/Robôs/projeto_ia_spec/memory/constitution.md")
        if ref_constitution.exists():
            shutil.copy2(ref_constitution, constitution_path)
        else:
            # Se não encontrar nenhum, criar versão básica
            basic_constitution = """# Constitution do Framework T2C

Este documento define TODAS as regras, especificações, padrões, exemplos e templates que a IA deve seguir ao gerar código para o framework T2C.

**IMPORTANTE:** Este documento é exclusivamente para uso da IA durante a geração de código.

## Nota

A constitution completa do framework T2C deve estar disponível no template do SpecKit.

A constitution contém todas as regras, padrões e templates necessários para geração de código.
"""
            constitution_path.write_text(basic_constitution, encoding="utf-8")


def _create_templates(project_path: Path):
    """Cria templates vazios para o desenvolvedor preencher"""
    templates_dir = project_path / ".specify/templates"
    
    # spec-template.md
    (templates_dir / "spec-template.md").write_text("""# Especificação de Automação RPA

## User Scenarios

### Scenario 1: [Nome do Cenário]
**Como** [persona]  
**Eu quero** [ação]  
**Para que** [objetivo]

**Dado que** [condição inicial]  
**Quando** [ação do usuário]  
**Então** [resultado esperado]

## Requirements

### Funcionais
- [ ] RF001: [Descrição]
- [ ] RF002: [Descrição]

### Não Funcionais
- [ ] RNF001: [Descrição]
- [ ] RNF002: [Descrição]

## Success Criteria

- [ ] SC001: [Critério de sucesso]
- [ ] SC002: [Critério de sucesso]

## Key Entities

### Entidade 1: [Nome]
- Campo1: [Tipo/Descrição]
- Campo2: [Tipo/Descrição]

### Entidade 2: [Nome]
- Campo1: [Tipo/Descrição]
- Campo2: [Tipo/Descrição]

## Observações

[Observações adicionais]
""", encoding="utf-8")
    
    # plan-template.md
    (templates_dir / "plan-template.md").write_text("""# Plano Técnico de Implementação

## Stack Tecnológica

- **Framework:** T2C Framework (v2.2.3)
- **Automação Web:** Clicknium
- **Plataforma:** BotCity
- **Linguagem:** Python 3.8+

## Arquitetura do Robô

### Componentes Principais

1. **T2CProcess**
   - Responsabilidade: [Descrição]
   - Fluxo: [Descrição do fluxo]

2. **T2CInitAllApplications**
   - Responsabilidade: [Descrição]
   - Aplicações a inicializar: [Lista]

3. **T2CCloseAllApplications**
   - Responsabilidade: [Descrição]
   - Aplicações a fechar: [Lista]

## Integrações

- [ ] Maestro (BotCity)
- [ ] T2CTracker
- [ ] Clicknium
- [ ] E-mail

## Estrutura de Dados

### Fila de Processamento
- Referência: [Campo identificador]
- Info Adicionais: [Estrutura JSON]

## Fluxo de Execução

1. [Passo 1]
2. [Passo 2]
3. [Passo 3]
""", encoding="utf-8")
    
    # selectors-template.md
    (templates_dir / "selectors-template.md").write_text("""# Seletores Clicknium

## Estrutura de Locators

### Pasta: [nome_pasta]

#### [nome_elemento]
- **Tipo:** [button/input/div/etc]
- **Seletor:** [descrição do seletor]
- **Uso:** [onde é usado]

#### [nome_elemento2]
- **Tipo:** [button/input/div/etc]
- **Seletor:** [descrição do seletor]
- **Uso:** [onde é usado]

## Notas

- Todos os seletores devem ser criados no Clicknium Recorder
- Manter nomenclatura consistente
- Documentar mudanças de UI que afetam seletores
""", encoding="utf-8")
    
    # business-rules-template.md
    (templates_dir / "business-rules-template.md").write_text("""# Regras de Negócio

## Validações (VAL*)

### VAL001: [Nome da Validação]
- **Descrição:** [Descrição completa]
- **Condição:** [Quando aplicar]
- **Ação em Erro:** [O que fazer se falhar]
- **Exceção:** BusinessRuleException

### VAL002: [Nome da Validação]
- **Descrição:** [Descrição completa]
- **Condição:** [Quando aplicar]
- **Ação em Erro:** [O que fazer se falhar]
- **Exceção:** BusinessRuleException

## Condições Especiais (COND*)

### COND001: [Nome da Condição]
- **Descrição:** [Descrição completa]
- **Condição:** [Quando aplicar]
- **Ação:** [O que fazer]

### COND002: [Nome da Condição]
- **Descrição:** [Descrição completa]
- **Condição:** [Quando aplicar]
- **Ação:** [O que fazer]

## Regras de Processamento (REG*)

### REG001: [Nome da Regra]
- **Descrição:** [Descrição completa]
- **Aplicação:** [Quando aplicar]
- **Resultado:** [Resultado esperado]

### REG002: [Nome da Regra]
- **Descrição:** [Descrição completa]
- **Aplicação:** [Quando aplicar]
- **Resultado:** [Resultado esperado]
""", encoding="utf-8")
    
    # tasks-template.md
    (templates_dir / "tasks-template.md").write_text("""# Breakdown de Tarefas

## Fase 1: Init

### Task 1.1: [Nome da Tarefa]
- **Descrição:** [Descrição]
- **Arquivo:** T2CInitAllApplications.py
- **Método:** execute()
- **Status:** [ ] Pendente / [ ] Em Progresso / [ ] Concluído

### Task 1.2: [Nome da Tarefa]
- **Descrição:** [Descrição]
- **Arquivo:** T2CInitAllApplications.py
- **Método:** add_to_queue()
- **Status:** [ ] Pendente / [ ] Em Progresso / [ ] Concluído

## Fase 2: Process

### Task 2.1: [Nome da Tarefa]
- **Descrição:** [Descrição]
- **Arquivo:** T2CProcess.py
- **Método:** execute()
- **Status:** [ ] Pendente / [ ] Em Progresso / [ ] Concluído

### Task 2.2: [Nome da Tarefa]
- **Descrição:** [Descrição]
- **Arquivo:** T2CProcess.py
- **Método:** execute()
- **Status:** [ ] Pendente / [ ] Em Progresso / [ ] Concluído

## Fase 3: End Process

### Task 3.1: [Nome da Tarefa]
- **Descrição:** [Descrição]
- **Arquivo:** T2CCloseAllApplications.py
- **Método:** execute()
- **Status:** [ ] Pendente / [ ] Em Progresso / [ ] Concluído
""", encoding="utf-8")


def _create_cursor_commands(project_path: Path):
    """Cria comandos Cursor"""
    commands_dir = project_path / ".cursor/commands"
    
    # t2c.extract-ddp.md
    (commands_dir / "t2c.extract-ddp.md").write_text("""# Extrair DDP

Extrai o texto de todos os slides de um arquivo DDP.pptx para que a LLM possa preencher os arquivos de especificação.

## Uso

\`\`\`
/t2c.extract-ddp [caminho_do_ddp]
\`\`\`

## Exemplo

\`\`\`
/t2c.extract-ddp specs/001-automacao-exemplo/DDP/ddp.pptx
\`\`\`

## O que faz

1. Lê o arquivo PPTX usando python-pptx
2. Extrai texto de todos os slides
3. Apresenta o texto extraído para a LLM
4. **A LLM preenche os arquivos de especificação** baseado no texto extraído:
   - \`specs/001-[nome]/spec.md\` - Especificação completa
   - \`specs/001-[nome]/plan.md\` - Plano técnico
   - \`specs/001-[nome]/selectors.md\` - Seletores Clicknium
   - \`specs/001-[nome]/business-rules.md\` - Regras de negócio

## Instruções para a LLM

Após extrair o texto do DDP, você deve:

1. **Ler todo o texto extraído** dos slides do PPTX
2. **Criar ou atualizar** os arquivos de especificação na pasta \`specs/001-[nome]/\`
3. **Preencher** cada arquivo baseado no conteúdo do DDP:
   - **spec.md**: Extrair cenários de usuário, requisitos funcionais/não-funcionais, critérios de sucesso, entidades principais
   - **plan.md**: Definir stack tecnológica (T2C Framework, Clicknium, BotCity), arquitetura do robô, integrações
   - **selectors.md**: Identificar elementos de UI mencionados no DDP (botões, campos, tabelas, etc.)
   - **business-rules.md**: Extrair validações (VAL*), condições especiais (COND*), regras de processamento (REG*)

4. **Usar os templates** em \`.specify/templates/\` como referência para a estrutura
5. **Manter a numeração** das regras (VAL001, VAL002, etc.) e tarefas (Task 1.1, Task 2.1, etc.)

## Notas

- Este comando apenas extrai o texto. A LLM é responsável por analisar e preencher os arquivos
- Se os arquivos já existirem, atualize-os com as novas informações do DDP
- Mantenha a estrutura e formatação dos templates
""", encoding="utf-8")
    
    # t2c.tasks.md
    (commands_dir / "t2c.tasks.md").write_text("""# Gerar Tasks

Gera o arquivo tasks.md baseado em spec.md, plan.md e business-rules.md.

## Uso

\`\`\`
/t2c.tasks [caminho_da_spec]
\`\`\`

## Exemplo

\`\`\`
/t2c.tasks specs/001-automacao-exemplo
\`\`\`

## O que faz

1. Lê spec.md, plan.md e business-rules.md
2. Analisa os requisitos e regras
3. Gera breakdown de tarefas organizado por fases:
   - Init (T2CInitAllApplications)
   - Process (T2CProcess)
   - End Process (T2CCloseAllApplications)
4. Cria tasks.md com todas as tarefas identificadas

## Arquivo Gerado

- \`specs/001-[nome]/tasks.md\`

## Notas

- Este comando é opcional - o desenvolvedor pode criar tasks.md manualmente
- As tarefas geradas devem ser revisadas e ajustadas conforme necessário
""", encoding="utf-8")
    
    # t2c.implement.md
    (commands_dir / "t2c.implement.md").write_text("""# Implementar Framework T2C

Gera o framework T2C completo baseado nas especificações preenchidas.

## Uso

\`\`\`
/t2c.implement [caminho_da_spec]
\`\`\`

## Exemplo

\`\`\`
/t2c.implement specs/001-automacao-exemplo
\`\`\`

## O que faz

1. Valida se todos os arquivos necessários estão preenchidos:
   - spec.md
   - plan.md
   - selectors.md
   - business-rules.md
   - tasks.md
   - config/*.md
2. Baixa o framework T2C do GitHub (organização privada)
3. Gera estrutura completa em \`generated/[nome-automacao]/\`
4. Copia arquivos do framework base
5. Gera arquivos customizados:
   - bot.py
   - T2CProcess.py
   - T2CInitAllApplications.py
   - T2CCloseAllApplications.py
   - Config.xlsx
6. Substitui variáveis de template
7. Gera requirements.txt, setup.py, README.md

## Arquivos Gerados

Estrutura completa do framework T2C em \`generated/[nome-automacao]/\`

## Pré-requisitos

- Acesso ao repositório privado do framework T2C
- Git configurado
- Python 3.8+ instalado

## Notas

- O framework é gerado do zero a cada execução
- Arquivos customizados são gerados baseados nas specs
- Arquivos do framework base são copiados (não modificados)
""", encoding="utf-8")
    
    # t2c.validate.md
    (commands_dir / "t2c.validate.md").write_text("""# Validar Especificações

Valida a estrutura e completude dos arquivos de especificação.

## Uso

\`\`\`
/t2c.validate [caminho_da_spec]
\`\`\`

## Exemplo

\`\`\`
/t2c.validate specs/001-automacao-exemplo
\`\`\`

## O que faz

1. Verifica se todos os arquivos necessários existem:
   - spec.md
   - plan.md
   - selectors.md
   - business-rules.md
   - tasks.md
   - config/*.md
2. Valida estrutura dos arquivos
3. Verifica se campos obrigatórios estão preenchidos
4. Gera relatório de validação

## Saída

Relatório indicando:
- ✓ Arquivos presentes
- ✓ Campos preenchidos
- ✗ Arquivos faltando
- ✗ Campos obrigatórios vazios

## Notas

- Execute antes de /t2c.implement para garantir que tudo está pronto
- Corrija os problemas indicados antes de prosseguir
""", encoding="utf-8")


def _create_vscode_config(project_path: Path, ai_assistant: str):
    """Cria configurações VS Code"""
    vscode_dir = project_path / ".vscode"
    
    settings = {
        "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
        "python.analysis.typeCheckingMode": "basic",
        "files.exclude": {
            "**/__pycache__": True,
            "**/*.pyc": True,
        }
    }
    
    if ai_assistant == "vscode-copilot":
        settings["github.copilot.enable"] = {
            "*": True
        }
    
    import json
    (vscode_dir / "settings.json").write_text(
        json.dumps(settings, indent=2),
        encoding="utf-8"
    )


def _create_automation_scripts(project_path: Path):
    """Cria scripts de automação PowerShell e Bash"""
    ps_dir = project_path / ".specify/scripts/powershell"
    bash_dir = project_path / ".specify/scripts/bash"
    
    # PowerShell: check-prerequisites.ps1
    (ps_dir / "check-prerequisites.ps1").write_text("""# Verifica pré-requisitos do projeto

Write-Host "Verificando pré-requisitos..." -ForegroundColor Cyan

# Verificar Python
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Python encontrado: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "✗ Python não encontrado!" -ForegroundColor Red
    exit 1
}

# Verificar Git
$gitVersion = git --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Git encontrado: $gitVersion" -ForegroundColor Green
} else {
    Write-Host "✗ Git não encontrado!" -ForegroundColor Red
    exit 1
}

# Verificar acesso ao repositório do framework T2C
Write-Host "Verificando acesso ao repositório do framework T2C..." -ForegroundColor Cyan
# TODO: Adicionar verificação específica

Write-Host "`nTodos os pré-requisitos estão instalados!" -ForegroundColor Green
""", encoding="utf-8")
    
    # PowerShell: create-new-feature.ps1
    (ps_dir / "create-new-feature.ps1").write_text("""# Cria nova feature (specs/001-[nome]/)

param(
    [Parameter(Mandatory=$true)]
    [string]$FeatureName
)

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $scriptPath))
$specsDir = Join-Path $projectRoot "specs"

# Encontrar próximo número disponível
$existingSpecs = Get-ChildItem -Path $specsDir -Directory | Where-Object { $_.Name -match '^\d{3}-' }
$maxNumber = 0

foreach ($spec in $existingSpecs) {
    $number = [int]($spec.Name -split '-')[0]
    if ($number -gt $maxNumber) {
        $maxNumber = $number
    }
}

$nextNumber = $maxNumber + 1
$featureNumber = $nextNumber.ToString("000")
$featureDir = Join-Path $specsDir "$featureNumber-$FeatureName"

# Criar estrutura
New-Item -ItemType Directory -Path $featureDir -Force | Out-Null
New-Item -ItemType Directory -Path (Join-Path $featureDir "DDP") -Force | Out-Null

# Copiar templates
$templatesDir = Join-Path $projectRoot ".specify/templates"
Copy-Item (Join-Path $templatesDir "spec-template.md") (Join-Path $featureDir "spec.md")
Copy-Item (Join-Path $templatesDir "plan-template.md") (Join-Path $featureDir "plan.md")
Copy-Item (Join-Path $templatesDir "selectors-template.md") (Join-Path $featureDir "selectors.md")
Copy-Item (Join-Path $templatesDir "business-rules-template.md") (Join-Path $featureDir "business-rules.md")
Copy-Item (Join-Path $templatesDir "tasks-template.md") (Join-Path $featureDir "tasks.md")

Write-Host "Feature criada: $featureDir" -ForegroundColor Green
""", encoding="utf-8")
    
    # PowerShell: extract-ddp.ps1
    (ps_dir / "extract-ddp.ps1").write_text("""# Script auxiliar para extração de DDP

param(
    [Parameter(Mandatory=$true)]
    [string]$DdpPath
)

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $scriptPath))

# Chamar Python para processar PPT
python -m rpa_speckit.utils.ddp_extractor "$DdpPath"

Write-Host "Extração concluída!" -ForegroundColor Green
""", encoding="utf-8")
    
    # PowerShell: common.ps1
    (ps_dir / "common.ps1").write_text("""# Funções comuns para scripts PowerShell

function Get-ProjectRoot {
    $scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
    return Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $scriptPath))
}

function Test-ProjectStructure {
    $root = Get-ProjectRoot
    $requiredDirs = @(
        ".specify",
        "specs",
        "generated",
        "DDP"
    )
    
    foreach ($dir in $requiredDirs) {
        $path = Join-Path $root $dir
        if (-not (Test-Path $path)) {
            Write-Host "✗ Diretório faltando: $dir" -ForegroundColor Red
            return $false
        }
    }
    
    return $true
}
""", encoding="utf-8")
    
    # Bash: check-prerequisites.sh
    (bash_dir / "check-prerequisites.sh").write_text("""#!/bin/bash
# Verifica pré-requisitos do projeto

echo "Verificando pré-requisitos..."

# Verificar Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✓ Python encontrado: $PYTHON_VERSION"
else
    echo "✗ Python não encontrado!"
    exit 1
fi

# Verificar Git
if command -v git &> /dev/null; then
    GIT_VERSION=$(git --version)
    echo "✓ Git encontrado: $GIT_VERSION"
else
    echo "✗ Git não encontrado!"
    exit 1
fi

echo ""
echo "Todos os pré-requisitos estão instalados!"
""", encoding="utf-8")
    
    # Bash: create-new-feature.sh
    (bash_dir / "create-new-feature.sh").write_text("""#!/bin/bash
# Cria nova feature (specs/001-[nome]/)

if [ -z "$1" ]; then
    echo "Uso: $0 <nome-da-feature>"
    exit 1
fi

FEATURE_NAME="$1"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
SPECS_DIR="$PROJECT_ROOT/specs"

# Encontrar próximo número disponível
MAX_NUMBER=0
for spec_dir in "$SPECS_DIR"/[0-9][0-9][0-9]-*; do
    if [ -d "$spec_dir" ]; then
        NUMBER=$(basename "$spec_dir" | cut -d'-' -f1 | sed 's/^0*//')
        if [ "$NUMBER" -gt "$MAX_NUMBER" ]; then
            MAX_NUMBER=$NUMBER
        fi
    fi
done

NEXT_NUMBER=$((MAX_NUMBER + 1))
FEATURE_NUMBER=$(printf "%03d" $NEXT_NUMBER)
FEATURE_DIR="$SPECS_DIR/$FEATURE_NUMBER-$FEATURE_NAME"

# Criar estrutura
mkdir -p "$FEATURE_DIR/DDP"

# Copiar templates
TEMPLATES_DIR="$PROJECT_ROOT/.specify/templates"
cp "$TEMPLATES_DIR/spec-template.md" "$FEATURE_DIR/spec.md"
cp "$TEMPLATES_DIR/plan-template.md" "$FEATURE_DIR/plan.md"
cp "$TEMPLATES_DIR/selectors-template.md" "$FEATURE_DIR/selectors.md"
cp "$TEMPLATES_DIR/business-rules-template.md" "$FEATURE_DIR/business-rules.md"
cp "$TEMPLATES_DIR/tasks-template.md" "$FEATURE_DIR/tasks.md"

echo "Feature criada: $FEATURE_DIR"
""", encoding="utf-8")
    
    # Bash: extract-ddp.sh
    (bash_dir / "extract-ddp.sh").write_text("""#!/bin/bash
# Script auxiliar para extração de DDP

if [ -z "$1" ]; then
    echo "Uso: $0 <caminho-do-ddp>"
    exit 1
fi

DDP_PATH="$1"

# Chamar Python para processar PPT
python3 -m rpa_speckit.utils.ddp_extractor "$DDP_PATH"

echo "Extração concluída!"
""", encoding="utf-8")
    
    # Bash: common.sh
    (bash_dir / "common.sh").write_text("""#!/bin/bash
# Funções comuns para scripts Bash

get_project_root() {
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    echo "$(cd "$SCRIPT_DIR/../../.." && pwd)"
}

test_project_structure() {
    ROOT=$(get_project_root)
    REQUIRED_DIRS=(".specify" "specs" "generated" "DDP")
    
    for dir in "${REQUIRED_DIRS[@]}"; do
        if [ ! -d "$ROOT/$dir" ]; then
            echo "✗ Diretório faltando: $dir"
            return 1
        fi
    done
    
    return 0
}
""", encoding="utf-8")


def _create_initial_files(project_path: Path, project_name: str):
    """Cria arquivos iniciais do projeto"""
    # README.md
    readme_content = f"""# {project_name}

Projeto de automação RPA criado com RPA Spec-Kit.

## Estrutura do Projeto

\`\`\`
{project_name}/
├── .specify/          # Configurações e templates
│   ├── memory/        # Constitution do framework T2C
│   ├── templates/     # Templates de especificação
│   └── scripts/       # Scripts de automação
├── specs/             # Especificações de automações
│   └── 001-[nome]/    # Primeira automação
│       ├── spec.md
│       ├── plan.md
│       ├── selectors.md
│       ├── business-rules.md
│       ├── tasks.md
│       └── DDP/        # DDPs (Documentos de Design de Processo)
├── generated/         # Framework T2C gerado
└── DDP/               # DDPs gerais
\`\`\`

## Fluxo de Trabalho

1. **Inicialização**: Projeto já inicializado ✓
2. **Extrair DDP**: Coloque DDP.pptx em `specs/001-[nome]/DDP/` e execute `/t2c.extract-ddp`
3. **Completar Specs**: Revise e complete os arquivos .md gerados
4. **Gerar Tasks** (Opcional): Execute `/t2c.tasks` para gerar tasks.md
5. **Implementar**: Execute `/t2c.implement` para gerar o framework T2C completo

## Comandos Disponíveis

- `/t2c.extract-ddp` - Extrai informações de DDP.pptx
- `/t2c.tasks` - Gera tasks.md baseado nas specs
- `/t2c.implement` - Gera framework T2C completo
- `/t2c.validate` - Valida estrutura e completude das specs

## Próximos Passos

1. Crie uma nova feature: `specs/001-[nome-da-automacao]/`
2. Coloque o DDP.pptx na pasta DDP/
3. Execute `/t2c.extract-ddp` para extrair informações
4. Complete os arquivos .md conforme necessário
5. Execute `/t2c.implement` para gerar o framework
"""
    (project_path / "README.md").write_text(readme_content, encoding="utf-8")
    
    # .gitignore
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# RPA Spec-Kit
generated/
*.pptx
*.xlsx
*.db
*.sqlite

# Logs
*.log

# OS
.DS_Store
Thumbs.db
"""
    (project_path / ".gitignore").write_text(gitignore_content, encoding="utf-8")

