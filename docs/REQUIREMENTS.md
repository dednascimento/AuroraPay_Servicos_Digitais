# Documento de Requisitos (REQ)

> **Escopo de Portfólio**: Os requisitos abaixo foram dimensionados para demonstrar capacidade de análise e implementação Full Stack/Backend. Em um cenário real, incluiriam SLA, LGPD e Integração Bancária via API.

## 1. Objetivo
Automatizar o processo de envio de notificações de cobrança (faturas) via e-mail, garantindo pontualidade, personalização e redução da inadimplência através de uma comunicação estruturada.

## 2. Requisitos Funcionais (RF)

| ID | Descrição | Regra de Negócio |
|----|-----------|------------------|
| **RF01** | **Leitura de Base de Dados** | O sistema deve ler um arquivo Excel (`.xlsx`) contendo múltiplas abas (`Clientes`, `Faturas`, `Itens`) e relacionar os dados. |
| **RF02** | **Cálculo de Prazos** | O sistema deve calcular automaticamente a diferença de dias entre a data atual e o vencimento. |
| **RF03** | **Régua de Cobrança** | Deve implementar as seguintes regras de disparo:<br>1. **D-5**: Lembrete 5 dias antes.<br>2. **D0**: Aviso no dia do vencimento.<br>3. **D+3**: Aviso de atraso 3 dias após. |
| **RF04** | **Envio de E-mail** | O sistema deve enviar e-mails em formato HTML com layout profissional e responsivo. |
| **RF05** | **Detalhamento de Fatura** | O corpo do e-mail deve conter uma tabela detalhando os itens/serviços cobrados e seus valores. |
| **RF06** | **Links Dinâmicos** | Deve gerar botões funcionais para "Pagar Fatura" e "Negociar" (este último apenas para atrasos). |
| **RF07** | **Modo de Teste** | Deve oferecer uma flag `--test` para simular envios sem validar a idempotência diária, marcando o assunto com `[TESTE]`. |
| **RF08** | **Filtro de Execução** | Deve oferecer uma flag `--rule` para permitir testar apenas uma regra específica (ex: apenas D0). |

## 3. Requisitos Não Funcionais (RNF)

| ID | Descrição | Critério |
|----|-----------|----------|
| **RNF01** | **Idempotência** | O sistema não pode enviar o mesmo e-mail para a mesma fatura mais de uma vez no mesmo dia (salvo em modo de teste). |
| **RNF02** | **Portabilidade** | O sistema deve rodar em qualquer ambiente Windows/Linux com Python 3.8+ instalado. |
| **RNF03** | **Segurança de Credenciais** | Credenciais sensíveis (senhas de e-mail) não devem estar no código fonte, mas sim em variáveis de ambiente (`.env`). |
| **RNF04** | **Auditoria** | Todas as ações (sucesso, falha ou pulo) devem ser registradas em um arquivo de log local (`execution_log.csv`). |
| **RNF05** | **Design UX/UI** | Os e-mails devem seguir padrões de alto contraste e clareza visual (cores semânticas: Verde/Lembrete, Azul/Hoj, Vermelho/Atraso). |
| **RNF06** | **Manutenibilidade** | O código deve seguir arquitetura modular (Clean Architecture) e padrões PEP8. |
