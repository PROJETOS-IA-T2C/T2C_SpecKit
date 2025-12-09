# Guia Mestre de Arquitetura e Estimativa para Automações RPA

Este documento é a fonte canônica da verdade para o design, desenvolvimento e estimativa de todos os projetos de Automação Robótica de Processos (RPA) utilizando o Framework T2C. Seu propósito é estabelecer um framework rigoroso que garanta que cada automação seja Robusta, Escalável, Manutenível e Previsível.

---

## 1. Introdução e Filosofia

Este não é mais um guia; é a **Bíblia da Arquitetura de Automação**. Ele foi projetado para ser o único documento de referência necessário para qualquer pessoa (ou IA) projetar, nomear, estimar e implementar um projeto de RPA.

A filosofia central é a **decomposição inteligente**: processos de negócio complexos são quebrados em robôs especialistas, e robôs são quebrados em tarefas funcionais claras. Esta granularidade é a base para a resiliência e a previsibilidade.

### 1.1 Diretriz de Comunicação (Simplicidade e Clareza)
Ao documentar, explicar ou definir processos para stakeholders, **elimine o "techinês"**.
*   ❌ **Evite:** "O robô consome o payload da fila e processa o milestone."
*   ✅ **Prefira:** "O robô lê os dados do pedido e atualiza o status da etapa."
*   **Regra:** A documentação deve ser direta, profissional e compreensível para uma pessoa de negócios não técnica. Evite metáforas infantis ou termos excessivamente técnicos em inglês no meio de frases em português.

---

## 2. Taxonomia dos Robôs (Definições Oficiais)

Antes de desenhar qualquer solução, é obrigatório classificar cada robô em um dos tipos abaixo.

### 2.1 Robô Dispatcher
*   **Função:** Popular filas de trabalho ou atualizar a base de dados para um standalone.
*   **Comportamento:** Linear (Executa uma vez do início ao fim).
*   **Quando usar:** Quando há uma fonte de dados em massa (Excel, E-mail, Banco, API List) que precisa ser iterada para criar itens transacionais para próximos robôs, ou atualizar estruturas de dados para consumo em um robô standalone.
*   **Características:**
    *   Pode conter regras complexas de extração, filtragem ou transformação de dados antes de popular a fila.
    *   Pode interagir com sistemas externos (APIs, bancos de dados, planilhas, etc.) conforme necessário para preparar o trabalho, desde que o foco seja sempre alimentar a fila ou preparar a base de dados, e não o processamento de negócio final.
    *   O objetivo primário é organizar, disponibilizar e garantir o input adequado para a etapa seguinte da automação, de maneira eficiente, previsível e reentrante.

### 2.2 Robô Performer 
*   **Função:** Consumir itens de uma fila e executar a lógica de negócio.
*   **Comportamento:** Cíclico/Transacional (Obter Item -> Processar -> Definir Status).
*   **Características:** 
    *   Sempre trabalha sobre uma fila (ou seja, recebe input padronizado e preparado, normalmente por um Dispatcher ou Standalone).
    *   Ideal para processamento pesado, execução de regras de negócio complexas e interação direta com sistemas finais.
    *   Cego para o mundo exterior (não monitora pastas/emails), apenas vê o item da fila.
    *   **Regra de Ouro:** Deve ser sempre **Queue-Driven**.

### 2.3 Robô Standalone
*   **Função:** Possui as mesmas características do Performer, mas nesse caso o próprio robô cria e consome sua própria fila (internamente), geralmente em execuções mais simples, rápidas e diretas.
*   **Comportamento:** Cíclico/Transacional (Obter Item -> Processar -> Definir Status).
*   **Quando usar:**
    *   Sempre que o input é simples ou facilmente acessível, evitando a necessidade de criar um Dispatcher separado (ex: ler um Excel local e processar as linhas).
    *   Etapas intermediárias ou de passagem rápida (ex: ler status no Notion e enviar e-mail).
*   **Vantagem:** Reduz a complexidade de arquitetura para processos menores, sem perda das garantias de robustez do padrão Performer.

### 2.4 O Par Assíncrono (Sender & Receiver) - **MANDATÓRIO PARA VERIFAI**
Padrão exclusivo para processamento de documentos com o Verifai (ou ferramentas de OCR assíncronas). **Este padrão pode ser repetido múltiplas vezes dentro de um mesmo macro-processo (ex: Extração Inicial -> Cotação -> Validação Final).**

#### A. Robô Sender (O Iniciador)
*   **Responsabilidade:** Preparar docs, enviar para o verifai e capturar o `Job_ID`.
*   **Output:** Cria um item na fila do robô receiver com o `Job_ID`.
*   **Regra:** Após despachar o ID para a fila, o robô **DEVE ENCERRAR**. Não espera o resultado e também não faz nenhuma outra atividade relacionada ao processo.

#### B. Robô Receiver (O Coletor)
*   **Responsabilidade:** Processar o resultado já pronto no Verifai, utilizando o `Job_ID`.
*   **Ação:** Captura o resultado do processamento do documento no Verifai e continua o processo com as regras de negócio.

