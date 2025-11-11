# T2C SpecKit

Toolkit completo para Spec-Driven Development de RPA com Framework T2C.

## 📋 Sobre

O T2C SpecKit é uma ferramenta que permite criar projetos de automação RPA seguindo o padrão Spec-Driven Development, com integração completa ao Framework T2C. Similar ao GitHub Spec-Kit, mas adaptado especificamente para automações RPA.

## 🚀 Instalação

### Via uvx (Recomendado)

```bash
uvx --from git+https://github.com/PROJETOS-IA-T2C/T2C_SpecKit.git t2c init meu-projeto
```

### Via pip

```bash
pip install t2c-speckit
```

## 📖 Uso

### 1. Inicializar Projeto

```bash
t2c init meu-projeto
```

Ou via uvx:

```bash
uvx --from git+https://github.com/PROJETOS-IA-T2C/T2C_SpecKit.git t2c init meu-projeto
```

O comando irá:
- Criar estrutura completa do projeto
- Configurar templates e constitution do framework T2C
- Criar comandos Cursor/VS Code conforme escolha (Cursor, VS Code + GitHub Copilot, ou VS Code + Claude)
- Configurar scripts de automação

### 2. Extrair DDP

Coloque o arquivo `DDP.pptx` em `specs/001-[nome]/DDP/` e execute:

**No Cursor:**
```
/t2c.extract-ddp specs/001-[nome]/DDP/ddp.pptx
```

**No VS Code + GitHub Copilot:**
- Use slash command: `/t2c.extract-ddp` ou `/t2c.extract-ddp specs/001-[nome]/DDP/ddp.pptx` (igual ao Cursor!)
- Ou use a task: `Ctrl+Shift+P` > "Tasks: Run Task" > "T2C: Extract DDP"
- Ou execute diretamente: `python .specify/scripts/extract-ddp.py`

O comando irá:
- Extrair informações do PPTX
- Preencher automaticamente: `spec.md` (ARQUIVO PRINCIPAL), `tests.md`, `selectors.md`, `business-rules.md`
- Marcar o que foi preenchido automaticamente vs. o que precisa completar

### 3. Completar Especificações

Revise e complete manualmente os arquivos gerados:
- `spec.md` - Especificação técnica e arquitetura (ARQUIVO PRINCIPAL)
- `tests.md` - Cenários de teste e validações
- `selectors.md` - Seletores Clicknium
- `business-rules.md` - Regras de negócio
- `tasks.md` - Breakdown de tarefas (opcional, pode ser gerado)

### 4. Gerar Tasks (Opcional)

**No Cursor:**
```
/t2c.tasks specs/001-[nome]
```

**No VS Code + GitHub Copilot:**
- Use slash command: `/t2c.tasks specs/001-[nome]` (igual ao Cursor!)

Gera `tasks.md` baseado nas outras especificações.

### 5. Implementar Framework

**No Cursor:**
```
/t2c.implement specs/001-[nome]
```

**No VS Code + GitHub Copilot:**
- Use slash command: `/t2c.implement specs/001-[nome]` (igual ao Cursor!)

O comando irá:
- Validar todas as specs
- Baixar framework T2C do GitHub
- Gerar framework completo em `generated/[nome-automacao]/`
- Criar arquivos customizados baseados nas specs

## 📁 Estrutura do Projeto

