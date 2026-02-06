# Sistema de Cobrança AuroraPay 🚀

Sistema automatizado para envio de faturas e lembretes de cobrança via e-mail.

## Funcionalidades
- 📧 **Envio Automático**: Dispara e-mails baseados em regras (5 dias antes, no dia, 3 dias após).
- 🎨 **Templates HTML**: Layouts profissionais com tabelas dinâmicas de itens.
- 📊 **Excel V2**: Suporte a múltiplas abas (Clientes, Faturas, Itens).
- 🛡️ **Idempotência**: Garante que o mesmo e-mail não seja enviado duas vezes no mesmo dia.
- 🧪 **Modo de Teste**: Simula envios sem afetar o histórico real.

## Instalação

1. Clone o repositório.
2. Crie um ambiente virtual:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure o `.env` com suas credenciais de e-mail:
   ```env
   SMTP_EMAIL=seu_email@gmail.com
   SMTP_PASSWORD=senha_app_google
   ```

## Como Usar

### Execução Normal (Produção)
Rode diariamente para processar a régua:
```bash
python src/main.py
```

### Modo de Teste
Para forçar envio e simular cenários:
```bash
python src/main.py --test
```

### Filtrar por Regra Específica
Se quiser testar apenas um tipo de aviso:
```bash
python src/main.py --test --rule D-5
python src/main.py --test --rule D0
python src/main.py --test --rule D+3
```

## Estrutura de Dados (Excel)
O arquivo `data/input/Regua_Cobranca_V2.xlsx` deve conter 3 abas. Para detalhes de preenchimento, consulte o [Manual Operacional (POP)](docs/POP.md).

## Documentação Completa
Este projeto conta com uma documentação abrangente para desenvolvedores e usuários:
- 🏗️ **[Arquitetura do Sistema](docs/ARCHITECTURE.md)**: Visão técnica e decisões de design.
- 🔀 **[Fluxograma](docs/FLOWCHART.md)**: Diagrama visual do processo de decisão.
- 📋 **[Requisitos](docs/REQUIREMENTS.md)**: Lista de requisitos funcionais e não funcionais.
- 📖 **[Manual Operacional (POP)](docs/POP.md)**: Guia passo-a-passo para execução e operação diária.
