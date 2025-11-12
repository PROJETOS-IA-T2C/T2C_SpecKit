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
try:
    from importlib.resources import files as resource_files
except ImportError:
    # Python < 3.9 fallback
    from importlib_resources import files as resource_files


class T2CFrameworkGenerator:
    """Classe para gerar framework T2C completo"""
    
    def __init__(self, spec_dir: str, framework_repo_url: Optional[str] = None, robot_name: Optional[str] = None):
        """
        Inicializa o gerador
        
        Args:
            spec_dir: Diretório com as specs (specs/001-[nome]/)
            framework_repo_url: URL do repositório do framework T2C (opcional)
            robot_name: Nome do robô específico para gerar (opcional, ex: 'robot1', 'robot2')
        """
        self.spec_dir = Path(spec_dir)
        self.framework_repo_url = framework_repo_url or "https://github.com/T2C-Consultoria/prj_botcity_framework_template.git"
        self.specs: Dict = {}
        self.project_name: str = ""
        self.generated_dir: Path = None
        self.robot_name: Optional[str] = robot_name
        self.is_multi_robot: bool = False
        self.robot_list: List[str] = []
    
    def detect_structure(self) -> bool:
        """
        Detecta se a estrutura é standalone ou múltiplos robôs
        
        Returns:
            True se múltiplos robôs, False se standalone
        """
        # Verificar se existe robot1/ (indica múltiplos robôs)
        robot1_dir = self.spec_dir / "robot1"
        if robot1_dir.exists() and robot1_dir.is_dir():
            self.is_multi_robot = True
            # Listar todos os robôs
            for item in self.spec_dir.iterdir():
                if item.is_dir() and item.name.startswith("robot") and item.name[5:].isdigit():
                    self.robot_list.append(item.name)
            self.robot_list.sort(key=lambda x: int(x[5:]) if x[5:].isdigit() else 0)
            return True
        
        # Se não tem robot1/, é standalone
        self.is_multi_robot = False
        self.robot_list = []
        return False
    
    def read_specs(self, robot_dir: Optional[Path] = None) -> Dict:
        """
        Lê todos os arquivos .md preenchidos
        
        Args:
            robot_dir: Diretório do robô específico (None para standalone ou raiz)
        
        Returns:
            Dicionário com todas as specs
        """
        # Determinar diretório base
        base_dir = robot_dir if robot_dir else self.spec_dir
        
        required_files = {
            'spec': 'spec.md',  # ARQUIVO PRINCIPAL - Arquitetura completa
            'selectors': 'selectors.md',
            'business_rules': 'business-rules.md',
            'tests': 'tests.md'
        }
        
        specs = {}
        
        for key, filename in required_files.items():
            file_path = base_dir / filename
            if file_path.exists():
                specs[key] = file_path.read_text(encoding="utf-8")
            else:
                raise FileNotFoundError(f"Arquivo obrigatório não encontrado: {file_path}")
        
        # Ler tasks.md da raiz (compartilhado)
        tasks_file = self.spec_dir / 'tasks.md'
        if tasks_file.exists():
            specs['tasks'] = tasks_file.read_text(encoding="utf-8")
        else:
            raise FileNotFoundError(f"Arquivo obrigatório não encontrado: tasks.md")
        
        # Ler configs se existirem
        config_dir = self.spec_dir.parent.parent / "config"
        if config_dir.exists():
            specs['configs'] = {}
            for config_file in config_dir.glob("*.md"):
                specs['configs'][config_file.stem] = config_file.read_text(encoding="utf-8")
        
        return specs
    
    def validate_specs(self, specs: Optional[Dict] = None) -> List[str]:
        """
        Valida completude das specs
        
        Args:
            specs: Dicionário de specs a validar (None para usar self.specs)
        
        Returns:
            Lista de erros encontrados (vazia se tudo OK)
        """
        errors = []
        specs_to_validate = specs if specs is not None else self.specs
        
        # Verificar se arquivos existem
        required_files = ['spec', 'selectors', 'business_rules', 'tests', 'tasks']
        for key in required_files:
            if key not in specs_to_validate:
                errors.append(f"Arquivo {key} não encontrado")
        
        # Verificar se spec não está vazio (ARQUIVO PRINCIPAL)
        if 'spec' in specs_to_validate:
            if len(specs_to_validate['spec'].strip()) < 100:
                errors.append("spec.md (ARQUIVO PRINCIPAL) parece estar vazio ou incompleto")
            # Verificar se spec tem stack definida
            if 'T2C Framework' not in specs_to_validate['spec']:
                errors.append("spec.md (ARQUIVO PRINCIPAL) não menciona T2C Framework")
        
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
    
    def generate_custom_files(self, templates_dir):
        """
        Gera arquivos customizados
        
        Args:
            templates_dir: Diretório com templates (pode ser Path ou Traversable)
        """
        # Helper para ler templates - suporta tanto Path quanto Traversable (importlib.resources)
        def read_template(template_path):
            if hasattr(template_path, 'read_text'):
                return template_path.read_text(encoding="utf-8")
            else:
                return Path(template_path).read_text(encoding="utf-8")
        
        # Ler templates
        bot_template = read_template(templates_dir / "bot.py.template")
        process_template = read_template(templates_dir / "t2c_process.py.template")
        init_template = read_template(templates_dir / "t2c_init_apps.py.template")
        close_template = read_template(templates_dir / "t2c_close_apps.py.template")
        
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
        if 'spec' in self.specs and 'pandas' in self.specs['spec'].lower():
            imports.append("import pandas as pd")
        
        # Verificar se usa time
        imports.append("from time import sleep")
        
        # Verificar se usa Browser
        if 'spec' in self.specs and ('navegador' in self.specs['spec'].lower() or 'browser' in self.specs['spec'].lower()):
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
        def read_template(template_path):
            if hasattr(template_path, 'read_text'):
                return template_path.read_text(encoding="utf-8")
            else:
                return Path(template_path).read_text(encoding="utf-8")
        template = read_template(templates_dir / "requirements.txt.template")
        (self.generated_dir / "requirements.txt").write_text(template, encoding="utf-8")
    
    def generate_setup_py(self, templates_dir: Path):
        """Gera setup.py"""
        def read_template(template_path):
            if hasattr(template_path, 'read_text'):
                return template_path.read_text(encoding="utf-8")
            else:
                return Path(template_path).read_text(encoding="utf-8")
        template = read_template(templates_dir / "setup.py.template")
        content = template.replace("{{PROJECT_NAME}}", self.project_name)
        content = content.replace("{{PROJECT_DESCRIPTION}}", f"Automação RPA - {self.project_name}")
        (self.generated_dir / "setup.py").write_text(content, encoding="utf-8")
    
    def generate_readme(self, templates_dir: Path):
        """Gera README.md"""
        def read_template(template_path):
            if hasattr(template_path, 'read_text'):
                return template_path.read_text(encoding="utf-8")
            else:
                return Path(template_path).read_text(encoding="utf-8")
        template = read_template(templates_dir / "readme.md.template")
        content = template.replace("{{PROJECT_NAME}}", self.project_name)
        content = content.replace("{{PROJECT_DESCRIPTION}}", f"Automação RPA gerada com RPA Spec-Kit")
        (self.generated_dir / "README.md").write_text(content, encoding="utf-8")
    
    def generate_single_robot(self, robot_name: str, output_dir: Path, skip_download: bool = False) -> Path:
        """
        Gera framework para um robô específico
        
        Args:
            robot_name: Nome do robô ('robot1', 'robot2', etc. ou None para standalone)
            output_dir: Diretório de saída
            skip_download: Se True, não baixa framework (usa estrutura local)
        
        Returns:
            Caminho do diretório gerado
        """
        # Determinar diretório do robô
        if robot_name:
            robot_dir = self.spec_dir / robot_name
            if not robot_dir.exists():
                raise FileNotFoundError(f"Diretório do robô não encontrado: {robot_dir}")
        else:
            robot_dir = None  # Standalone
        
        # Ler specs do robô
        specs = self.read_specs(robot_dir)
        self.specs = specs
        
        # Validar
        errors = self.validate_specs(specs)
        if errors:
            raise ValueError(f"Erros de validação para {robot_name or 'standalone'}: {', '.join(errors)}")
        
        # Determinar nome do projeto
        base_project_name = self.determine_project_name()
        
        # Se múltiplos robôs, adicionar sufixo do robô
        if robot_name:
            project_name = f"{base_project_name}-{robot_name}"
        else:
            project_name = base_project_name
        
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
        # Usar importlib.resources para acessar templates do pacote instalado
        try:
            from rpa_speckit import templates
            templates_resource = resource_files(templates) / "code"
            templates_dir = Path(templates_resource)
        except (ImportError, AttributeError):
            # Fallback: tentar caminho relativo (modo desenvolvimento)
            templates_dir = Path(__file__).parent.parent / "templates" / "code"
        
        self.generate_custom_files(templates_dir)
        
        # Gerar Config.xlsx
        self.generate_config_xlsx()
        
        # Gerar arquivos de projeto
        self.generate_requirements_txt(templates_dir)
        self.generate_setup_py(templates_dir)
        self.generate_readme(templates_dir)
        
        return self.generated_dir
    
    def generate(self, output_dir: Path, skip_download: bool = False):
        """
        Gera framework completo (standalone ou múltiplos robôs)
        
        Args:
            output_dir: Diretório de saída
            skip_download: Se True, não baixa framework (usa estrutura local)
        
        Returns:
            Lista de caminhos dos diretórios gerados (ou caminho único se standalone)
        """
        # Detectar estrutura
        is_multi = self.detect_structure()
        
        generated_dirs = []
        
        if is_multi:
            # Múltiplos robôs
            robots_to_generate = self.robot_list
            
            # Se robot_name foi especificado, gerar apenas esse
            if self.robot_name:
                if self.robot_name not in robots_to_generate:
                    raise ValueError(f"Robô '{self.robot_name}' não encontrado. Robôs disponíveis: {', '.join(robots_to_generate)}")
                robots_to_generate = [self.robot_name]
            
            # Gerar cada robô
            for robot_name in robots_to_generate:
                generated_dir = self.generate_single_robot(robot_name, output_dir, skip_download)
                generated_dirs.append(generated_dir)
        else:
            # Standalone
            generated_dir = self.generate_single_robot(None, output_dir, skip_download)
            generated_dirs.append(generated_dir)
        
        # Retornar lista ou único caminho
        if len(generated_dirs) == 1:
            return generated_dirs[0]
        return generated_dirs

