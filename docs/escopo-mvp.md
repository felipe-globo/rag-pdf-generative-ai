# Escopo do MVP — RAG com documentos PDF

## 1. Propósito do documento

Este documento delimita o **Produto Mínimo Viável (MVP)** do sistema de *Retrieval-Augmented Generation* (RAG) sobre documentos PDF, servindo como referência para desenvolvimento, avaliação acadêmica e controle de escopo.

## 2. Visão do MVP

O MVP consiste em um sistema que:

1. aceita **documentos PDF** como fonte de conhecimento;
2. **indexa** o conteúdo por meio de *chunking*, *embeddings* e armazenamento em **base vetorial**;
3. responde a **perguntas em linguagem natural** com base exclusiva (ou prioritariamente) no texto recuperado dos documentos.

## 3. Requisitos funcionais

| ID | Requisito | Prioridade (MVP) |
|----|-----------|------------------|
| RF-01 | Carregar um ou mais arquivos PDF e extrair texto utilizável | Alta |
| RF-02 | Dividir o texto em **chunks** com tamanho e sobreposição configuráveis | Alta |
| RF-03 | Gerar **embeddings** para cada chunk e persistir no **vector store** | Alta |
| RF-04 | Permitir **consulta** ao índice (similaridade) retornando os trechos mais relevantes (*top-k*) | Alta |
| RF-05 | Enviar ao **LLM** o contexto recuperado + pergunta do usuário e gerar **resposta textual** | Alta |
| RF-06 | Expor **interface** (ex.: Streamlit) para upload/seleção de PDFs, pergunta e exibição da resposta | Alta |
| RF-07 | Associar metadados mínimos aos chunks (ex.: nome do arquivo, página ou índice do chunk) para rastreabilidade | Média |
| RF-08 | Documentar variáveis de ambiente (ex.: chave de API) via `.env.example` | Média |

## 4. Requisitos não funcionais

| ID | Requisito | Critério / observação |
|----|-----------|------------------------|
| RNF-01 | **Segurança de credenciais** | Chaves de API não versionadas; uso de `.env` ignorado pelo Git |
| RNF-02 | **Reprodutibilidade** | `requirements.txt` e instruções de instalação no README |
| RNF-03 | **Simplicidade operacional** | Vector store local (ex.: Chroma persistido em disco) sem infraestrutura externa obrigatória |
| RNF-04 | **Desempenho razoável** | MVP aceita latência compatível com ambiente acadêmico; sem SLA formal |
| RNF-05 | **Manutenibilidade** | Separação lógica entre ingestão, armazenamento, RAG e UI |
| RNF-06 | **Rastreabilidade acadêmica** | Possibilidade de identificar de qual documento/trecho partiu a informação (mínimo viável) |

## 5. Fora do escopo do MVP

Os itens abaixo **não** fazem parte do MVP e podem ser tratados em releases posteriores ou permanecerem fora do projeto, conforme decisão documentada.

| Item | Motivo |
|------|--------|
| Autenticação de usuários e multi-tenancy | Complexidade de produto e infraestrutura além do objetivo acadêmico do MVP |
| Processamento assíncrono em fila (Celery, etc.) | Não necessário para volume e uso previstos no MVP |
| OCR avançado para PDFs escaneados de baixa qualidade | Dependências e tuning adicionais; pode entrar em release de qualidade se houver demanda |
| Avaliação sistemática com métricas de RAG (Ragas, golden sets) | Útil, mas tratada como melhoria de qualidade pós-MVP |
| Deploy em produção (Kubernetes, CDN, observabilidade enterprise) | Escopo de entrega final / opcional |
| Suporte a múltiplos provedores de LLM com feature parity | Integração prioritária com um provedor no MVP |
| Edição colaborativa de documentos ou versionamento fino de PDFs no sistema | Fora do foco de “consulta sobre corpus estático” |

## 6. Premissas e dependências

- Acesso a um **provedor de LLM e embeddings** via API (ex.: OpenAI ou equivalente configurável).
- PDFs com texto extraível; PDFs predominantemente imagem podem falhar ou ter qualidade inferior sem OCR.

## 7. Critérios de aceite do MVP (sumário)

- É possível **indexar** pelo menos um PDF e **persistir** o índice localmente.
- É possível **fazer uma pergunta** e obter uma **resposta** fundamentada nos trechos recuperados.
- O repositório contém **documentação** suficiente para instalar e executar o projeto.
