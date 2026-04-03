# CLAUDE.md

## Repository Overview

This is the **Mistral AI Cookbook** — a collection of examples, guides, and integrations demonstrating Mistral's models and APIs. Content includes Jupyter notebooks, Python applications, and documentation contributed by Mistral engineers, the community, and partners.

## Repository Structure

```
cookbook/
├── quickstart.ipynb              # Entry-point notebook (chat, embeddings basics)
├── concept-deep-dive/            # Educational deep-dives (prompting, quantization, sampling, tokenization)
├── mistral/                      # Official Mistral examples organized by capability
│   ├── agents/                   # Agent implementations
│   │   ├── agents_api/           # Framework-based (6 projects: financial_analyst, food_diet_companion,
│   │   │                         #   github_agent, multi_agents_data_analysis, prd_linear_ticket, travel_assistant)
│   │   └── non_framework/        # Custom implementations (6 projects: agentic_workflows, earnings_calls,
│   │                             #   hubspot_dynamic_multi_agent, industrial_knowledge_agent,
│   │                             #   recruitment_agent, transcript_linearticket_agent)
│   ├── classifier_factory/       # Fine-tuning classifiers
│   ├── data_generation/          # Synthetic data generation
│   ├── embeddings/               # Embedding examples
│   ├── evaluation/               # Evaluation frameworks
│   ├── fine_tune/                # Fine-tuning guides
│   ├── function_calling/         # Function calling (including text-to-SQL)
│   ├── image_understanding/      # Pixtral image processing
│   ├── lechat_custom_mcp_server/ # MCP server examples (includes tic-tac-toe game)
│   ├── moderation/               # Content moderation
│   ├── ocr/                      # OCR and document understanding
│   │   ├── documentChunking/     #   Advanced document chunking
│   │   ├── hcls/                 #   Healthcare/Life Sciences OCR
│   │   └── product_datasheet_analysis/  # Product-specific OCR
│   ├── prompting/                # Prompting techniques
│   └── rag/                      # RAG implementations
├── third_party/                  # 33 third-party integrations
├── data/                         # Shared data files (CSV, SQL, JSONL)
├── images/                       # Screenshots and diagrams
└── gif/                          # Demo GIFs
```

### File Counts

| Type | Count |
|------|-------|
| Jupyter Notebooks (.ipynb) | ~94 |
| Python scripts (.py) | ~46 |
| Markdown files (.md) | ~54 |
| Third-party integrations | 33 |
| Agent projects (framework) | 6 |
| Agent projects (non-framework) | 6 |

### Third-Party Integrations (`third_party/`)

Organized by category:
- **RAG & Vector DBs:** LlamaIndex, LangChain, ChromaDB, Pinecone, Milvus, Neo4j, Haystack, Azure_AI_Search, MongoDB, Neon
- **Observability:** Phoenix, Langfuse, Langtrace, MLflow, OpenLIT, Maxim, phospho
- **UI/Chat:** Chainlit, Streamlit, Gradio, Mesop, Solara, Panel
- **Multi-agent:** CAMEL_AI, MS_Autogen_pgsql, metagpt, PydanticAI
- **Other:** E2B_Code_Interpreting, Indexify, argilla, Pixeltable, wandb, Ollama, x-cmd

## Key Conventions

### File Formats
- **Notebooks (.ipynb)**: Primary format for examples. Must be runnable on Google Colab.
- **Python scripts (.py)**: Used in agent projects for tools, backends, and MCP servers.
- **Markdown (.md)**: Used for concept deep-dives and README files within subdirectories.

### Naming Conventions
- Snake_case for notebooks and directories: `basic_RAG.ipynb`, `function_calling/`
- Brand names kept as-is when relevant: `Neo4j_rag.ipynb`, `Pixtral_function_calling.ipynb`
- Agent projects use descriptive directory names: `financial_analyst/`, `travel_assistant/`

### Dependency Management
- **pyproject.toml** + **uv.lock**: Used in modern agent projects (agents_api/)
- **requirements.txt**: Used in simpler or older projects
- **No root-level pyproject.toml** — each agent project manages its own dependencies
- Python version: typically 3.9+ (3.11+ for newer projects)
- `uv` is the preferred package manager for newer projects
- Always pin package versions in notebooks and config files

