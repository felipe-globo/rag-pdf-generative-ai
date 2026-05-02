# Backlog do projeto — RAG com documentos PDF

Organização em **três releases**, do núcleo funcional até entrega e refinamentos. Itens são objetivos e podem virar *issues* no GitHub.

## Estado atual (pós‑MVP backend)

**MVP backend + CLI:** concluído — pipeline *PDF → chunks → embeddings → Chroma persistido → retrieval → resposta LLM com citações*, exposto via `app.py` e scripts auxiliares em `scripts/`.

**Interface gráfica (UI):** deliberadamente **não implementada nesta versão**. Itens relacionados foram movidos para evoluções futuras (principalmente Releases 2–3).

---

## Release 1 — Core (MVP funcional do RAG)

**Objetivo:** pipeline completo *ingestão/indexação → pergunta → resposta*, executável localmente (via CLI).

| # | Item | Notas |
|---|------|--------|
| R1.1 | Estruturar pacote Python (`src/rag_pdf/`: ingestão, embeddings, vector store, RAG, LLM, config) | ✅ MVP |
| R1.2 | Implementar leitura de PDF (PyPDF) e normalização básica de texto | ✅ MVP |
| R1.3 | Implementar *chunking* (tamanho, overlap) com parâmetros via config/env | ✅ MVP |
| R1.4 | Integrar modelo de embeddings e vector store (Chroma) com persistência em disco | ✅ MVP |
| R1.5 | Implementar fluxo de *retrieval* (*top-k*) e *chain* para o LLM (prompt grounded + citações) | ✅ MVP |
| R1.6 | ~~Implementar UI mínima (Streamlit)~~ | **Futuro** — ver Release 2 (R2.7) / Release 3 |
| R1.7 | Configuração via `.env` + `python-dotenv`; validar ausência de segredos no Git | ✅ MVP |
| R1.8 | Documentar README: instalação, execução CLI (`app.py`), variáveis obrigatórias | ✅ MVP |

**Critério de conclusão da Release 1:** um usuário consegue, em máquina local, indexar PDF(s) e obter respostas coerentes com o corpus carregado — **cumprido com CLI** (`app.py`).

---

## Release 2 — Qualidade (precisão, UX e robustez)

**Objetivo:** melhorar utilidade e confiabilidade sem mudar o escopo fundamental do MVP.

| # | Item | Notas |
|---|------|--------|
| R2.1 | Exibir **trechos recuperados** e metadados (arquivo, página/chunk) junto à resposta | Transparência e avaliação acadêmica |
| R2.2 | Ajustar prompt do sistema: instruções para citar apenas o contexto e admitir “não sei” | Reduz alucinação fora do corpus |
| R2.3 | Parâmetros de RAG expostos na **CLI** ou arquivo de config (*top‑k*, chunk size, temperatura) | UI web como evolução em R2.7 |
| R2.4 | Tratamento de erros explícito (PDF vazio, falha de API, índice vazio) | Mensagens claras ao usuário |
| R2.5 | Testes automatizados com *pytest* (doubles embeddings/LLM; integração sintética) | ✅ baseline em `tests/` — expandir cenários conforme roadmap |
| R2.6 | (*Opcional*) estratégia para PDFs com pouco texto — aviso ao usuário ou tentativa de OCR simples | Escopo incremental |
| R2.7 | **Nova — UI (Streamlit ou web)** | Upload, disparo de indexação, chat, visualização opcional dos trechos recuperados |


**Critério de conclusão da Release 2:** fluxo estável, respostas mais auditáveis e experiência menos frágil para demonstração e correção.

---

## Release 3 — Entrega final (refinamentos, documentação e deploy)

**Objetivo:** fechar o ciclo acadêmico com documentação consolidada e opção de demonstração acessível — **opcional quando houver UI ou demo pública**.

| # | Item | Notas |
|---|------|--------|
| R3.1 | Revisar documentação em `/docs` (escopo, arquitetura, backlog) conforme implementação real | Consistência código × docs |
| R3.2 | Diagramas atualizados (Mermaid) e glossário breve (RAG, embedding, chunk) | Apêndice opcional em `arquitetura.md` |
| R3.3 | Script ou Makefile com alvos `install`, `run`, `test` (se aplicável) | Reduz fricção para avaliador |
| R3.4 | (*Opcional*) deploy estático da UI ou container Docker para demo | Streamlit Community Cloud ou Docker local |
| R3.5 | (*Opcional*) `LICENSE` e política de dados se houver uso de PDFs reais | Alinhamento institucional |
| R3.6 | Tag de versão (ex.: `v1.0.0`) e release notes curtas no GitHub | Rastreabilidade da entrega |

**Critério de conclusão da Release 3:** projeto apresentável, documentado e reproduzível por terceiros com esforço baixo.
