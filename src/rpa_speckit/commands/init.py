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
        ".specify/scripts",
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
    
    # Criar script de extração de DDP
    console.print("[cyan]Criando script de extração de DDP...[/cyan]")
    _create_extract_ddp_script(project_path)
    
    # Criar requirements.txt
    console.print("[cyan]Criando requirements.txt...[/cyan]")
    _create_requirements_txt(project_path)
    
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


def _create_extract_ddp_script(project_path: Path):
    """Cria script Python pronto para extração de DDP"""
    scripts_dir = project_path / ".specify/scripts"
    
    # Usar raw string para evitar problemas com escape e encoding
    script_content = r'''#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para extração de texto de arquivos DDP.pptx
Este script já está pronto e não deve ser modificado.
"""
import sys
import os
import subprocess
from pathlib import Path

try:
    from pptx import Presentation
except ImportError:
    print("python-pptx não está instalado. Instalando automaticamente...", file=sys.stderr)
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "python-pptx>=0.6.21"], 
                             stdout=sys.stderr, stderr=sys.stderr)
        from pptx import Presentation
        print("python-pptx instalado com sucesso!", file=sys.stderr)
    except Exception as e:
        print(f"Erro ao instalar python-pptx: {e}", file=sys.stderr)
        print("Tente instalar manualmente: pip install python-pptx", file=sys.stderr)
        sys.exit(1)


def extract_ddp(pptx_path: str) -> str:
    """
    Extrai texto de todos os slides de um arquivo DDP.pptx
    
    Args:
        pptx_path: Caminho para o arquivo DDP.pptx (pode ser relativo, absoluto ou apenas nome do arquivo)
        
    Returns:
        Texto formatado com conteúdo de todos os slides
    """
    # Converter para Path e resolver para absoluto (simples e direto)
    pptx_file = Path(pptx_path).resolve()
    
    # Se não encontrar, procurar automaticamente nas pastas comuns
    if not pptx_file.exists():
        # Procurar em DDP/ primeiro
        ddp_dir = Path("DDP")
        if ddp_dir.exists():
            pptx_files = list(ddp_dir.glob("*.pptx"))
            if pptx_files:
                pptx_file = pptx_files[0].resolve()
        
        # Se não encontrou, procurar em specs/*/DDP/
        if not pptx_file.exists():
            for spec_dir in Path("specs").glob("*/DDP"):
                if spec_dir.exists():
                    pptx_files = list(spec_dir.glob("*.pptx"))
                    if pptx_files:
                        pptx_file = pptx_files[0].resolve()
                        break
        
        if not pptx_file.exists():
            raise FileNotFoundError(f"DDP não encontrado: {pptx_path}")
    
    # Usar caminho absoluto sempre (simples)
    presentation = Presentation(str(pptx_file.absolute()))
    
    # Formatar texto para apresentar à LLM
    formatted_text = "# Conteúdo Extraído do DDP\n\n"
    formatted_text += f"**Arquivo:** {pptx_path}\n\n"
    formatted_text += f"**Total de slides:** {len(presentation.slides)}\n\n"
    formatted_text += "---\n\n"
    
    # Passar slide por slide e extrair texto
    for i, slide in enumerate(presentation.slides, 1):
        slide_text = []
        
        # Extrair texto de todas as formas no slide
        for shape in slide.shapes:
            if hasattr(shape, "text") and shape.text.strip():
                slide_text.append(shape.text.strip())
        
        # Adicionar slide ao texto formatado
        formatted_text += f"## Slide {i}\n\n"
        formatted_text += "\n".join(slide_text)
        formatted_text += "\n\n---\n\n"
    
    return formatted_text


def main():
    """CLI para extração de DDP"""
    # Configurar encoding UTF-8 para stdout/stderr no Windows
    if sys.platform == 'win32':
        import io
        try:
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
        except:
            pass
    
    # Se não passou caminho, procurar automaticamente
    if len(sys.argv) < 2:
        # Procurar arquivos .pptx nas pastas comuns
        search_dirs = [Path("DDP")]
        for spec_dir in Path("specs").glob("*/DDP"):
            search_dirs.append(spec_dir)
        
        pptx_file = None
        for search_dir in search_dirs:
            if search_dir.exists():
                pptx_files = list(search_dir.glob("*.pptx"))
                if pptx_files:
                    pptx_file = pptx_files[0].resolve()
                    break
        
        if not pptx_file:
            print("Erro: Nenhum arquivo .pptx encontrado. Use: python .specify/scripts/extract-ddp.py <caminho>", file=sys.stderr)
            sys.exit(1)
        
        ddp_path = str(pptx_file)
    else:
        ddp_path = sys.argv[1]
    
    try:
        extracted_text = extract_ddp(ddp_path)
        print(extracted_text)
    except FileNotFoundError as e:
        print(f"Erro: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Erro ao extrair DDP: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
'''
    
    extract_script = scripts_dir / "extract-ddp.py"
    extract_script.write_text(script_content, encoding="utf-8")