### Content Guidelines (from CONTRIBUTING_GUIDE.md and README.md)
- Include authorship: name, GitHub handle, and affiliation
- Keep images under 500KB
- Maintain neutral tone, minimize marketing language
- Respect copyright — don't copy content without permission
- Tag all package versions for reproducibility
- New cookbooks must be added to the README.md tables (official or third-party)

## Security

### Pre-commit Hooks (REQUIRED)
Install before committing:
```bash
pip install pre-commit
pre-commit install
```

Hooks enforced (`.pre-commit-config.yaml`, using pre-commit v4.5.0):
- `detect-private-key` — blocks commits containing API keys or credentials
- `check-byte-order-marker` — BOM detection
- `check-merge-conflict` — merge conflict markers
- `check-symlinks` — broken symlinks
- `check-yaml`, `check-toml` — format validation
- `trailing-whitespace`, `end-of-file-fixer`, `mixed-line-ending` — formatting

**Never commit API keys, secrets, or credentials.** Use environment variables instead (e.g., `os.environ["MISTRAL_API_KEY"]`). Use `.env` files locally.

### CI/CD
- **security-check.yml**: Runs `detect-private-key` on all pushes/PRs to main/develop (Python 3.9)
- **trigger-docs-update.yml**: Pushes to main trigger a webhook to update `mistralai/platform-docs` using `COOKBOOKS_UPDATE_KEY` secret

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

### Agent Projects — Framework-based (`mistral/agents/agents_api/`)
These use the Mistral Agents API and follow a common structure:
```
agent_name/
├── pyproject.toml        # Dependencies and project config
├── uv.lock               # Locked dependencies
├── README.md             # Usage instructions
├── app.py or agent.py    # Entry point
├── tools/                # Tool implementations (MCP servers, utilities)
├── mcp_servers/          # MCP server definitions (some projects)
├── backend/              # Backend logic
├── public/               # Static assets (some projects)
├── .chainlit/            # Chainlit UI config (some projects)
└── configs.py            # Centralized configuration
```

Projects: `financial_analyst`, `food_diet_companion`, `github_agent`, `multi_agents_data_analysis`, `prd_linear_ticket`, `travel_assistant`

### Agent Projects — Non-framework (`mistral/agents/non_framework/`)
Custom agent implementations using direct API calls:
- `agentic_workflows/` — Parallel/serial workflow patterns (notebooks)
- `earnings_calls/` — Multi-agent earnings call analysis (MAECAS)
- `hubspot_dynamic_multi_agent/` — HubSpot integration with Chainlit UI
- `industrial_knowledge_agent/` — Industry-specific knowledge agent
- `recruitment_agent/` — Multi-agent recruitment workflow
- `transcript_linearticket_agent/` — Transcript to ticket conversion

### Third-Party Integrations (`third_party/`)
Each integration typically contains:
```
ToolName/
├── README.md             # Setup and usage guide
└── example_notebook.ipynb # Working example with the integration
```

### Concept Deep-Dives (`concept-deep-dive/`)
Educational content organized by topic with markdown docs and visual assets (PNG diagrams):
- `prompting/` — Prompt optimization techniques
- `quantization/` — 5 method-specific notebooks (AWQ, BnB, EXL2, GGUF, GPTQ)
- `sampling/` — Temperature, top-k, top-p explanations with diagrams
- `tokenization/` — 7 markdown files covering basics, boundaries, templates, control tokens

### Shared Data (`data/`)
- `LeetCodeTSNE.csv` — LeetCode dataset
- `Symptom2Disease.csv` — Medical/healthcare data
- `northwind-queries.jsonl` — Database queries
- `northwind-schema.sql` — Database schema

## Common Tools and Libraries
- `mistralai` — Mistral Python SDK
- `chainlit` — Chat UI for agent demos
- `langchain` / `llama-index` — LLM orchestration
- `chromadb` / `pinecone` / `milvus` — Vector stores for RAG
- `uv` — Fast Python package manager (used in newer projects)
