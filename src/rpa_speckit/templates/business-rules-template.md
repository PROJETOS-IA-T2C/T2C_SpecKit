# Exceções de Negócio

> **⚠️ IMPORTANTE:** Ao criar o arquivo final, replique apenas a estrutura do template. Remova anotações de ajuda.

## Lista de Exceções (BusinessRuleException)

> **Regra:** Estas exceções DEVEM ser tratadas com `raise BusinessRuleException("Mensagem")`. O framework não fará retentativa automática.

### EXC001: [Nome Curto da Exceção]
- **Descrição:** [Descrição detalhada do erro de negócio]
- **Condição:** [Lógica que dispara o erro. Ex: "Se CPF não existir na base"]
- **Ação:** [Logar erro e marcar item como Business Error]

### EXC002: [Nome Curto da Exceção]
- **Descrição:** [Descrição detalhada]
- **Condição:** [Lógica que dispara o erro]
- **Ação:** [Logar erro e marcar item como Business Error]
