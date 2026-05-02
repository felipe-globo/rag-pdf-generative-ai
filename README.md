## RAG com documentos PDF usando IA Generativa

**Versão estável:** [`v1.0.0`](https://github.com/felipe-globo/rag-pdf-generative-ai/releases) (Semantic Versioning) — **MVP backend + CLI concluído**.

Projeto acadêmico (Pós-graduação em Engenharia de Software com foco em IA) para construir um sistema de **Retrieval-Augmented Generation (RAG)** que:

- lê e processa documentos **PDF**
- cria **embeddings** de trechos (chunks)
- armazena e consulta em uma **base vetorial**
- responde perguntas **grounded** no conteúdo dos documentos (com rastreabilidade de fontes)

### Status do MVP (escopo fechado)

O **MVP do backend RAG está concluído e validado localmente** via **CLI** (`app.py`): ingestão → indexação (Chroma persistido) → *retrieval* semântico → resposta com LLM e citações derivadas dos metadados.

**Fora do escopo desta entrega:** interface gráfica (ex.: Streamlit, *web app*, *chat UI*). Essa evolução está registrada como trabalho futuro em [`docs/backlog.md`](docs/backlog.md) e na seção [Próximos passos](#próximos-passos--trabalho-futuro) abaixo.

---

## Release v1.0.0 — MVP estável

**Objetivo desta versão:** congelar o **primeiro baseline funcional**: RAG ponta‑a‑ponta por linha de comando, testável sem UI.

| Incluído | Descrição |
|----------|-----------|
| Pipeline completo | Ingestão PDF → chunking → embeddings → Chroma persistido → retrieval semântico → chain LLM com citações |
| CLI | `app.py` (`--index`, `-q`, parâmetros e `.env`; ver [Como rodar](#como-rodar-cli--mvp)) |
| Qualidade | Suite `pytest` com doubles (embeddings / LLM) e um fluxo de integração sintético |
| Documentação | `docs/` (`escopo-mvp.md`, `arquitetura.md`, `backlog.md`) + este README |

**Critérios de uso em produção acadêmica:** Python 3.9+, dependências em `requirements.txt`, `OPENAI_API_KEY` no `.env`; PDFs locais sob `PDF_DIR`; índice Chroma sob `CHROMA_PERSIST_DIR`.

---

## Documentação técnica

Documentação de escopo, planejamento e arquitetura está na pasta [`docs/`](docs/):

| Documento | Conteúdo |
|-----------|----------|
| [`docs/escopo-mvp.md`](docs/escopo-mvp.md) | MVP: requisitos funcionais e não funcionais, fora de escopo, critérios de aceite |
| [`docs/backlog.md`](docs/backlog.md) | Backlog em 3 releases (Core, Qualidade, Entrega final) |
| [`docs/arquitetura.md`](docs/arquitetura.md) | Componentes, fluxo de dados (PDF → resposta), diagrama Mermaid, integração entre camadas |

O **detalhamento** de arquitetura, decisões de desenho e limitações conscientes do sistema estão em `docs/arquitetura.md`. Este README resume o essencial e aponta para esses artefatos.

---

## Arquitetura (resumo)

Fluxo principal do RAG (alinha-se a [`docs/arquitetura.md`](docs/arquitetura.md)):

1. **Ingestão** — PDFs → extração de texto e normalização básica  
2. **Chunking** — divisão em trechos com sobreposição configurável  
3. **Embeddings** — vetores por chunk (mesmo modelo na indexação e na consulta)  
4. **Vector store** — persistência local (ex.: Chroma) com metadados (`source`, página, etc.)  
5. **Retrieval** — similaridade (*top‑k*) sobre o índice  
6. **LLM** — prompt com contexto recuperado + pergunta → resposta fundamentada no corpus  

Camadas de referência (MVP): **CLI** (`app.py`), **orquestração RAG** (módulos em `rag_pdf/` com LangChain/OpenAI/Chroma conforme código), **storage** (Chroma em disco), **config** (`.env`).

Para diagrama Mermaid, tabela de componentes e integração entre módulos, ver [`docs/arquitetura.md`](docs/arquitetura.md).

---

## Estrutura sugerida do repositório

> Estrutura alinhada ao MVP **backend + CLI**. PDFs e Chroma local não são versionados (ver `.gitignore`).

```
.
├── README.md
├── app.py                      # CLI end-to-end (indexar + perguntar)
├── pyproject.toml               # configuração pytest (pythonpath → src/)
├── requirements.txt
├── .gitignore
├── .env.example
├── docs/
│   ├── escopo-mvp.md
│   ├── backlog.md
│   └── arquitetura.md
├── scripts/                    # exemplos de uso por etapa (opcional)
├── data/
│   ├── pdfs/                   # PDFs de entrada (local; não versionar)
│   └── chroma/                 # persistência do vector store (local; não versionar)
├── src/
│   └── rag_pdf/
│       ├── config.py
│       ├── ingestion/          # PDF → texto → chunks
│       ├── embeddings/         # embeddings (OpenAI)
│       ├── vectorstore/       # indexação Chroma persistida
│       ├── rag/               # retrieval + chain LLM
│       ├── llm/               # provedor de chat
│       └── utils/             # ex.: bootstrap de .env
├── tests/                     # pytest — unitários + integração (doubles, sem API real)
│   ├── conftest.py
│   ├── test_loader.py
│   ├── test_retriever.py
│   ├── test_chain.py
│   └── test_integration.py
```

---

## Testes (qualidade)

Os testes rodam com **`pytest`**, **sem chamar OpenAI/Chroma em produção** nos casos principais: *embeddings* e *LLM* usam **implementações determinísticas** definidas em `tests/conftest.py` (vetores hash-based e LLM sintético).

```bash
venv/bin/pip install -r requirements.txt
venv/bin/python -m pytest -q
```

Arquivos relevantes:

| Arquivo | Cobertura focada |
|---------|------------------|
| `tests/test_loader.py` | limpeza de texto, *chunking* com *fallback* offline, `PdfReader` isolado com *mock* |
| `tests/test_retriever.py` | IDs determinísticos, validação de parâmetros, indexação + consulta no Chroma em diretório temporário |
| `tests/test_chain.py` | *prompt* + chamada ao *LLM double* + citações/meta |
| `tests/test_integration.py` | fluxo RAG sintético (`LoadedDocument` → chunks → índice → resposta), sem PDF em disco |

O `pythonpath` para importar `rag_pdf/` é definido em `pyproject.toml` (`tool.pytest.ini_options`).

---


## Requisitos

- Python **3.9+** (recomendado 3.10+)
- Chave de API do provedor de LLM/Embeddings (ex.: OpenAI)

---

## Instalação

1. Crie e ative um ambiente virtual.

```bash
python -m venv venv
source venv/bin/activate
```

2. Instale as dependências.

```bash
pip install -r requirements.txt
```

3. Configure variáveis de ambiente.

- Copie o arquivo de exemplo:

```bash
cp .env.example .env
```

- Preencha valores (ex.: `OPENAI_API_KEY`) no `.env`.

---

## Como rodar (CLI — MVP) — entrega v1.0.0

Coloque seus PDFs em `data/pdfs/` **ou** aponte `--pdf-dir` para a pasta onde estão os arquivos.

**Indexar e perguntar** (primeira execução ou após mudar corpus):

```bash
venv/bin/python app.py --index -q "Sua pergunta aqui"
```

**Somente perguntar** (índice já persistido em `CHROMA_PERSIST_DIR`):

```bash
venv/bin/python app.py -q "Sua pergunta aqui"
```

Parâmetros úteis: `--k`, `--pdf-dir`, `--persist-dir`, `--collection`, `--embed-model`, `--llm-model` (ver `app.py --help`). Variáveis de ambiente equivalentes estão em `.env.example`.

Scripts auxiliares em `scripts/` (ingestão, indexação, retrieval, resposta isolados) permanecem disponíveis para depuração.

---

## Próximos passos / trabalho futuro

Não faz parte do MVP atual; previsto como evolução de produto e detalhado no [`docs/backlog.md`](docs/backlog.md):

- **Interface gráfica** (Streamlit ou *web*) para upload, perguntas e visualização de trechos recuperados
- **Makefile / alvos** `install`, `run`, `test` para onboarding de avaliadores
- **Ampliação de cobertura de testes** (filtros metadata, cenários PDF reais opcionais, *CI* em GitHub Actions)
- Opcional: *deploy* de demo (Streamlit Cloud, Docker)

---

## Tecnologias utilizadas

- **LangChain**: integração OpenAI (embeddings e chat usados pelo código)
- **ChromaDB**: vector store local com persistência
- **PyPDF**: extração de texto de PDFs
- **tiktoken**: utilitários de tokenização/contagem (controle de contexto / chunking)
- **python-dotenv**: carregamento de `.env` (segurança e portabilidade)
- **pytest**: testes automatizados (vide seção Testes)

---

## Boas práticas adotadas (recomendadas para avaliação)

- **Separação de camadas** (CLI / núcleo RAG / embeddings / LLM / storage / config)
- **Persistência do índice** e reindexação controlada
- **Rastreabilidade de fontes** (metadados por chunk: arquivo, página), conforme reforçado em [`docs/escopo-mvp.md`](docs/escopo-mvp.md)
- **Configuração via ambiente** (sem chaves hard-coded)
- **Suite de testes automatizados** com *pytest* (`tests/` + doubles), alinhado ao backlog (Release 2) em [`docs/backlog.md`](docs/backlog.md)

---

## Segurança

- Não versione `.env` nem chaves de API.
- Não versione PDFs reais/privados (use `data/pdfs/` ignorado no git).

---

## Licença

Defina a licença conforme orientação da instituição (ex.: MIT para projeto aberto) ou mantenha como “uso acadêmico”.

