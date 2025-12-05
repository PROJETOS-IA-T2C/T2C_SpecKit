# Seletores Clicknium

> **⚠️ IMPORTANTE:** Ao criar o arquivo final, replique apenas a estrutura do template. Remova anotações de ajuda.

## Estrutura de Locators (Store)

> **Regra:** Use `{{parametro}}` para seletores dinâmicos. Ex: `locator.notepad.menu_item` com propriedade `name='{{nome_menu}}'`.

### Pasta: [nome_pasta]

#### [nome_elemento]
- **Tipo:** [button/input/div/etc]
- **Seletor:** [descrição ou atributos principais]
- **Dinâmico:** [SIM/NÃO] (Se SIM, listar parâmetros: `{{param1}}`)
- **Uso:** [onde é usado no código]

#### [nome_elemento2]
- **Tipo:** [button/input/div/etc]
- **Seletor:** [descrição]
- **Dinâmico:** NÃO
- **Uso:** [onde é usado]