### 2.5 O Padrão Pipeline (Daisy-Chain)
Uma variação permitida onde o output de um robô serve imediatamente como input para a fila do próximo, sem depender exclusivamente de agendamentos baseados em varredura de banco de dados.

*   **Hibridismo:** Um robô pode atuar como *Performer* da Etapa A e *Dispatcher* da Etapa B simultaneamente.
*   **Regra:** Ao finalizar sua tarefa com sucesso, o robô monta o payload e cria o item na fila do próximo robô especialista.
*   **Vantagem:** Reduz latência entre etapas e isola falhas de componentes específicos (ex: OCR, API externa).

---

## 3. Princípios de Design de Arquitetura

### 3.1 O Princípio da Responsabilidade Única (Isolamento de Loop)
**Regra:** Um robô deve ter apenas UM loop principal de processamento.

*   **Cenário Proibido:** Entrar em um site, iterar sobre uma lista de Clientes (Loop 1) e, para cada cliente, iterar sobre suas Notas Fiscais (Loop 2) para processá-las.
*   **Solução Correta:**
    *   **Robô 1:** Itera Clientes -> Extrai Notas -> Envia para Fila.
    *   **Robô 2:** Consome Fila de Notas -> Processa Nota.
*   **Exceção (Linearidade):** Se o processamento do "filho" é imediato e usa o mesmo contexto de navegação do "pai" sem riscos de quebra, pode-se manter junto (ex: Emitir Boleto A e logo em seguida Boleto B na mesma tela).

### 3.2 O Princípio da Atomicidade de Estado (State-Driven)
Este princípio vale para qualquer processo, independente da duração: o robô nunca deve ser responsável por mais de um estado/etapa do fluxo. Para cada etapa, o robô atua exclusivamente em um único estado. 

*   O estado do processo nunca deve permanecer apenas na "memória" do robô.
*   A responsabilidade de cada robô é mover o item de um Estado A para um Estado B, sem sobrepor etapas.
    *   *Ex:* De "Novo" para "Aguardando Cotação".
    *   *Ex:* De "Cotação Recebida" para "Aprovado".

### 3.3 Separação de Ingestão e Processamento (I/O vs CPU)
Sempre que uma etapa envolver monitoramento ativo de uma fonte instável (E-mail, Pasta de Rede, Web Scraping lento) seguida de um processamento pesado ou custoso (IA, Verifai, Regras complexas), recomenda-se separar em dois robôs:
1.  **Robô Coletor:** Apenas baixa, salva e enfileira. (Rápido, baixo risco de erro de negócio).
2.  **Robô Processador:** Consome a fila e executa a regra. (Isolado da instabilidade da fonte).


## 4. Componentes Técnicos

### 4.1 Filas (Queues)
*   **Obrigatório:** Schema definido (payload JSON).
*   **Contrato:** Produtor e Consumidor devem concordar estritamente com os campos (ex: `caminho_arquivo`, `id_transacao`, `prioridade`).

### 4.2 Anatomia da Execução (REFramework Simplificado)
1.  **Init:** Config, Login, Kill Process. Falha aqui aborta tudo.
2.  **Main Loop:**
    *   `Get Transaction Item`
    *   `Process Transaction` (Try/Catch de Negócio vs Sistema)
    *   `Set Transaction Status` (Success, Business Rule Exception, System Exception)
3.  **End Process:** Logout, Close, Relatórios.

---

## 5. Nomenclatura e Padrões (Obrigatório)

A padronização permite que qualquer desenvolvedor (ou IA) entenda o projeto apenas lendo os nomes dos arquivos.

### 5.1 Projetos e Robôs
`prj_<Empresa>_<IDProcesso>_<SubSigla>_<Seq>_<Sistema>`
*   *Ex:* `prj_PlanoEPlano_ID55_GFIP_03_DIGIT`

### 5.2 Filas
`Queue_<IDProcesso>_<SeqConsumidor>_<Descricao>`
*   *Ex:* `Queue_ID55_04_PENDING_GFIP_VERIFY`

### 5.3 Variáveis e Código
*   **Variáveis:** `var_strNome`, `var_intIdade`, `var_dictDados`, `var_listItens`.
*   **Argumentos:** `arg_strCaminho`, `arg_dictConfig`.
*   **Constantes:** `CONS_STR_URL_BASE`.
*   **Classes:** PascalCase (`LeitorExcel`, `T2CProcess`).
*   **Métodos:** snake_case (`ler_planilha`, `processar_item`).

---

## 6. Framework de Estimativa (FEFP)

Use esta tabela para calcular o esforço de desenvolvimento (Horas Sênior).

| Complexidade | Características | Tempo Base (h) |
| :--- | :--- | :--- |
| **Baixa** | Configurações, Leituras simples, 1 sistema. | **2 - 4** |
| **Média** | Lógica padrão, APIs, Web Moderno. | **6 - 12** |
| **Alta** | Regras complexas, UI instável (SAP/Citrix), VerifAI. | **14 - 20** |
| **Muito Alta** | Crítico, Legado pesado, IA complexa. | **22 - 32** |