```
meu-projeto/
├── .specify/              # Configurações e templates
│   ├── memory/
│   │   └── constitution.md # Constitution do framework T2C
│   └── templates/         # Templates de especificação
├── .cursor/              # Comandos Cursor (se escolhido)
│   └── commands/
│       ├── t2c.extract-ddp.md
│       ├── t2c.tasks.md
│       ├── t2c.implement.md
│       └── t2c.validate.md
├── .vscode/              # Configurações VS Code (se escolhido)
│   ├── commands/         # Comandos slash para GitHub Copilot (igual ao Cursor)
│   │   ├── t2c.extract-ddp.md
│   │   ├── t2c.tasks.md
│   │   ├── t2c.implement.md
│   │   └── t2c.validate.md
│   ├── copilot-instructions.md  # Instruções para slash commands
│   ├── tasks.json        # Tasks para executar scripts
│   ├── settings.json     # Configurações do VS Code
│   └── README.md         # Como usar os comandos
├── specs/                 # Especificações de automações
│   └── 001-[nome]/
│       ├── spec.md     # ARQUIVO PRINCIPAL
│       ├── tests.md
│       ├── selectors.md
│       ├── business-rules.md
│       ├── tasks.md
│       └── DDP/
├── generated/            # Framework T2C gerado
└── DDP/                  # DDPs gerais
```

## 🔧 Comandos Disponíveis

### Cursor

No Cursor, use os comandos slash diretamente:
- `/t2c.extract-ddp [caminho]` - Extrai informações de DDP.pptx
- `/t2c.tasks [caminho]` - Gera tasks.md
- `/t2c.implement [caminho]` - Gera framework T2C completo
- `/t2c.validate [caminho]` - Valida estrutura e completude

### VS Code + GitHub Copilot

No VS Code com GitHub Copilot, use os slash commands **EXATAMENTE como no Cursor**:

- `/t2c.extract-ddp [caminho]` - Extrai informações de DDP.pptx
- `/t2c.tasks [caminho]` - Gera tasks.md
- `/t2c.implement [caminho]` - Gera framework T2C completo
- `/t2c.validate [caminho]` - Valida estrutura e completude

**Experiência idêntica ao Cursor!** O Copilot reconhece os slash commands e lê automaticamente os arquivos em `.vscode/commands/`.

Alternativas:
- **Tasks do VS Code**: `Ctrl+Shift+P` > "Tasks: Run Task" > "T2C: Extract DDP"
- **Executar diretamente**: `python .specify/scripts/extract-ddp.py`

Consulte `.vscode/README.md` para mais detalhes sobre como usar os comandos com GitHub Copilot.

## 🎯 Fluxo de Trabalho Completo

1. **Inicialização**: `t2c init meu-projeto` ou via uvx
2. **Extrair DDP**: Coloque DDP.pptx e execute o comando apropriado:
   - **Cursor**: `/t2c.extract-ddp`
   - **VS Code + Copilot**: `/t2c.extract-ddp` (mesmo comando slash!)
3. **Completar Specs**: Revise e complete os arquivos .md
4. **Gerar Tasks** (Opcional): Execute o comando apropriado:
   - **Cursor**: `/t2c.tasks`
   - **VS Code + Copilot**: `/t2c.tasks` (mesmo comando slash!)
5. **Implementar**: Execute o comando apropriado para gerar framework:
   - **Cursor**: `/t2c.implement`
   - **VS Code + Copilot**: `/t2c.implement` (mesmo comando slash!)
6. **Testar**: Teste o framework gerado em `generated/`

## 🏗️ Framework T2C

O T2C SpecKit gera projetos baseados no Framework T2C versão 2.2.3, que fornece:

- Gerenciamento completo do ciclo de vida (inicialização, processamento, finalização)
- Gerenciamento de fila (SQLite)
- Tratamento de erros (business e system exceptions)
- Geração de relatórios (analítico e sintético)
- Envio de e-mails
- Integração com Maestro (BotCity)
- Logging estruturado

## 📚 Documentação

- [Constitution do Framework T2C](.specify/memory/constitution.md) - Regras e padrões completos
- [Templates](.specify/templates/) - Templates de especificação
- [Framework T2C](https://github.com/T2C-Consultoria/prj_botcity_framework_template.git) - Repositório do framework

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor, leia [CONTRIBUTING.md](CONTRIBUTING.md) para detalhes.

## 📝 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🙏 Agradecimentos

- Framework T2C
- BotCity
- Clicknium