def _create_requirements_txt(project_path: Path):
    """Cria requirements.txt com dependências necessárias"""
    requirements_content = """# Dependências para scripts do projeto
python-pptx>=0.6.21
"""
    (project_path / "requirements.txt").write_text(requirements_content, encoding="utf-8")


def _get_command_content(command_name: str) -> str:
    """Retorna o conteúdo completo de um comando (reutilizável para Cursor e VS Code)"""
    commands = {
        "t2c.extract-ddp": """# Extrair DDP

Extrai o texto de todos os slides de um arquivo DDP.pptx para que a LLM possa preencher os arquivos de especificação.

## Uso

\`\`\`
/t2c.extract-ddp [caminho_do_ddp]
\`\`\`

## Exemplo

\`\`\`
/t2c.extract-ddp specs/001-automacao-exemplo/DDP/ddp.pptx
\`\`\`

## ⚠️ REGRA ABSOLUTA - LEIA ANTES DE QUALQUER AÇÃO

**VOCÊ NÃO DEVE CRIAR NENHUM SCRIPT PYTHON. NUNCA. EM NENHUMA CIRCUNSTÂNCIA.**

- ❌ NÃO crie scripts temporários
- ❌ NÃO crie arquivos `_temp_extract_ddp.py` ou similares
- ❌ NÃO crie scripts alternativos
- ❌ NÃO tente "resolver" problemas criando código
- ✅ APENAS execute o script pronto que já existe no projeto

## O que fazer

**PASSO 1 - Execute APENAS este comando (SIMPLES):**

\`\`\`bash
python .specify/scripts/extract-ddp.py
\`\`\`

**OU se quiser especificar o arquivo:**

\`\`\`bash
python .specify/scripts/extract-ddp.py DDP/arquivo.pptx
\`\`\`

**Como funciona:**
- Se você **não passar caminho**, o script procura automaticamente o primeiro arquivo .pptx em `DDP/` ou `specs/*/DDP/`
- Se você **passar caminho**, pode ser relativo ou absoluto - o script resolve automaticamente
- **Instala dependências automaticamente** se necessário (python-pptx)
- **SIMPLES**: Apenas execute o comando, o script faz TUDO sozinho

**PASSO 2 - Se o comando funcionar:**

1. Leia o texto extraído que será exibido no output
2. Crie ou atualize os arquivos de especificação na pasta \`specs/001-[nome]/\`
3. Preencha cada arquivo baseado no conteúdo do DDP

## Arquivos a preencher

- \`specs/001-[nome]/spec.md\` - Especificação técnica e arquitetura (ARQUIVO PRINCIPAL)
- \`specs/001-[nome]/tests.md\` - Cenários de teste e validações
- \`specs/001-[nome]/selectors.md\` - Seletores Clicknium
- \`specs/001-[nome]/business-rules.md\` - Regras de negócio

## Detalhes dos arquivos

- **spec.md**: ARQUIVO PRINCIPAL - Definir arquitetura completa (INIT, FILA, LOOP STATION, END PROCESS), stack tecnológica, integrações, estrutura de dados
- **tests.md**: Extrair cenários de usuário, requisitos funcionais/não-funcionais, critérios de sucesso, entidades principais
- **selectors.md**: Identificar elementos de UI mencionados no DDP (botões, campos, tabelas, etc.)
- **business-rules.md**: Extrair validações (VAL*), condições especiais (COND*), regras de processamento (REG*)

## Lembre-se

- O script `.specify/scripts/extract-ddp.py` JÁ EXISTE no projeto e está pronto
- Você apenas precisa EXECUTÁ-LO, não criá-lo
- Use os templates em \`.specify/templates/\` como referência para a estrutura
- Mantenha a numeração das regras (VAL001, VAL002, etc.) e tarefas (Task 1.1, Task 2.1, etc.)
- Se os arquivos já existirem, atualize-os com as novas informações do DDP""",
        "t2c.tasks": """# Gerar Tasks

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
- As tarefas geradas devem ser revisadas e ajustadas conforme necessário""",
        "t2c.implement": """# Implementar Framework T2C

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
- Arquivos do framework base são copiados (não modificados)""",
        "t2c.validate": """# Validar Especificações

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
- Corrija os problemas indicados antes de prosseguir"""
    }
    return commands.get(command_name, "")