*   **Micro-Tasks:** Quebre tudo em tarefas de no máximo **4 horas**.

---

## 7. Guia de Construção de Código (IA Instructions)

Ao solicitar código para a IA, o output deve seguir estritamente este formato modular.

### O Que NÃO Fazer
*   ❌ Não gerar `bot.py` inteiro.
*   ❌ Não reescrever `InitAllApplications.py`.

### O Que FAZER (Output Esperado)
Gerar classes especialistas em `classes_t2c/`.

**Exemplo: Classe de Leitura de Excel**
Arquivo: `classes_t2c/excel/excel.py`

```python
import pandas as pd
from src.utils.T2CExceptions import BusinessRuleException

class excel:
    """
    Classe especialista para manipulação do Excel de Input.
    """
    @staticmethod
    def ler_e_validar(arg_strCaminho: str) -> list:
        try:
            var_df = pd.read_excel(arg_strCaminho)
        except Exception as e:
            raise Exception(f"Erro crítico ao abrir Excel: {e}")

        if "CPF" not in var_df.columns:
            raise BusinessRuleException("Coluna obrigatória 'CPF' ausente.")

        return var_df.to_dict('records')
```

---

## 8. Exemplo de Arquitetura Real (Case: Cotação de Frete - KEA)

Abaixo, a aplicação prática da arquitetura para um processo de Cotação de Frete Internacional, exemplificando a separação de robôs e a **linguagem direta e funcional**.

### Fase 1: Entrada de Dados e Validação

**1. Robô de Triagem e Envio para Leitura (Dispatcher/Sender)**
*   **Função:** Monitorar continuamente o Notion e o E-mail em busca de novos pedidos.
*   **Ação:** Identifica a solicitação, baixa os documentos anexos (Fatura e Lista de Itens), padroniza os nomes dos arquivos e envia para a ferramenta de Leitura Inteligente (Verifai).
*   **Objetivo:** Garantir que o documento seja legível e esteja pronto para processamento.

**2. Robô de Validação e Disparo de Cotação (Performer/Receiver)**
*   **Função:** Processar os dados extraídos pela leitura inteligente.
*   **Ação:**
    *   Cruza as informações lidas nos documentos contra o que foi preenchido no formulário do pedido (pesos, medidas, endereços).
    *   Caso encontre divergências, marca o item para revisão humana.
    *   Estando tudo correto, consulta a lista de fornecedores e envia os e-mails solicitando orçamento.
*   **Objetivo:** Garantir a qualidade dos dados antes de contatar os fornecedores.

### Fase 2: Gestão das Propostas

**3. Robô de Monitoramento de Respostas (Dispatcher)**
*   **Função:** Verificar o retorno das transportadoras.
*   **Ação:**
    *   Monitora a caixa de e-mail identificando respostas vinculadas aos pedidos em aberto.
    *   Controla o prazo de resposta (72h ou 96h). Se o fornecedor não responder no prazo, envia um e-mail de cobrança automaticamente.
*   **Objetivo:** Centralizar as respostas e garantir que os prazos sejam cumpridos.

**4. Robô de Comparação de Preços (Performer)**
*   **Função:** Analisar as ofertas recebidas.
*   **Ação:**
    *   Lê o conteúdo da proposta (no corpo do e-mail ou PDF anexo) para capturar preço, prazo de entrega e data de saída.
    *   Atualiza o Notion com um quadro comparativo (Ranking) das melhores opções baseadas em preço e prazo.
    *   Muda o status do pedido para "Aguardando Aprovação".
*   **Objetivo:** Entregar os dados prontos para tomada de decisão do gestor.

### Fase 3: Oficialização do Embarque

**5. Robô de Verificação de Aprovação (Dispatcher)**
*   **Função:** Identificar pedidos aprovados pelo gestor.
*   **Ação:** Varre o Notion buscando itens onde a decisão humana foi tomada e verifica se todas as informações finais estão preenchidas corretamente para o cadastro.
*   **Objetivo:** Separar o fluxo de decisão do fluxo de cadastro no sistema.

**6. Robô de Cadastro no Sistema (Performer - Integração OSA)**
*   **Função:** Registrar o embarque oficial.
*   **Ação:** Acessa o sistema OSA e realiza o cadastro completo do embarque (criação do ASN), inserindo todos os detalhes técnicos e financeiros. Ao final, salva o número do protocolo gerado no Notion.
*   **Objetivo:** Eliminar a digitação manual de dados complexos no sistema ERP.

### Fase 4: Pós-Embarque

**7. Robô de Rastreamento (Standalone)**
*   **Função:** Acompanhar o trânsito da carga.
*   **Ação:**
    *   Diariamente, verifica a lista de embarques em andamento.
    *   Consulta o status atualizado (Coleta, Em Trânsito, Desembaraço, Entrega) e atualiza tanto o sistema OSA quanto o Notion.
    *   Encerra o processo quando a entrega é confirmada.
*   **Objetivo:** Manter a visibilidade da operação atualizada sem intervenção manual.
