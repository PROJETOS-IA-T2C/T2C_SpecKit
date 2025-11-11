"""
Comando init - Cria estrutura inicial do projeto
"""
import os
import shutil
from pathlib import Path
from rich.console import Console
try:
    from importlib.resources import files as resource_files
except ImportError:
    # Python < 3.9 fallback
    from importlib_resources import files as resource_files


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
    
    # Criar arquivos iniciais
    console.print("[cyan]Criando arquivos iniciais...[/cyan]")
    _create_initial_files(project_path, project_name)
    
    console.print("[green]✓[/green] Estrutura criada com sucesso!")


def _copy_constitution(project_path: Path):
    """Copia a constitution do framework T2C do template interno"""
    constitution_path = project_path / ".specify/memory/constitution.md"
    
    try:
        # Usar importlib.resources para acessar arquivos do pacote instalado
        from rpa_speckit import memory
        constitution_resource = resource_files(memory) / "constitution.md"
        
        if constitution_resource.is_file():
            # Ler conteúdo do recurso do pacote
            constitution_content = constitution_resource.read_text(encoding="utf-8")
            constitution_path.write_text(constitution_content, encoding="utf-8")
        else:
            raise FileNotFoundError("Constitution não encontrada no pacote")
    except (ImportError, FileNotFoundError, AttributeError):
        # Fallback: tentar caminho relativo (modo desenvolvimento)
        memory_dir = Path(__file__).parent.parent.parent / "memory"
        internal_constitution = memory_dir / "constitution.md"
        
        if internal_constitution.exists():
            shutil.copy2(internal_constitution, constitution_path)
        else:
            # Se não encontrar, criar versão básica
            basic_constitution = """# Constitution do Framework T2C

Este documento define TODAS as regras, especificações, padrões, exemplos e templates que a IA deve seguir ao gerar código para o framework T2C.

**IMPORTANTE:** Este documento é exclusivamente para uso da IA durante a geração de código.

## Nota

A constitution completa do framework T2C deve estar disponível no SpecKit.

A constitution contém todas as regras, padrões e templates necessários para geração de código.
"""
            constitution_path.write_text(basic_constitution, encoding="utf-8")


def _create_templates(project_path: Path):
    """Cria templates vazios para o desenvolvedor preencher"""
    templates_dir = project_path / ".specify/templates"
    
    # Lista de templates para copiar
    template_files = [
        "spec-template.md",
        "tests-template.md",
        "selectors-template.md",
        "business-rules-template.md",
        "tasks-template.md"
    ]
    
    try:
        # Usar importlib.resources para acessar templates do pacote instalado
        from rpa_speckit import templates
        templates_resource = resource_files(templates)
        
        # Copiar cada template do pacote
        for template_file in template_files:
            dest_template = templates_dir / template_file
            template_resource = templates_resource / template_file
            
            if template_resource.is_file():
                # Ler conteúdo do recurso do pacote
                template_content = template_resource.read_text(encoding="utf-8")
                dest_template.write_text(template_content, encoding="utf-8")
            else:
                # Fallback: criar arquivo vazio se template não existir
                dest_template.write_text(f"# {template_file}\n\n[Template não encontrado no pacote]", encoding="utf-8")
    except (ImportError, AttributeError):
        # Fallback: tentar caminho relativo (modo desenvolvimento)
        internal_templates_dir = Path(__file__).parent.parent.parent / "templates"
        
        for template_file in template_files:
            source_template = internal_templates_dir / template_file
            dest_template = templates_dir / template_file
            
            if source_template.exists():
                shutil.copy2(source_template, dest_template)
            else:
                # Fallback: criar arquivo vazio se template não existir
                dest_template.write_text(f"# {template_file}\n\n[Template não encontrado]", encoding="utf-8")


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

1. **EXECUTA o script pronto**: `python -m rpa_speckit.utils.ddp_extractor [caminho_do_ddp]`
2. O script extrai texto de todos os slides do PPTX usando python-pptx
3. Apresenta o texto extraído para a LLM
4. **A LLM preenche os arquivos de especificação** baseado no texto extraído:
   - \`specs/001-[nome]/spec.md\` - Especificação técnica e arquitetura (ARQUIVO PRINCIPAL)
   - \`specs/001-[nome]/tests.md\` - Cenários de teste e validações
   - \`specs/001-[nome]/selectors.md\` - Seletores Clicknium
   - \`specs/001-[nome]/business-rules.md\` - Regras de negócio

## Instruções para a LLM

**IMPORTANTE**: NÃO crie um novo script Python. Use o script pronto que já existe:

1. **Execute o comando**: `python -m rpa_speckit.utils.ddp_extractor [caminho_do_ddp]`
2. **Leia o texto extraído** que será exibido no output
3. **Crie ou atualize** os arquivos de especificação na pasta \`specs/001-[nome]/\`
4. **Preencha** cada arquivo baseado no conteúdo do DDP:
   - **spec.md**: ARQUIVO PRINCIPAL - Definir arquitetura completa (INIT, FILA, LOOP STATION, END PROCESS), stack tecnológica, integrações, estrutura de dados
   - **tests.md**: Extrair cenários de usuário, requisitos funcionais/não-funcionais, critérios de sucesso, entidades principais
   - **selectors.md**: Identificar elementos de UI mencionados no DDP (botões, campos, tabelas, etc.)
   - **business-rules.md**: Extrair validações (VAL*), condições especiais (COND*), regras de processamento (REG*)

5. **Use os templates** em \`.specify/templates/\` como referência para a estrutura
6. **Mantenha a numeração** das regras (VAL001, VAL002, etc.) e tarefas (Task 1.1, Task 2.1, etc.)

## Notas

- **NÃO crie novos scripts** - use o script pronto: `python -m rpa_speckit.utils.ddp_extractor`
- O script já está instalado e pronto para uso
- Se os arquivos já existirem, atualize-os com as novas informações do DDP
- Mantenha a estrutura e formatação dos templates
""", encoding="utf-8")
    
    # t2c.tasks.md
    (commands_dir / "t2c.tasks.md").write_text("""# Gerar Tasks

Gera o arquivo tasks.md baseado em spec.md e business-rules.md.

## Uso

\`\`\`
/t2c.tasks [caminho_da_spec]
\`\`\`

## Exemplo

\`\`\`
/t2c.tasks specs/001-automacao-exemplo
\`\`\`

## O que faz

1. Lê spec.md e business-rules.md
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
   - spec.md (ARQUIVO PRINCIPAL - arquitetura completa)
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
   - spec.md (ARQUIVO PRINCIPAL)
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
│   └── templates/     # Templates de especificação
├── specs/             # Especificações de automações
│   └── 001-[nome]/    # Primeira automação
│       ├── spec.md     # ARQUIVO PRINCIPAL - Arquitetura completa
│       ├── tests.md    # Cenários de teste e validações
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