def _create_cursor_commands(project_path: Path):
    """Cria comandos Cursor"""
    commands_dir = project_path / ".cursor/commands"
    
    # Usar a mesma função para garantir conteúdo idêntico
    for cmd_name in ["t2c.extract-ddp", "t2c.tasks", "t2c.implement", "t2c.validate"]:
        content = _get_command_content(cmd_name)
        (commands_dir / f"{cmd_name}.md").write_text(content, encoding="utf-8")


def _create_vscode_config(project_path: Path, ai_assistant: str):
    """Cria configurações VS Code com comandos equivalentes ao Cursor"""
    vscode_dir = project_path / ".vscode"
    commands_dir = vscode_dir / "commands"
    commands_dir.mkdir(exist_ok=True)
    
    # Criar diretório .github para copilot-instructions
    github_dir = project_path / ".github"
    github_dir.mkdir(exist_ok=True)
    
    # Criar settings.json
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
    
    # Criar comandos markdown (EXATAMENTE como no Cursor, com slash commands)
    _create_vscode_commands(commands_dir)
    
    # Criar arquivo de instruções do Copilot
    _create_copilot_instructions(github_dir, commands_dir)
    
    # Criar tasks.json (para executar scripts)
    _create_vscode_tasks(vscode_dir)
    
    # Criar README explicando como usar
    _create_vscode_readme(vscode_dir)


def _create_vscode_commands(commands_dir: Path):
    """Cria arquivos markdown de comandos EXATAMENTE como no Cursor (com slash commands)"""
    
    # Usar a mesma função para garantir conteúdo idêntico
    for cmd_name in ["t2c.extract-ddp", "t2c.tasks", "t2c.implement", "t2c.validate"]:
        content = _get_command_content(cmd_name)
        (commands_dir / f"{cmd_name}.md").write_text(content, encoding="utf-8")


