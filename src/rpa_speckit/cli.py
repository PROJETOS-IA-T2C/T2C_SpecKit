"""
CLI principal do RPA Spec-Kit
"""
import click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import box
from rich.align import Align

from rpa_speckit.commands.init import init_project
from rpa_speckit.utils.ddp_extractor import extract_ddp
from pathlib import Path

console = Console()


def print_banner():
    """Exibe o banner do T2C SpecKit com ASCII Art e degradê"""
    
    # ASCII Art do T2C SpecKit (T2C em cima, SPECKIT embaixo)
    ascii_art = """
    ╔══════════════════════════════════════════════════════════════════════════════╗
    ║                                                                              ║
    ║   ████████╗██████╗  ██████╗      ██████╗ ██████╗  █████╗                     ║
    ║   ╚══██╔══╝╚════██╗██╔════╝      ██╔══██╗██╔══██╗██╔══██╗                    ║
    ║      ██║    █████╔╝██║           ██████╔╝██████╔╝███████║                    ║
    ║      ██║   ██╔══██╗██║           ██╔══██╗██╔═══╝ ██╔══██║                    ║
    ║      ██║   ██████╔╝╚██████╗      ██║  ██║██║     ██║  ██║                    ║
    ║      ╚═╝   ╚═════╝  ╚═════╝      ╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝                    ║
    ║                                                                              ║
    ║           ███████╗██████╗ ███████╗ ██████╗██╗  ██╗██╗████████╗               ║
    ║           ██╔════╝██╔══██╗██╔════╝██╔════╝██║ ██╔╝██║╚══██╔══╝               ║
    ║           ███████╗██████╔╝█████╗  ██║     █████╔╝ ██║   ██║                  ║
    ║           ╚════██║██╔═══╝ ██╔══╝  ██║     ██╔═██╗ ██║   ██║                  ║
    ║           ███████║██║     ███████╗╚██████╗██║  ██╗██║   ██║                  ║
    ║           ╚══════╝╚═╝     ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝   ╚═╝                  ║
    ║                                                                              ║
    ║       > AUTOMATION INTELLIGENCE       > SPEC-DRIVEN DEVELOPMENT              ║
    ║       > VERSION: 0.1.0                > FRAMEWORK: T2C                       ║
    ║                                                                              ║
    ╚══════════════════════════════════════════════════════════════════════════════╝
    """
    
    # Criar texto com degradê de cores suave
    lines = ascii_art.strip().split('\n')
    banner_text = Text()
    
    # Paleta de cores para degradê suave (cyan -> blue -> purple -> cyan)
    color_palette = [
        "bright_cyan", "cyan", "bright_blue", "blue",
        "bright_magenta", "magenta", "bright_blue", "cyan",
        "bright_cyan", "cyan", "bright_blue", "blue"
    ]
    
    for i, line in enumerate(lines):
        # Calcular índice de cor baseado na posição (degradê suave)
        color_index = int((i / len(lines)) * len(color_palette))
        color_index = min(color_index, len(color_palette) - 1)
        color = color_palette[color_index]
        
        # Aplicar estilos especiais
        if i == 0 or i == len(lines) - 1:
            # Bordas superiores e inferiores
            banner_text.append(line + "\n", style=f"bold {color}")
        elif "═══" in line:
            # Linhas decorativas
            banner_text.append(line + "\n", style=f"bold bright_{color}")
        elif any(keyword in line for keyword in ["T2C", "SpecKit", "Spec-Driven", "Framework", "Toolkit", "Integration"]):
            # Textos importantes
            banner_text.append(line + "\n", style=f"bold bright_{color}")
        else:
            # Linhas normais
            banner_text.append(line + "\n", style=color)
    
    # Criar painel com borda decorativa
    panel = Panel(
        banner_text,
        border_style="bright_cyan",
        box=box.DOUBLE_EDGE,
        padding=(1, 1),
    )
    
    console.print()
    console.print(Align.center(panel))
    console.print()
    
    # Mensagem de boas-vindas com estilo e emoji
    welcome = Text()
    welcome.append("🚀 ", style="bold yellow")
    welcome.append("Bem-vindo ao ", style="bright_white")
    welcome.append("T2C SpecKit", style="bold bright_cyan")
    welcome.append(" - Crie automações RPA de forma estruturada e eficiente! ", style="bright_white")
    welcome.append("✨", style="bold yellow")
    
    console.print(Align.center(welcome))
    console.print()


@click.group()
@click.version_option(version="0.1.0", prog_name="t2c")
def cli():
    """
    T2C SpecKit - Toolkit para Spec-Driven Development de RPA
    
    Crie projetos de automação RPA seguindo o padrão Spec-Driven Development
    com integração completa ao Framework T2C.
    """
    pass


