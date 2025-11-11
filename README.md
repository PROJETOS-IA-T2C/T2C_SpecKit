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
- Criar comandos Cursor/VS Code conforme escolha
- Configurar scripts de automação

### 2. Extrair DDP

Coloque o arquivo `DDP.pptx` em `specs/001-[nome]/DDP/` e execute:

```
/t2c.extract-ddp specs/001-[nome]/DDP/ddp.pptx
```

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

```
/t2c.tasks specs/001-[nome]
```

Gera `tasks.md` baseado nas outras especificações.

### 5. Implementar Framework

```
/t2c.implement specs/001-[nome]
```

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

### Cursor/VS Code

- `/t2c.extract-ddp [caminho]` - Extrai informações de DDP.pptx
- `/t2c.tasks [caminho]` - Gera tasks.md
- `/t2c.implement [caminho]` - Gera framework T2C completo
- `/t2c.validate [caminho]` - Valida estrutura e completude

## 🎯 Fluxo de Trabalho Completo

1. **Inicialização**: `t2c init meu-projeto` ou via uvx
2. **Extrair DDP**: Coloque DDP.pptx e execute `/t2c.extract-ddp`
3. **Completar Specs**: Revise e complete os arquivos .md
4. **Gerar Tasks** (Opcional): Execute `/t2c.tasks`
5. **Implementar**: Execute `/t2c.implement` para gerar framework
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

