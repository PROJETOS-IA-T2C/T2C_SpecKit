"""
Gerador de Framework T2C - Gera framework completo baseado em specs
"""
import os
import shutil
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Optional
import re


class T2CFrameworkGenerator:
    """Classe para gerar framework T2C completo"""
    
    def __init__(self, spec_dir: str, framework_repo_url: Optional[str] = None):
        """
        Inicializa o gerador
        
        Args:
            spec_dir: Diretório com as specs (specs/001-[nome]/)
            framework_repo_url: URL do repositório do framework T2C (opcional)
        """
        self.spec_dir = Path(spec_dir)
        self.framework_repo_url = framework_repo_url or "https://github.com/T2C-Consultoria/prj_botcity_framework_template.git"
        self.specs: Dict = {}
        self.project_name: str = ""
        self.generated_dir: Path = None
    
    def read_specs(self) -> Dict:
        """
        Lê todos os arquivos .md preenchidos
        
        Returns:
            Dicionário com todas as specs
        """
        required_files = {
            'spec': 'spec.md',
            'plan': 'plan.md',
            'selectors': 'selectors.md',
            'business_rules': 'business-rules.md',
            'tasks': 'tasks.md'
        }
        
        for key, filename in required_files.items():
            file_path = self.spec_dir / filename
            if file_path.exists():
                self.specs[key] = file_path.read_text(encoding="utf-8")
            else:
                raise FileNotFoundError(f"Arquivo obrigatório não encontrado: {filename}")
        
        # Ler configs se existirem
        config_dir = self.spec_dir.parent.parent / "config"
        if config_dir.exists():
            self.specs['configs'] = {}
            for config_file in config_dir.glob("*.md"):
                self.specs['configs'][config_file.stem] = config_file.read_text(encoding="utf-8")
        
        return self.specs
    
    def validate_specs(self) -> List[str]:
        """
        Valida completude das specs
        
        Returns:
            Lista de erros encontrados (vazia se tudo OK)
        """
        errors = []
        
        # Verificar se arquivos existem
        required_files = ['spec', 'plan', 'selectors', 'business_rules', 'tasks']
        for key in required_files:
            if key not in self.specs:
                errors.append(f"Arquivo {key} não encontrado")
        
        # Verificar se spec não está vazio
        if 'spec' in self.specs:
            if len(self.specs['spec'].strip()) < 100:
                errors.append("spec.md parece estar vazio ou incompleto")
        
        # Verificar se plan tem stack definida
        if 'plan' in self.specs:
            if 'T2C Framework' not in self.specs['plan']:
                errors.append("plan.md não menciona T2C Framework")
        
        return errors
    
    def determine_project_name(self) -> str:
        """
        Determina o nome do projeto
        
        Returns:
            Nome do projeto
        """
        # Tentar obter de config/base.md
        if 'configs' in self.specs and 'base' in self.specs['configs']:
            # Procurar por padrão de nome
            match = re.search(r'NomeProjeto[:\s]+([^\n]+)', self.specs['configs']['base'], re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        # Usar nome do diretório da spec
        dir_name = self.spec_dir.name
        if dir_name.startswith('001-'):
            return dir_name[4:]  # Remove "001-"
        return dir_name
    
    def download_framework(self, target_dir: Path, project_name: str) -> Path:
        """
        Baixa framework do GitHub usando cookiecutter
        
        Args:
            target_dir: Diretório onde baixar
            project_name: Nome do projeto para cookiecutter
            
        Returns:
            Caminho do framework baixado
        """
        framework_dir = target_dir / "t2c_framework_temp"
        
        if framework_dir.exists():
            shutil.rmtree(framework_dir)
        
        # Verificar se cookiecutter está instalado
        try:
            subprocess.run(["cookiecutter", "--version"], check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Se cookiecutter não estiver instalado, tentar instalar ou usar git clone
            try:
                subprocess.run(
                    ["pip", "install", "cookiecutter"],
                    check=True,
                    capture_output=True
                )
            except subprocess.CalledProcessError:
                # Fallback: clonar repositório diretamente
                try:
                    subprocess.run(
                        ["git", "clone", self.framework_repo_url, str(framework_dir)],
                        check=True,
                        capture_output=True
                    )
                    return framework_dir
                except subprocess.CalledProcessError as e:
                    raise RuntimeError(f"Erro ao baixar framework: {e.stderr.decode()}")
        
        # Usar cookiecutter para gerar projeto
        try:
            # Cookiecutter precisa de um template, então vamos clonar primeiro
            template_dir = target_dir / "t2c_template_temp"
            if template_dir.exists():
                shutil.rmtree(template_dir)
            
            subprocess.run(
                ["git", "clone", self.framework_repo_url, str(template_dir)],
                check=True,
                capture_output=True
            )
            
            # Executar cookiecutter
            # Cookiecutter espera respostas interativas, então vamos usar variáveis de ambiente
            import os
            env = os.environ.copy()
            env['COOKIECUTTER_REPLAY'] = 'false'
            
            # Criar arquivo de contexto para cookiecutter
            context_file = template_dir / "cookiecutter.json"
            if not context_file.exists():
                # Se não tiver cookiecutter.json, criar um básico
                import json
                context = {
                    "project_name": project_name,
                    "project_slug": project_name.lower().replace(" ", "_").replace("-", "_")
                }
                context_file.write_text(json.dumps(context, indent=2), encoding="utf-8")
            
            # Executar cookiecutter
            subprocess.run(
                ["cookiecutter", str(template_dir), "--no-input", f"project_name={project_name}"],
                cwd=str(target_dir),
                check=True,
                capture_output=True
            )
            
            # O cookiecutter cria o diretório com o nome do projeto
            framework_dir = target_dir / project_name
            if not framework_dir.exists():
                # Se cookiecutter não funcionou, usar o template clonado
                framework_dir = template_dir
            
        except subprocess.CalledProcessError as e:
            # Fallback: usar template clonado diretamente
            if template_dir.exists():
                framework_dir = template_dir
            else:
                raise RuntimeError(f"Erro ao gerar framework com cookiecutter: {e.stderr.decode()}")
        
        return framework_dir
    
    def generate_project_structure(self, project_name: str, output_dir: Path):
        """
        Cria estrutura de diretórios do projeto
        
        Args:
            project_name: Nome do projeto
            output_dir: Diretório de saída
        """
        self.project_name = project_name
        self.generated_dir = output_dir / project_name
        
        if self.generated_dir.exists():
            shutil.rmtree(self.generated_dir)
        
        # Estrutura de diretórios
        directories = [
            f"{project_name}/__init__.py",
            f"{project_name}/__main__.py",
            f"{project_name}/classes_t2c/__init__.py",
            f"{project_name}/classes_t2c/framework",
            f"{project_name}/classes_t2c/queue",
            f"{project_name}/classes_t2c/dados_execucao",
            f"{project_name}/classes_t2c/relatorios",
            f"{project_name}/classes_t2c/email/send",
            f"{project_name}/classes_t2c/utils",
            f"{project_name}/resources/config",
            f"{project_name}/resources/sqlite",
            f"{project_name}/resources/templates",
            f"{project_name}/resources/scripts/analitico_sintetico",
        ]
        
        for directory in directories:
            path = self.generated_dir / directory
            if directory.endswith('.py'):
                path.parent.mkdir(parents=True, exist_ok=True)
            else:
                path.mkdir(parents=True, exist_ok=True)
    
    def copy_framework_files(self, framework_dir: Path):
        """
        Copia arquivos do framework base
        
        Args:
            framework_dir: Diretório do framework baixado
        """
        # Arquivos a copiar (não customizados)
        files_to_copy = [
            "classes_t2c/framework/T2CLoopStation.py",
            "classes_t2c/framework/T2CInitialization.py",
            "classes_t2c/framework/T2CEndProcess.py",
            "classes_t2c/framework/T2CInitAllSettings.py",
            "classes_t2c/framework/T2CGetTransaction.py",
            "classes_t2c/framework/T2CKillAllProcesses.py",
            "classes_t2c/queue/T2CQueueManager.py",
            "classes_t2c/dados_execucao/T2CDadosExecucao.py",
            "classes_t2c/relatorios/T2CRelatorios.py",
            "classes_t2c/email/send/T2CSendEmail.py",
            "classes_t2c/utils/T2CMaestro.py",
            "classes_t2c/utils/T2CTracker.py",
            "classes_t2c/utils/T2CExceptions.py",
            "classes_t2c/utils/T2CGenericReusable.py",
            "classes_t2c/utils/T2CBackupSqlite.py",
            "classes_t2c/utils/T2CRobotStream.py",
            "classes_t2c/utils/T2CScreenRecorder.py",
        ]
        
        # Copiar arquivos
        for file_path in files_to_copy:
            src = framework_dir / file_path
            dst = self.generated_dir / self.project_name / file_path
            
            if src.exists():
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
            else:
                # Se não encontrar no framework, criar arquivo vazio com aviso
                dst.parent.mkdir(parents=True, exist_ok=True)
                dst.write_text(f"# Arquivo do framework T2C\n# TODO: Copiar de {file_path}\n", encoding="utf-8")
    
    def generate_custom_files(self, templates_dir: Path):
        """
        Gera arquivos customizados
        
        Args:
            templates_dir: Diretório com templates
        """
        # Ler templates
        bot_template = (templates_dir / "bot.py.template").read_text(encoding="utf-8")
        process_template = (templates_dir / "t2c_process.py.template").read_text(encoding="utf-8")
        init_template = (templates_dir / "t2c_init_apps.py.template").read_text(encoding="utf-8")
        close_template = (templates_dir / "t2c_close_apps.py.template").read_text(encoding="utf-8")
        
        # Gerar código baseado nas specs
        imports = self._generate_imports()
        validacoes = self._generate_validacoes()
        condicoes = self._generate_condicoes()
        processamento = self._generate_processamento()
        preenchimento_fila = self._generate_preenchimento_fila()
        inicializacao = self._generate_inicializacao()
        fechamento = self._generate_fechamento()
        
        # Substituir variáveis
        bot_content = bot_template.replace("{{PROJECT_NAME}}", self.project_name)
        process_content = process_template.replace("{{PROJECT_NAME}}", self.project_name)
        process_content = process_content.replace("{{IMPORTS}}", imports)
        process_content = process_content.replace("{{VALIDACOES_ENTRADA}}", validacoes)
        process_content = process_content.replace("{{CONDICOES_ESPECIAIS}}", condicoes)
        process_content = process_content.replace("{{PROCESSAMENTO_PRINCIPAL}}", processamento)
        
        init_content = init_template.replace("{{PROJECT_NAME}}", self.project_name)
        init_content = init_content.replace("{{IMPORTS}}", imports)
        init_content = init_content.replace("{{PREENCHIMENTO_FILA}}", preenchimento_fila)
        init_content = init_content.replace("{{INICIALIZACAO_APLICACOES}}", inicializacao)
        
        close_content = close_template.replace("{{PROJECT_NAME}}", self.project_name)
        close_content = close_content.replace("{{IMPORTS}}", imports)
        close_content = close_content.replace("{{FECHAMENTO_APLICACOES}}", fechamento)
        
        # Salvar arquivos
        (self.generated_dir / self.project_name / "bot.py").write_text(bot_content, encoding="utf-8")
        (self.generated_dir / self.project_name / "classes_t2c" / "framework" / "T2CProcess.py").write_text(process_content, encoding="utf-8")
        (self.generated_dir / self.project_name / "classes_t2c" / "framework" / "T2CInitAllApplications.py").write_text(init_content, encoding="utf-8")
        (self.generated_dir / self.project_name / "classes_t2c" / "framework" / "T2CCloseAllApplications.py").write_text(close_content, encoding="utf-8")
        
        # Gerar __init__.py
        init_py_content = f"# {self.project_name} - Framework T2C\n# Versão: 2.2.3\n\n"
        (self.generated_dir / self.project_name / "__init__.py").write_text(init_py_content, encoding="utf-8")
        (self.generated_dir / self.project_name / "classes_t2c" / "__init__.py").write_text(init_py_content, encoding="utf-8")
    
    def _generate_imports(self) -> str:
        """Gera imports baseado nas specs"""
        imports = []
        
        # Verificar se usa Clicknium
        if 'selectors' in self.specs and 'clicknium' in self.specs['selectors'].lower():
            imports.append("from clicknium import clicknium as cc, locator")
        
        # Verificar se usa pandas
        if 'plan' in self.specs and 'pandas' in self.specs['plan'].lower():
            imports.append("import pandas as pd")
        
        # Verificar se usa time
        imports.append("from time import sleep")
        
        # Verificar se usa Browser
        if 'plan' in self.specs and ('navegador' in self.specs['plan'].lower() or 'browser' in self.specs['plan'].lower()):
            imports.append("from botcity.web import Browser")
        
        return '\n'.join(imports) if imports else "# Nenhum import adicional necessário"
    
    def _generate_validacoes(self) -> str:
        """Gera código de validações baseado em business-rules.md"""
        if 'business_rules' not in self.specs:
            return "# Nenhuma validação definida"
        
        validacoes = []
        rules_text = self.specs['business_rules']
        
        # Procurar por VAL*
        val_pattern = r'###\s*VAL\d+[:\s]+([^\n]+)'
        matches = re.findall(val_pattern, rules_text, re.IGNORECASE)
        
        for i, match in enumerate(matches[:10], 1):
            validacoes.append(f"        # VAL{i:03d}: {match.strip()}")
            validacoes.append(f"        # TODO: Implementar validação")
            validacoes.append("")
        
        if not validacoes:
            return "# Nenhuma validação definida"
        
        return '\n'.join(validacoes)
    
    def _generate_condicoes(self) -> str:
        """Gera código de condições especiais"""
        if 'business_rules' not in self.specs:
            return "# Nenhuma condição especial definida"
        
        condicoes = []
        rules_text = self.specs['business_rules']
        
        # Procurar por COND*
        cond_pattern = r'###\s*COND\d+[:\s]+([^\n]+)'
        matches = re.findall(cond_pattern, rules_text, re.IGNORECASE)
        
        for i, match in enumerate(matches[:10], 1):
            condicoes.append(f"        # COND{i:03d}: {match.strip()}")
            condicoes.append(f"        # TODO: Implementar condição")
            condicoes.append("")
        
        if not condicoes:
            return "# Nenhuma condição especial definida"
        
        return '\n'.join(condicoes)
    
    def _generate_processamento(self) -> str:
        """Gera código de processamento principal"""
        if 'tasks' not in self.specs:
            return "# TODO: Implementar processamento principal"
        
        processamento = []
        tasks_text = self.specs['tasks']
        
        # Procurar por tasks da fase Process
        process_pattern = r'###\s*Task\s+2\.\d+[:\s]+([^\n]+)'
        matches = re.findall(process_pattern, tasks_text, re.IGNORECASE)
        
        for i, match in enumerate(matches, 1):
            processamento.append(f"        # Task 2.{i}: {match.strip()}")
            processamento.append(f"        # TODO: Implementar")
            processamento.append("")
        
        if not processamento:
            return "# TODO: Implementar processamento principal"
        
        return '\n'.join(processamento)
    
    def _generate_preenchimento_fila(self) -> str:
        """Gera código para preencher fila"""
        if 'tasks' not in self.specs:
            return "# TODO: Implementar preenchimento da fila"
        
        tasks_text = self.specs['tasks']
        
        # Procurar por Task 1.2 (add_to_queue)
        if 'Task 1.2' in tasks_text or 'add_to_queue' in tasks_text.lower():
            return """        # TODO: Implementar lógica para preencher fila
        # Exemplo:
        # import pandas as pd
        # df = pd.read_excel('dados.xlsx')
        # for index, row in df.iterrows():
        #     var_dictInfoAdicional = {'campo1': row['campo1']}
        #     QueueManager.insert_new_queue_item(
        #         arg_strReferencia=str(row['id']),
        #         arg_dictInfAdicional=var_dictInfoAdicional
        #     )"""
        
        return "# TODO: Implementar preenchimento da fila"
    
    def _generate_inicializacao(self) -> str:
        """Gera código de inicialização"""
        if 'tasks' not in self.specs:
            return "# TODO: Implementar inicialização de aplicações"
        
        tasks_text = self.specs['tasks']
        
        # Verificar se menciona navegador
        if 'navegador' in tasks_text.lower() or 'browser' in tasks_text.lower():
            return """            # Inicializar navegador
            InitAllSettings.initiate_web_manipulator(
                arg_boolHeadless=False,
                arg_brwBrowserEscolhido=Browser.CHROME,
                arg_strPastaDownload=r"C:\\Downloads"
            )
            
            # Navegar para página inicial
            # InitAllSettings.var_botWebbot.navigate_to("https://exemplo.com")"""
        
        return "# TODO: Implementar inicialização de aplicações"
    
    def _generate_fechamento(self) -> str:
        """Gera código de fechamento"""
        return """            # Fechar navegador
            if InitAllSettings.var_botWebbot is not None:
                InitAllSettings.var_botWebbot.stop_browser()
            
            # Fechar outras aplicações se necessário
            # subprocess.run(['taskkill', '/F', '/IM', 'aplicacao.exe'])"""
    
    def generate_config_xlsx(self):
        """Gera Config.xlsx baseado em config/*.md"""
        # TODO: Implementar geração de Excel
        # Por enquanto, criar arquivo placeholder
        config_path = self.generated_dir / self.project_name / "resources" / "config" / "Config.xlsx"
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text("# TODO: Gerar Config.xlsx baseado em config/*.md\n", encoding="utf-8")
    
    def generate_requirements_txt(self, templates_dir: Path):
        """Gera requirements.txt"""
        template = (templates_dir / "requirements.txt.template").read_text(encoding="utf-8")
        (self.generated_dir / "requirements.txt").write_text(template, encoding="utf-8")
    
    def generate_setup_py(self, templates_dir: Path):
        """Gera setup.py"""
        template = (templates_dir / "setup.py.template").read_text(encoding="utf-8")
        content = template.replace("{{PROJECT_NAME}}", self.project_name)
        content = content.replace("{{PROJECT_DESCRIPTION}}", f"Automação RPA - {self.project_name}")
        (self.generated_dir / "setup.py").write_text(content, encoding="utf-8")
    
    def generate_readme(self, templates_dir: Path):
        """Gera README.md"""
        template = (templates_dir / "readme.md.template").read_text(encoding="utf-8")
        content = template.replace("{{PROJECT_NAME}}", self.project_name)
        content = content.replace("{{PROJECT_DESCRIPTION}}", f"Automação RPA gerada com RPA Spec-Kit")
        (self.generated_dir / "README.md").write_text(content, encoding="utf-8")
    
    def generate(self, output_dir: Path, skip_download: bool = False):
        """
        Gera framework completo
        
        Args:
            output_dir: Diretório de saída
            skip_download: Se True, não baixa framework (usa estrutura local)
        """
        # Ler specs
        self.read_specs()
        
        # Validar
        errors = self.validate_specs()
        if errors:
            raise ValueError(f"Erros de validação: {', '.join(errors)}")
        
        # Determinar nome do projeto
        project_name = self.determine_project_name()
        
        # Criar estrutura
        self.generate_project_structure(project_name, output_dir)
        
        # Baixar framework (se necessário)
        if not skip_download:
            temp_dir = output_dir / "temp"
            temp_dir.mkdir(exist_ok=True)
            framework_dir = self.download_framework(temp_dir, project_name)
        else:
            framework_dir = None
        
        # Copiar arquivos do framework
        if framework_dir:
            self.copy_framework_files(framework_dir)
        
        # Gerar arquivos customizados
        templates_dir = Path(__file__).parent.parent / "templates" / "code"
        self.generate_custom_files(templates_dir)
        
        # Gerar Config.xlsx
        self.generate_config_xlsx()
        
        # Gerar arquivos de projeto
        self.generate_requirements_txt(templates_dir)
        self.generate_setup_py(templates_dir)
        self.generate_readme(templates_dir)
        
        return self.generated_dir