@cli.command()
@click.argument("project_name", required=False)
def init(project_name):
    """
    Inicializa um novo projeto RPA Spec-Kit.
    
    Se PROJECT_NAME não for fornecido, será solicitado interativamente.
    """
    print_banner()
    
    # Se não forneceu nome, pedir interativamente
    if not project_name:
        project_name = console.input("[bold cyan]Nome do projeto:[/bold cyan] ").strip()
        if not project_name:
            console.print("[bold red]Erro:[/bold red] Nome do projeto é obrigatório.")
            raise click.Abort()
    
    # Perguntar qual AI Assistant
    console.print("\n[bold yellow]Selecione seu AI Assistant:[/bold yellow]")
    console.print("  [cyan]1.[/cyan] Cursor")
    console.print("  [cyan]2.[/cyan] VS Code + GitHub Copilot")
    
    choice = console.input("\n[bold cyan]Escolha (1-2):[/bold cyan] ").strip()
    
    ai_assistant_map = {
        "1": "cursor",
        "2": "vscode-copilot"
    }
    
    ai_assistant = ai_assistant_map.get(choice, "cursor")
    
    # Confirmar criação
    console.print(f"\n[bold yellow]Confirmação:[/bold yellow]")
    console.print(f"  [cyan]Projeto:[/cyan] {project_name}")
    console.print(f"  [cyan]AI Assistant:[/cyan] {ai_assistant}")
    
    confirm = console.input("\n[bold yellow]Criar projeto? (s/N):[/bold yellow] ").strip().lower()
    
    if confirm not in ['s', 'sim', 'y', 'yes']:
        console.print("[yellow]Operação cancelada.[/yellow]")
        raise click.Abort()
    
    # Criar projeto
    try:
        init_project(project_name, ai_assistant, console)
        console.print(f"\n[bold green]✓[/bold green] Projeto [bold]{project_name}[/bold] criado com sucesso!")
        console.print("\n[bold cyan]Próximos passos:[/bold cyan]")
        console.print("  1. Abra o projeto no editor escolhido")
        console.print("  2. Coloque o DDP (PPTX ou DOCX) em specs/001-[nome]/DDP/")
        console.print("  3. Execute o comando /t2c.extract-ddp para extrair informações")
        console.print("  4. Complete os arquivos .md conforme necessário")
        console.print("  5. Execute /t2c.implement para gerar o framework T2C")
    except Exception as e:
        console.print(f"\n[bold red]Erro ao criar projeto:[/bold red] {str(e)}")
        raise click.Abort()


@cli.command(name="extract-ddp")
@click.argument("ddp_path", required=False)
def extract_ddp_cmd(ddp_path):
    """
    Extrai texto de um arquivo DDP (PPTX ou DOCX).
    
    Se DDP_PATH não for fornecido, procura automaticamente em DDP/ ou specs/*/DDP/
    """
    try:
        # Se não forneceu caminho, procurar automaticamente
        if not ddp_path:
            console.print("[yellow]Procurando arquivo DDP automaticamente...[/yellow]")
            
            # Procurar em DDP/ primeiro
            ddp_dir = Path("DDP")
            ddp_file = None
            
            if ddp_dir.exists():
                # Procurar PPTX primeiro, depois DOCX
                pptx_files = list(ddp_dir.glob("*.pptx"))
                docx_files = list(ddp_dir.glob("*.docx"))
                if pptx_files:
                    ddp_file = pptx_files[0]
                elif docx_files:
                    ddp_file = docx_files[0]
            
            # Se não encontrou, procurar em specs/*/DDP/
            if not ddp_file:
                for spec_dir in Path("specs").glob("*/DDP"):
                    if spec_dir.exists():
                        pptx_files = list(spec_dir.glob("*.pptx"))
                        docx_files = list(spec_dir.glob("*.docx"))
                        if pptx_files:
                            ddp_file = pptx_files[0]
                            break
                        elif docx_files:
                            ddp_file = docx_files[0]
                            break
            
            if not ddp_file:
                console.print("[bold red]Erro:[/bold red] Nenhum arquivo DDP (.pptx ou .docx) encontrado.")
                console.print("  Procurou em: DDP/ e specs/*/DDP/")
                console.print("  Use: t2c extract-ddp <caminho_do_arquivo>")
                raise click.Abort()
            
            ddp_path = str(ddp_file)
            console.print(f"[green]Arquivo encontrado:[/green] {ddp_path}")
        
        # Extrair conteúdo
        console.print(f"\n[cyan]Extraindo conteúdo de:[/cyan] {ddp_path}")
        extracted_text = extract_ddp(ddp_path)
        
        # Exibir resultado
        console.print("\n" + "="*80)
        console.print(extracted_text)
        console.print("="*80)
        
    except FileNotFoundError as e:
        console.print(f"[bold red]Erro:[/bold red] {e}")
        raise click.Abort()
    except ValueError as e:
        console.print(f"[bold red]Erro:[/bold red] {e}")
        raise click.Abort()
    except Exception as e:
        console.print(f"[bold red]Erro ao extrair DDP:[/bold red] {str(e)}")
        raise click.Abort()


def main():
    """Ponto de entrada principal"""
    cli()


if __name__ == "__main__":
    main()

