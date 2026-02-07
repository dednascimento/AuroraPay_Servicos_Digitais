# Arquitetura do Sistema de Cobrança AuroraPay

> **Nota**: Este documento reflete a arquitetura de uma solução de portfólio. Para ambientes enterprise, recomenda-se o uso de filas (RabbitMQ/Kafka) e microsserviços segregados.

Este documento descreve a arquitetura técnica do sistema de automação de cobranças, seguindo princípios de **Clean Architecture** e **Modularidade**.

## 1. Visão Geral
O sistema tem como objetivo ler uma base de dados de faturas (Excel), processar regras de negócio baseadas em datas (vencimento) e enviar notificações por e-mail (HTML) de forma idempotente.

## 2. Estrutura de Diretórios
```
src/
├── core/           # Entidades de Domínio (Puras)
├── services/       # Regras de Negócio e Casos de Uso
├── infrastructure/ # Adaptadores Externos (Excel, E-mail, Log, OS)
└── utils/          # Utilitários compartilhados
```

## 3. Componentes Principais

### 3.1 Core (`src/core`)
Define as estruturas de dados fundamentais do sistema, sem dependências externas.
- **Entities**: `Invoice`, `InvoiceItem`.
- **Enums**: `BillingAction`.

### 3.2 Services (`src/services`)
Contém a lógica de orquestração.
- **BillingManager**: 
  - Lê faturas via `ExcelAdapter`.
  - Determina a regra a ser aplicada (`D-5`, `D0`, `D+3`) com base na data atual.
  - Verifica idempotência (se já foi processado hoje) via `LogAdapter`.
  - Delega o envio de e-mail para `EmailAdapter`.

### 3.3 Infrastructure (`src/infrastructure`)
Implementa a comunicação com o mundo externo.
- **ExcelAdapter**: Lê arquivo `Regua_Cobranca_V2.xlsx` e normaliza dados de múltiplas abas (`Clientes`, `Faturas`, `Itens`) para objetos de domínio.
- **EmailAdapter**: Gerencia templates HTML, substituição de variáveis dinâmicas e conexão SMTP com Gmail.
- **LogAdapter**: Mantém um registro de auditoria (`execution_log.csv`) para garantir idempotência.

## 4. Fluxo de Execução
1. **Início**: `main.py` é acionado (pode receber flags `--test`, `--rule`).
2. **Setup**: Instanciação dos adaptadores e injeção de dependência no `BillingManager`.
3. **Leitura**: `BillingManager` solicita faturas ao `ExcelAdapter`.
4. **Processamento** (Loop por Fatura):
   - Calcula Delta de dias (Hoje - Vencimento).
   - Define Regra (ex: `D0`).
   - Se `--test` inativo: Verifica se regra já foi executada hoje para aquele ID.
5. **Ação**:
   - `EmailAdapter` carrega template correspondente.
   - Gera tabela dinâmica de itens.
   - Dispara e-mail via SMTP.
6. **Log**: Resultado (SUCCESS/FAILED) é gravado no CSV.

## 5. Design Patterns Utilizados
- **Dependency Injection**: `BillingManager` recebe adaptadores no construtor.
- **Adapter Pattern**: Isolamento de bibliotecas externas (`pandas`, `smtplib`).
- **Repository Pattern** (Simplificado): Leitura de dados abstraída no `ExcelAdapter`.
