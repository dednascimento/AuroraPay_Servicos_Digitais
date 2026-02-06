# Procedimento Operacional Padrão (POP)

**Título**: Execução Diária da Régua de Cobrança  
**Código**: POP-COB-001  
**Versão**: 1.0  
**Data**: 06/02/2026

---

## 1. Objetivo
Padronizar a execução do script de automação de cobranças, garantindo que os dados de entrada estejam corretos e que o processamento ocorra de forma segura e auditável.

## 2. Pré-Requisitos
1.  Python 3 instalado e configurado no PATH.
2.  Arquivo `.env` configurado com credenciais de SMTP ativas.
3.  Acesso à pasta `data/input/`.

## 3. Fluxo de Processamento (Entrada/Saída)

### 3.1 Entrada de Dados
O sistema consome o arquivo: `data/input/Regua_Cobranca_V2.xlsx`

**Estrutura Obrigatória do Arquivo:**
O arquivo **DEVE** conter as seguintes abas e colunas. Nomes de colunas são normalizados (minúsculos/sem espaços), mas a ordem ideal é:

1.  **Aba `Clientes`**:
    *   `cliente_id` (Chave Primária, ex: CLI_01)
    *   `nome`
    *   `email`

2.  **Aba `Faturas`**:
    *   `fatura_id` (Chave Primária, ex: FAT_001)
    *   `cliente_id` (Chave Estrangeira)
    *   `data_vencimento` (DD/MM/AAAA)
    *   `status`

3.  **Aba `Itens`**:
    *   `fatura_id` (Chave Estrangeira para vincular itens à fatura)
    *   `descricao`
    *   `valor`

> **Nota**: O sistema aceita reajustes de colunas desde que os nomes essenciais existam. Colunas extras serão ignoradas.

### 3.2 Processamento
O script cruza as informações:
1.  Lê todas as faturas em aberto.
2.  Busca os itens correspondentes na aba `Itens`.
3.  Busca os dados do cliente na aba `Clientes`.
4.  Aplica a regra do dia (D-5, D0, D+3).

### 3.3 Saída de Dados
*   **E-mails**: Disparados via SMTP para os clientes.
*   **Logs**: Registrados em `data/output/execution_log.csv` com Data, ID da Fatura, Regra e Status.

---

## 4. Instruções de Execução

### 4.1 Operação de Rotina (Produção)
Para rodar a régua oficial do dia:
```bash
python src/main.py
```
*   O sistema verificará o log para não enviar duplicatas.

### 4.2 Simulação e Testes (Homologação)
Para verificar se uma nova base de dados está correta sem enviar e-mails reais duplicados ou afetar o log oficial:
```bash
python src/main.py --test
```

Para validar apenas uma regra específica (ex: verificar se os atrasados estão sendo capturados):
```bash
python src/main.py --test --rule D+3
```

## 5. Resolução de Problemas

| Sintoma | Causa Provável | Solução |
|---------|----------------|---------|
| "Client not found" no log | ID do cliente na aba `Faturas` não bate com aba `Clientes`. | Verificar digitação dos IDs no Excel. |
| E-mail não enviado | Idempotência ativa (já rodou hoje). | Usar `--test` para forçar ou apagar linha do log. |
| "Credenciais inválidas" | Arquivo `.env` incorreto. | Verificar senha de aplicativo Google no `.env`. |
