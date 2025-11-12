# Exceções de Negócio

> **⚠️ IMPORTANTE:** Ao criar o arquivo final, replique apenas a estrutura do template. Remova todas as anotações, exemplos e informações que não sejam do processo real. Mantenha apenas as informações reais do processo para reduzir a quantidade de informação no documento.

> **Nota:** As Business Exceptions listadas abaixo são mapeadas no DDP (Documento de Definição de Processo) e devem ser organizadas neste documento. Se durante a análise você identificar uma possível exceção de negócio que não foi mapeada no DDP, adicione-a na seção "Exceções Não Mapeadas" no final deste documento.

## Business Exceptions

As exceções de negócio são situações mapeadas no processo que podem ocorrer durante a execução e precisam ser tratadas adequadamente. Estas exceções devem ser lançadas como `BusinessRuleException` para indicar que o erro é de negócio e não deve ser retentado automaticamente pelo framework.

### EXC001: [Nome da Exceção]
- **Descrição:** [Descrição completa da exceção]
- **Condição:** [Quando esta exceção pode ocorrer]
- **Ação em Erro:** [O que fazer quando esta exceção ocorrer]
- **Exceção:** BusinessRuleException

### EXC002: [Nome da Exceção]
- **Descrição:** [Descrição completa da exceção]
- **Condição:** [Quando esta exceção pode ocorrer]
- **Ação em Erro:** [O que fazer quando esta exceção ocorrer]
- **Exceção:** BusinessRuleException

---

## Exceções Não Mapeadas

Esta seção deve conter exceções de negócio identificadas durante a análise que não foram mapeadas no DDP original. Essas exceções devem ser documentadas para possível inclusão futura no DDP.

### EXC_UNMAPPED001: [Nome da Exceção Identificada]
- **Descrição:** [Descrição completa da exceção identificada]
- **Condição:** [Quando esta exceção pode ocorrer]
- **Ação em Erro:** [O que fazer quando esta exceção ocorrer]
- **Observação:** Exceção identificada durante a análise, não mapeada no DDP original

### EXC_UNMAPPED002: [Nome da Exceção Identificada]
- **Descrição:** [Descrição completa da exceção identificada]
- **Condição:** [Quando esta exceção pode ocorrer]
- **Ação em Erro:** [O que fazer quando esta exceção ocorrer]
- **Observação:** Exceção identificada durante a análise, não mapeada no DDP original
