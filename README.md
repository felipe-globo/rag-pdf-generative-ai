## RAG com documentos PDF usando IA Generativa

Projeto acadêmico (Pós-graduação em Engenharia de Software com foco em IA) para construir um sistema de **Retrieval-Augmented Generation (RAG)** que:

- lê e processa documentos **PDF**
- cria **embeddings** de trechos (chunks)
- armazena e consulta em uma **base vetorial**
- responde perguntas **grounded** no conteúdo dos documentos (com rastreabilidade de fontes)

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

Camadas de referência: **UI** (Streamlit), **orquestração RAG** (LangChain), **storage** (Chroma em disco), **config** (`.env`).

Para diagrama Mermaid, tabela de componentes e integração entre módulos, ver [`docs/arquitetura.md`](docs/arquitetura.md).

---

## Estrutura sugerida do repositório

> A estrutura abaixo melhora organização, testabilidade e avaliação acadêmica. A pasta `docs/` já reflete a documentação técnica do MVP e da arquitetura; `src/` permanece o alvo da implementação.

```
.
├── README.md
├── requirements.txt
├── .gitignore
├── .env.example
├── docs/
│   ├── escopo-mvp.md
│   ├── backlog.md
│   └── arquitetura.md
├── data/
│   ├── pdfs/                  # PDFs de entrada (não versionar conteúdo real)
│   └── chroma/                # persistência do vector store (não versionar)
├── src/
│   └── rag_pdf/
│       ├── __init__.py
│       ├── config.py           # leitura de env + defaults
│       ├── ingestion/
│       │   ├── __init__.py
│       │   ├── pdf_loader.py   # leitura/extração de texto do PDF
│       │   └── chunking.py     # splitters e normalização
│       ├── vectorstore/
│       │   ├── __init__.py
│       │   └── chroma.py       # criação/persistência/consulta
│       ├── rag/
│       │   ├── __init__.py
│       │   ├── retriever.py    # k, filtros, estratégia
│       │   └── chain.py        # orquestração LLM + contexto
│       └── ui/
│           ├── __init__.py
│           └── app_streamlit.py
└── tests/
    └── test_smoke.py
```

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

## Como rodar

### Interface (Streamlit)

Quando `src/rag_pdf/ui/app_streamlit.py` existir:

```bash
streamlit run src/rag_pdf/ui/app_streamlit.py
```

### Execução por linha de comando (opcional)

Se você criar um entrypoint (ex.: `python -m rag_pdf ...`), documente aqui os comandos principais:

- indexar PDFs
- fazer perguntas
- limpar/recriar índice

---

## Tecnologias utilizadas

- **LangChain**: orquestração do pipeline RAG (loaders, splitters, retrievers, chains)
- **ChromaDB**: vector store local com persistência
- **PyPDF**: extração de texto de PDFs
- **tiktoken**: utilitários de tokenização/contagem (controle de contexto)
- **Streamlit**: interface web simples para demonstração
- **python-dotenv**: carregamento de `.env` (segurança e portabilidade)

---

## Boas práticas adotadas (recomendadas para avaliação)

- **Separação de camadas** (UI / core / storage / config)
- **Persistência do índice** e reindexação controlada
- **Rastreabilidade de fontes** (metadados por chunk: arquivo, página), conforme reforçado em [`docs/escopo-mvp.md`](docs/escopo-mvp.md)
- **Configuração via ambiente** (sem chaves hard-coded)
- **Testes de fumaça** (indexação e retrieval mínimos), previstos no roadmap em [`docs/backlog.md`](docs/backlog.md)

---

## Segurança

- Não versione `.env` nem chaves de API.
- Não versione PDFs reais/privados (use `data/pdfs/` ignorado no git).

---

## Licença

Defina a licença conforme orientação da instituição (ex.: MIT para projeto aberto) ou mantenha como “uso acadêmico”.