def _create_copilot_instructions(github_dir: Path, commands_dir: Path):
    """Cria arquivo de instruções do Copilot para suportar slash commands"""
    instructions_content = """# GitHub Copilot Instructions - T2C Commands

Este projeto usa comandos slash customizados (similar ao Cursor) que devem ser reconhecidos pelo GitHub Copilot Chat.

## Comandos Disponíveis

Quando o usuário digitar um comando slash no chat do Copilot, você deve:

1. **Reconhecer o comando**: Se o usuário digitar `/t2c.extract-ddp`, `/t2c.tasks`, `/t2c.implement`, ou `/t2c.validate`
2. **Ler o arquivo correspondente**: Consulte `.vscode/commands/[nome-do-comando].md` para entender o que fazer
3. **Executar as instruções**: Siga EXATAMENTE as instruções do arquivo markdown

## Comandos Slash Customizados

### `/t2c.extract-ddp [caminho]`
- **Arquivo de referência**: `.vscode/commands/t2c.extract-ddp.md`
- **Função**: Extrai texto de arquivos DDP.pptx
- **Uso**: `/t2c.extract-ddp` ou `/t2c.extract-ddp specs/001-exemplo/DDP/ddp.pptx`

### `/t2c.tasks [caminho]`
- **Arquivo de referência**: `.vscode/commands/t2c.tasks.md`
- **Função**: Gera arquivo tasks.md baseado em spec.md e business-rules.md
- **Uso**: `/t2c.tasks specs/001-exemplo`

### `/t2c.implement [caminho]`
- **Arquivo de referência**: `.vscode/commands/t2c.implement.md`
- **Função**: Gera framework T2C completo baseado nas especificações
- **Uso**: `/t2c.implement specs/001-exemplo`

### `/t2c.validate [caminho]`
- **Arquivo de referência**: `.vscode/commands/t2c.validate.md`
- **Função**: Valida estrutura e completude dos arquivos de especificação
- **Uso**: `/t2c.validate specs/001-exemplo`

## Como Funcionar

Quando o usuário usar um slash command:

1. **Detecte o comando**: Se começar com `/t2c.`, é um comando customizado
2. **Leia o arquivo**: Abra e leia o conteúdo de `.vscode/commands/[comando].md`
3. **Siga as instruções**: Execute EXATAMENTE o que está descrito no arquivo
4. **Respeite as regras**: Preste atenção especial às seções "⚠️ REGRA ABSOLUTA"

## Importante

- **NUNCA crie scripts Python** quando o comando pedir para executar um script existente
- **SEMPRE leia o arquivo markdown** antes de executar qualquer ação
- **Siga as instruções passo a passo** conforme descrito nos arquivos de comando
- **Use os templates** em `.specify/templates/` como referência quando necessário

## Estrutura de Arquivos

```
.vscode/
└── commands/
    ├── t2c.extract-ddp.md  # Instruções completas para extrair DDP
    ├── t2c.tasks.md         # Instruções para gerar tasks.md
    ├── t2c.implement.md     # Instruções para implementar framework
    └── t2c.validate.md      # Instruções para validar specs
```

Cada arquivo contém instruções detalhadas sobre como executar o comando correspondente.
"""
    
    (github_dir / "copilot-instructions.md").write_text(instructions_content, encoding="utf-8")


