# Plano de Testes (Test Plan)

> **⚠️ IMPORTANTE:** Ao criar o arquivo final, replique apenas a estrutura do template. Remova anotações de ajuda.

## Cenários de Teste (Input -> Output)

### Cenário 1: [Caminho Feliz - Padrão]
- **Pré-condição:** [Estado do sistema/dados antes do teste. Ex: "Fila com item válido"]
- **Ação:** [O que o robô fará]
- **Resultado Esperado:** [O que deve acontecer. Ex: "Item processado com sucesso, status SUCESSO"]

### Cenário 2: [Exceção de Negócio - EXC001]
- **Pré-condição:** [Dados inválidos específicos. Ex: "Item com CPF inválido"]
- **Ação:** [Robô tenta processar]
- **Resultado Esperado:** [Item marcado como BUSINESS ERROR com mensagem correta]

### Cenário 3: [Exceção de Sistema]
- **Pré-condição:** [Sistema offline ou tela alterada]
- **Ação:** [Robô tenta processar]
- **Resultado Esperado:** [Item retentado 3 vezes e marcado como APP ERROR]

## Massa de Teste Sugerida

| Campo | Cenário 1 (Sucesso) | Cenário 2 (Erro Negócio) |
|-------|---------------------|--------------------------|
| CPF | 123.456.789-00 | 000.000.000-00 |
| Valor | 100.00 | -50.00 |
