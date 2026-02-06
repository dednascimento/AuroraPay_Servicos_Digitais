
MISSÃO ATUAL DO AGENTE

1) Assuma que a estrutura atual do repositório é provisória.
2) Seu PRIMEIRO objetivo é remodelar a arquitetura do projeto.
3) Não implemente lógica, código ou automação antes de:
   - definir a arquitetura
   - documentar essa arquitetura
   - propor a estrutura final de pastas

---

MODO DE TRABALHO

- Trabalhe sempre em etapas explícitas.
- Antes de executar qualquer ação, explique o que será feito.
- Nunca pule etapas.
- Não presuma tecnologias sem justificar.
- Não “otimize” antes de entender o problema.
- Priorize clareza e rastreabilidade, não velocidade.

---

MODO DE EXECUÇÃO

Siga rigorosamente esta ordem:

ETAPA 1 — Arquitetura
- Analisar o contexto do projeto AuroraPay (régua de cobrança)
- Analisar os artefatos existentes:
  - Excel de entrada
  - Templates de e-mail em Markdown
  - Logs esperados
- Definir:
  - fluxos
  - responsabilidades
  - limites de cada módulo
- Criar documentação arquitetural em Markdown

⚠️ Não avance para nenhuma outra etapa antes de concluir esta.

ETAPA 2 — Estrutura
- Propor e criar uma nova estrutura de pastas
- Reorganizar os arquivos existentes conforme a arquitetura
- Justificar mudanças estruturais

ETAPA 3 — Execução incremental
- Somente após arquitetura e estrutura estarem claras:
  - implementar leitura do Excel
  - implementar regras da régua
  - implementar disparo de e-mails
  - implementar logs
  - implementar interface de visualização

---

REGRAS IMPORTANTES

- O Excel é fonte legítima de dados (não é provisório).
- Os templates de e-mail são conteúdo versionável e externo à lógica.
- A régua de cobrança atua por fatura, não apenas por cliente.
- O agente não deve “inventar” features que não resolvam rotina real.
- Toda decisão relevante deve ser documentada.

---

CRITÉRIO DE SUCESSO

O trabalho está correto se:
- Qualquer pessoa entender o projeto apenas lendo os arquivos
- A arquitetura explicar o funcionamento sem explicação verbal
- O sistema reduzir trabalho humano real
- O projeto puder ser reutilizado como serviço do ITPD
