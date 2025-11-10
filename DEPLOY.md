# Guia de Deploy

## Preparação para Publicação

O projeto está configurado para ser usado via `uvx` a partir do repositório:
**https://github.com/PROJETOS-IA-T2C/T2C_SpecKit.git**

## Configurações Atualizadas

### 1. Nome do Pacote
- **Nome:** `t2c-speckit`
- **Comando CLI:** `t2c` (principal) e `t2c-speckit` (alternativo)

### 2. Repositório do Framework T2C
- **URL:** https://github.com/T2C-Consultoria/prj_botcity_framework_template.git
- **Método:** Usa cookiecutter para gerar projetos

### 3. Dependências
- `click>=8.0.0`
- `rich>=13.0.0`
- `pyyaml>=6.0`
- `python-pptx>=0.6.21`
- `cookiecutter>=2.1.0` (novo)

## Como Usar Após Deploy

### Via uvx (Recomendado)

```bash
uvx --from git+https://github.com/PROJETOS-IA-T2C/T2C_SpecKit.git t2c init meu-projeto
```

### Via pip

```bash
pip install git+https://github.com/PROJETOS-IA-T2C/T2C_SpecKit.git
t2c init meu-projeto
```

## Comandos Disponíveis

Todos os comandos agora usam o prefixo `t2c`:

- `/t2c.extract-ddp` - Extrai informações de DDP.pptx
- `/t2c.tasks` - Gera tasks.md
- `/t2c.implement` - Gera framework T2C completo
- `/t2c.validate` - Valida estrutura e completude

## Notas Importantes

1. O framework T2C usa **cookiecutter** para gerar projetos
2. O gerador tenta instalar cookiecutter automaticamente se não estiver instalado
3. Se cookiecutter falhar, o sistema faz fallback para git clone direto
4. Todos os comandos Cursor foram atualizados para usar `t2c.` ao invés de `rpa.`

## Checklist Antes de Fazer Push

- [x] Nome do pacote atualizado para `t2c-speckit`
- [x] Comando CLI atualizado para `t2c`
- [x] URL do framework T2C atualizada
- [x] Cookiecutter adicionado às dependências
- [x] Comandos Cursor atualizados para `t2c.`
- [x] README atualizado com URLs corretas
- [x] Banner atualizado para "T2C SpecKit"

