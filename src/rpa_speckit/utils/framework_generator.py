"""
Gerador de Código Modular T2C - Gera classes especialistas baseadas em specs
"""
import os
import shutil
from pathlib import Path
from typing import Dict, List, Optional
import re

class T2CFrameworkGenerator:
    """Classe para suportar a geração de código modular"""
    
    def __init__(self, spec_dir: str):
        """
        Inicializa o gerador
        
        Args:
            spec_dir: Diretório com as specs (specs/001-[nome]/)
        """
        self.spec_dir = Path(spec_dir)
        self.specs: Dict = {}
        self.project_name: str = ""
    
    def read_specs(self) -> Dict:
        """Lê todos os arquivos .md preenchidos"""
        required_files = {
            'spec': 'spec.md',
            'selectors': 'selectors.md',
            'business_rules': 'business-rules.md',
            'tasks': 'tasks.md'
        }
        
        specs = {}
        for key, filename in required_files.items():
            file_path = self.spec_dir / filename
            if file_path.exists():
                specs[key] = file_path.read_text(encoding="utf-8")
        
        return specs

    def generate_structure(self, output_dir: Path):
        """
        Gera apenas a estrutura de pastas para os códigos modulares.
        Não gera arquivos de framework nem templates core.
        """
        project_name = self.spec_dir.name.replace("001-", "") if self.spec_dir.name.startswith("001-") else self.spec_dir.name
        
        base_dir = output_dir / project_name / "generated"
        
        # Estrutura sugerida para organização modular
        # A estrutura real será dinâmica baseada nos sistemas (ex: generated/sap, generated/totvs)
        folders = [
            "framework",  # Para arquivos core do T2C (manuais)
            "utils"       # Para utilitários comuns
        ]
        
        for folder in folders:
            (base_dir / folder).mkdir(parents=True, exist_ok=True)
            
        # Cria __init__.py para tornar pacote Python
        (base_dir / "__init__.py").touch()
