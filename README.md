## RAG com documentos PDF usando IA Generativa

Projeto acadêmico (Pós-graduação em Engenharia de Software com foco em IA) para construir um sistema de **Retrieval-Augmented Generation (RAG)** que:

- lê e processa documentos **PDF**
- cria **embeddings** de trechos (chunks)
- armazena e consulta em uma **base vetorial**
- responde perguntas **grounded** no conteúdo dos documentos (com rastreabilidade de fontes)

---

## Arquitetura (alto nível)

Fluxo principal do RAG:

1. **Ingestão**
   - leitura de PDFs
   - extração de texto e limpeza básica
2. **Chunking**
   - divisão do texto em trechos com sobreposição (para preservar contexto)
3. **Embeddings**
   - geração de vetores para cada chunk (modelo de embeddings)
4. **Indexação / Vector Store**
   - persistência dos vetores e metadados (ex.: `source`, página, posição)
5. **Retrieval**
   - busca por similaridade (top‑k) + filtros por metadados (quando aplicável)
6. **Geração (LLM)**
   - montagem do prompt com os trechos recuperados
   - resposta final com base no contexto recuperado (idealmente com **citações**)

Componentes sugeridos (camadas):

- **UI/API**: Streamlit (interface de chat e upload/seleção de PDFs)
- **RAG Core**: pipeline de ingestão, indexação, retrieval e geração
- **Storage**: diretório de persistência do Chroma (ou outro vector store)
- **Config**: variáveis de ambiente (`.env`) para chaves e parâmetros

---

## Estrutura sugerida do repositório

> A estrutura abaixo melhora organização, testabilidade e avaliação acadêmica. Você pode adotar integralmente antes de implementar as features.

```
.
├── README.md
├── requirements.txt
├── .gitignore
├── .env.example
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
- **Rastreabilidade de fontes** (metadados por chunk: arquivo, página)
- **Configuração via ambiente** (sem chaves hard-coded)
- **Testes de fumaça** (indexação e retrieval mínimos)

---

## Segurança

- Não versione `.env` nem chaves de API.
- Não versione PDFs reais/privados (use `data/pdfs/` ignorado no git).

---

## Licença

Defina a licença conforme orientação da instituição (ex.: MIT para projeto aberto) ou mantenha como “uso acadêmico”.

