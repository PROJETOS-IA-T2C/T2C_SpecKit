"""
Extrator de DDP - Extrai texto de arquivos PPTX e DOCX
"""
from pathlib import Path
from pptx import Presentation
from docx import Document


def extract_ddp(ddp_path: str) -> str:
    """
    Extrai texto de um arquivo DDP (PPTX ou DOCX)
    
    Args:
        ddp_path: Caminho para o arquivo DDP (pode ser .pptx ou .docx)
        
    Returns:
        Texto formatado com conteúdo do arquivo
    """
    ddp_file = Path(ddp_path)
    if not ddp_file.exists():
        raise FileNotFoundError(f"DDP não encontrado: {ddp_path}")
    
    # Detectar tipo de arquivo pela extensão
    file_ext = ddp_file.suffix.lower()
    
    if file_ext == '.pptx':
        return _extract_pptx(ddp_file, ddp_path)
    elif file_ext in ['.docx', '.doc']:
        return _extract_docx(ddp_file, ddp_path)
    else:
        raise ValueError(f"Formato não suportado: {file_ext}. Use .pptx ou .docx")


def _extract_pptx(pptx_file: Path, original_path: str) -> str:
    """Extrai texto de um arquivo PPTX"""
    presentation = Presentation(str(pptx_file))
    
    # Formatar texto para apresentar à LLM
    formatted_text = "# Conteúdo Extraído do DDP\n\n"
    formatted_text += f"**Arquivo:** {original_path}\n\n"
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


def _extract_docx(docx_file: Path, original_path: str) -> str:
    """Extrai texto de um arquivo DOCX"""
    doc = Document(str(docx_file))
    
    # Formatar texto para apresentar à LLM (mesmo formato do PPTX)
    formatted_text = "# Conteúdo Extraído do DDP\n\n"
    formatted_text += f"**Arquivo:** {original_path}\n\n"
    
    # Contar parágrafos não vazios como "slides"
    paragraphs = [p for p in doc.paragraphs if p.text.strip()]
    formatted_text += f"**Total de slides:** {len(paragraphs)}\n\n"
    formatted_text += "---\n\n"
    
    # Passar parágrafo por parágrafo e extrair texto
    slide_num = 1
    for paragraph in doc.paragraphs:
        text = paragraph.text.strip()
        if text:  # Apenas parágrafos não vazios
            formatted_text += f"## Slide {slide_num}\n\n"
            formatted_text += text
            formatted_text += "\n\n---\n\n"
            slide_num += 1
    
    return formatted_text


def main():
    """CLI para extração de DDP"""
    import sys
    import io
    
    # Configurar encoding UTF-8 para stdout/stderr no Windows
    if sys.platform == 'win32':
        try:
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
        except:
            pass
    
    if len(sys.argv) < 2:
        print("Uso: python -m rpa_speckit.utils.ddp_extractor <caminho_do_ddp>", file=sys.stderr)
        sys.exit(1)
    
    ddp_path = sys.argv[1]
    
    try:
        extracted_text = extract_ddp(ddp_path)
        print(extracted_text)
    except FileNotFoundError as e:
        print(f"Erro: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Erro: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Erro ao extrair DDP: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()