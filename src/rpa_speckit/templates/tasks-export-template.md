# Exportar Tasks para Excel

Gera uma planilha de estimativa preenchida com base no tasks.md.

## Uso

\`\`\`
/t2c.export-tasks [caminho_tasks]
\`\`\`

## Exemplo

\`\`\`
/t2c.export-tasks specs/001-exemplo/tasks.md
\`\`\`

## O que faz

1. Lê o arquivo `tasks.md` do projeto
2. Extrai as tarefas, robôs e estimativas
3. Executa o script Python `.specify/scripts/excel_exporter.py` para preencher o template Excel

## Instruções para a LLM

1. **Localizar Arquivos:**
   - Tasks: O arquivo passado como argumento (ou procurar `tasks.md` nas specs)
   - Script: `.specify/scripts/excel_exporter.py`
   - Template: Procurar por arquivos `.xlsx` na raiz ou em `.specify/templates/` (ex: `Estimativa de Esforco - Template.xlsx`)

2. **Extração:**
   - Ler `tasks.md` e montar a estrutura de dados JSON com:
     - `process_name`: Nome do processo (do cabeçalho ou nome da pasta)
     - `template`: Caminho do template encontrado
     - `output`: `Estimativa_[NomeProcesso].xlsx` (na raiz)
     - `tasks`: Lista de objetos {robot, name, description, estimate}

3. **Execução:**
   - Executar o script Python passando o JSON como argumento.
   - **NÃO** tente recriar a lógica Python. Use o script existente.
   - **Comando:** `python .specify/scripts/excel_exporter.py '{"json_data"}'`

