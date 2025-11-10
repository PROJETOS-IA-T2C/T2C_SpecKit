"""
Extrator de DDP - Extrai texto de arquivos PPTX
"""
from pathlib import Path
from pptx import Presentation


def extract_ddp(pptx_path: str) -> str:
    """
    Extrai texto de todos os slides de um arquivo DDP.pptx
    
    Args:
        pptx_path: Caminho para o arquivo DDP.pptx
        
    Returns:
        Texto formatado com conteúdo de todos os slides
    """
    pptx_file = Path(pptx_path)
    if not pptx_file.exists():
        raise FileNotFoundError(f"DDP não encontrado: {pptx_path}")
    
    presentation = Presentation(str(pptx_file))
    
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