def _create_vscode_tasks(vscode_dir: Path):
    """Cria tasks.json com tasks para executar os scripts"""
    tasks = {
        "version": "2.0.0",
        "tasks": [
            {
                "label": "T2C: Extract DDP",
                "type": "shell",
                "command": "python",
                "args": [
                    "${workspaceFolder}/.specify/scripts/extract-ddp.py"
                ],
                "problemMatcher": [],
                "presentation": {
                    "reveal": "always",
                    "panel": "new"
                },
                "group": {
                    "kind": "build",
                    "isDefault": False
                }
            },
            {
                "label": "T2C: Extract DDP (with file)",
                "type": "shell",
                "command": "python",
                "args": [
                    "${workspaceFolder}/.specify/scripts/extract-ddp.py",
                    "${input:ddpPath}"
                ],
                "problemMatcher": [],
                "presentation": {
                    "reveal": "always",
                    "panel": "new"
                },
                "group": {
                    "kind": "build",
                    "isDefault": False
                }
            }
        ],
        "inputs": [
            {
                "id": "ddpPath",
                "type": "promptString",
                "description": "Caminho do arquivo DDP (relativo ao workspace)",
                "default": "DDP/ddp.pptx"
            }
        ]
    }
    
    import json
    (vscode_dir / "tasks.json").write_text(
        json.dumps(tasks, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )


def _create_vscode_readme(vscode_dir: Path):
    """Cria README explicando como usar os comandos com GitHub Copilot"""
    readme_content = """# Comandos T2C para VS Code + GitHub Copilot

Este diretório contém os comandos T2C disponíveis para uso com GitHub Copilot.

## Como Usar

### Método 1: Slash Commands (Igual ao Cursor) ⭐

No chat do GitHub Copilot, use os slash commands diretamente:

- **Extrair DDP**: `/t2c.extract-ddp` ou `/t2c.extract-ddp specs/001-exemplo/DDP/ddp.pptx`
- **Gerar Tasks**: `/t2c.tasks specs/001-exemplo`
- **Implementar Framework**: `/t2c.implement specs/001-exemplo`
- **Validar Specs**: `/t2c.validate specs/001-exemplo`

O Copilot reconhecerá os slash commands e lerá automaticamente os arquivos em `.vscode/commands/` para entender o que fazer.

**Nota**: O arquivo `.github/copilot-instructions.md` contém instruções para o Copilot sobre como processar esses comandos.

### Método 2: Mencionar ao GitHub Copilot

Você também pode mencionar o comando diretamente:

- **Extrair DDP**: "Execute o comando t2c.extract-ddp" ou "Extrair DDP usando t2c.extract-ddp"
- **Gerar Tasks**: "Execute o comando t2c.tasks" ou "Gerar tasks usando t2c.tasks"
- **Implementar Framework**: "Execute o comando t2c.implement" ou "Implementar framework usando t2c.implement"
- **Validar Specs**: "Execute o comando t2c.validate" ou "Validar specs usando t2c.validate"

### Método 3: Usar Tasks do VS Code

1. Pressione `Ctrl+Shift+P` (ou `Cmd+Shift+P` no Mac)
2. Digite "Tasks: Run Task"
3. Selecione uma das tasks disponíveis:
   - **T2C: Extract DDP** - Extrai DDP automaticamente
   - **T2C: Extract DDP (with file)** - Extrai DDP de um arquivo específico

### Método 4: Executar Scripts Diretamente

Você também pode executar os scripts diretamente no terminal:

```bash
# Extrair DDP (procura automaticamente)
python .specify/scripts/extract-ddp.py

# Extrair DDP de arquivo específico
python .specify/scripts/extract-ddp.py DDP/arquivo.pptx
```

## Comandos Disponíveis

### t2c.extract-ddp

Extrai o texto de todos os slides de um arquivo DDP.pptx.

**Uso com Copilot:**
- "Execute t2c.extract-ddp"
- "Extrair DDP do arquivo specs/001-exemplo/DDP/ddp.pptx"

### t2c.tasks

Gera o arquivo tasks.md baseado em spec.md e business-rules.md.

**Uso com Copilot:**
- "Execute t2c.tasks para specs/001-exemplo"
- "Gerar tasks.md baseado nas specs"

### t2c.implement

Gera o framework T2C completo baseado nas especificações.

**Uso com Copilot:**
- "Execute t2c.implement para specs/001-exemplo"
- "Implementar framework T2C completo"

### t2c.validate

Valida a estrutura e completude dos arquivos de especificação.

**Uso com Copilot:**
- "Execute t2c.validate para specs/001-exemplo"
- "Validar todas as specs"

## Documentação Completa

Consulte os arquivos em `.vscode/commands/` para documentação detalhada de cada comando:
- `t2c.extract-ddp.md`
- `t2c.tasks.md`
- `t2c.implement.md`
- `t2c.validate.md`

## Dicas

1. **Sempre mencione o comando completo**: "t2c.extract-ddp" em vez de apenas "extrair"
2. **Seja específico sobre o caminho**: "t2c.extract-ddp specs/001-exemplo/DDP/ddp.pptx"
3. **Leia a documentação**: O Copilot pode ler os arquivos `.md` para entender melhor o que fazer
4. **Use as tasks**: Para execução rápida, use as tasks do VS Code (`Ctrl+Shift+P` > "Tasks: Run Task")
"""
    
    (vscode_dir / "README.md").write_text(readme_content, encoding="utf-8")


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
│   └── scripts/       # Scripts prontos (extract-ddp.py)
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
2. **Extrair DDP**: Coloque DDP.pptx em `specs/001-[nome]/DDP/` ou `DDP/` e execute `/t2c.extract-ddp`
   - O script instala dependências automaticamente se necessário
4. **Completar Specs**: Revise e complete os arquivos .md gerados
5. **Gerar Tasks** (Opcional): Execute `/t2c.tasks` para gerar tasks.md
6. **Implementar**: Execute `/t2c.implement` para gerar o framework T2C completo

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

