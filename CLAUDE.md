# CLAUDE.md

## Repository Overview

This is the **Mistral AI Cookbook** — a collection of examples, guides, and integrations demonstrating Mistral's models and APIs. Content includes Jupyter notebooks, Python applications, and documentation contributed by Mistral engineers, the community, and partners.

## Repository Structure

```
cookbook/
├── quickstart.ipynb              # Entry-point notebook (chat, embeddings basics)
├── CONTRIBUTING_GUIDE.md         # Contribution guidelines and security setup
├── concept-deep-dive/            # Educational deep-dives (prompting, quantization, sampling, tokenization)
├── mistral/                      # Official Mistral examples organized by capability
│   ├── agents/                   # Agent implementations
│   │   ├── agents_api/           # Framework-based (Mistral Agents API) — 6 projects
│   │   └── non_framework/        # Custom agent implementations
│   ├── classifier_factory/       # Fine-tuning classifiers
│   ├── data_generation/          # Synthetic data generation
│   ├── embeddings/               # Embedding examples
│   ├── evaluation/               # Evaluation frameworks
│   ├── fine_tune/                # Fine-tuning guides
│   ├── function_calling/         # Function calling (including text-to-SQL)
│   ├── image_understanding/      # Pixtral image processing
│   ├── lechat_custom_mcp_server/ # MCP server examples
│   ├── moderation/               # Content moderation
│   ├── ocr/                      # OCR and document understanding
│   ├── prompting/                # Prompting techniques
│   └── rag/                      # RAG implementations
├── third_party/                  # 34 third-party integrations (LlamaIndex, LangChain, ChromaDB, etc.)
├── data/                         # Shared data files (CSV, SQL, JSONL)
├── images/                       # Screenshots and diagrams
└── gif/                          # Demo GIFs
```

## Key Conventions

### File Formats
- **Notebooks (.ipynb)**: Primary format for examples (~94 notebooks). Must be runnable on Google Colab.
- **Python scripts (.py)**: Used in agent projects for tools, backends, and MCP servers (~46 files).
- **Markdown (.md)**: Used for concept deep-dives and README files within subdirectories (~54 files).

### Naming Conventions
- Snake_case for notebooks and directories: `basic_RAG.ipynb`, `function_calling/`
- Brand names kept as-is when relevant: `Neo4j_rag.ipynb`, `Pixtral_function_calling.ipynb`
- Agent projects use descriptive directory names: `financial_analyst/`, `travel_assistant/`

### Dependency Management
- **pyproject.toml** + **uv.lock**: Used in modern agent projects (agents_api/)
- **requirements.txt**: Used in simpler or older projects
- Python version: typically 3.11+
- Always pin package versions in notebooks and config files

### Content Guidelines (from CONTRIBUTING_GUIDE.md and README.md)
- Include authorship: name, GitHub handle, and affiliation
- Keep images under 500KB
- Maintain neutral tone, minimize marketing language
- Respect copyright — don't copy content without permission
- Tag all package versions for reproducibility

## Security

### Pre-commit Hooks (REQUIRED)
Install before committing:
```bash
pip install pre-commit
pre-commit install
```

Hooks enforced (`.pre-commit-config.yaml`, using `pre-commit-hooks` v4.5.0):
- `detect-private-key` — blocks commits containing API keys or credentials
- `check-byte-order-marker` — prevents BOM characters
- `check-merge-conflict` — catches unresolved merge conflict markers
- `check-symlinks` — validates symlinks
- `check-yaml`, `check-toml` — format validation
- `trailing-whitespace`, `end-of-file-fixer`, `mixed-line-ending` — formatting

**Never commit API keys, secrets, or credentials.** Use environment variables instead (e.g., `os.environ["MISTRAL_API_KEY"]`).

### CI/CD
- **security-check.yml**: Runs `detect-private-key` on all pushes/PRs to main/develop (Python 3.9)
- **trigger-docs-update.yml**: Pushes to main trigger a webhook to update `mistralai/platform-docs` via `COOKBOOKS_UPDATE_KEY` secret

## Development Workflow

1. Fork and clone the repository
2. Install pre-commit hooks: `pip install pre-commit && pre-commit install`
3. Create a feature branch from `main`
4. Add or update content following the conventions above
5. Test notebooks locally or on Google Colab
6. Submit a PR using the provided template (`.github/pull_request_template.md`)

### PR Checklist (from template)
- Code is self-reviewed and well-commented
- Package versions are tagged
- New cookbooks are added to README.md tables
- No private keys or secrets included

## Project Organization Patterns

### Agent Projects (`mistral/agents/`)
Agent projects under `agents_api/` include 6 projects with varying structures:

| Project | pyproject.toml | requirements.txt | Entry point |
|---------|:-:|:-:|---|
| financial_analyst | — | — | app.py |
| food_diet_companion | Yes | Yes | — |
| github_agent | — | — | — |
| multi_agents_data_analysis | Yes | — | app.py |
| prd_linear_ticket | — | — | app.py |
| travel_assistant | Yes | — | — |

Common project structure:
```
agent_name/
├── pyproject.toml        # Dependencies and project config (when present)
├── uv.lock               # Locked dependencies (when present)
├── requirements.txt      # Alternative dependency file (when present)
├── README.md             # Usage instructions
├── app.py or main.py     # Entry point
├── tools/                # Tool implementations (MCP servers, utilities)
├── backend/              # Backend logic
└── configs.py            # Centralized configuration
```

### Third-Party Integrations (`third_party/`)
34 integrations including: Azure_AI_Search, CAMEL_AI, Chainlit, ChromaDB, E2B_Code_Interpreting, Haystack, Indexify, Langfuse, Langtrace, LlamaIndex, MLflow, Maxim, Milvus, MongoDB, Neo4j, Neon, Ollama, Phoenix, Pinecone, Pixeltable, PydanticAI, argilla, gradio, langchain, mesop, metagpt, openlit, panel, phospho, solara, streamlit, wandb, x-cmd, and MS_Autogen_pgsql.

Each integration typically contains:
```
ToolName/
├── README.md             # Setup and usage guide
└── example_notebook.ipynb # Working example with the integration
```

### Concept Deep-Dives (`concept-deep-dive/`)
Educational content organized by topic (prompting, quantization, sampling, tokenization) with markdown docs and visual assets (PNG diagrams).

### Data Files (`data/`)
Shared datasets used by notebooks:
- `northwind-schema.sql` — SQL schema for function calling examples
- `northwind-queries.jsonl` — JSONL query samples
- `Symptom2Disease.csv` — Classification dataset
- `LeetCodeTSNE.csv` — Embedding visualization dataset

## Common Tools and Libraries
- `mistralai` — Mistral Python SDK
- `chainlit` — Chat UI for agent demos
- `langchain` / `llama-index` — LLM orchestration
- `chromadb` / `pinecone` / `milvus` — Vector stores for RAG
- `uv` — Fast Python package manager (used in newer projects)
