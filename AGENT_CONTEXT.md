# Project Context

## Project Goal Summary

**deepmind1 (TheFarm)** is an automated multi-agent diligence workflow system that uses LLM-based agents orchestrated through a structured pipeline to perform investment analysis, strategic decision-making, and research tasks.

**Core Value Proposition:** Transform unstructured research questions into rigorous, auditable, multi-perspective analyses with clear recommendations and documented reasoning chains.

## Current Capabilities

The system employs **9 specialized agents** organized into four categories:

### Strategic Reasoning Agents (01-04)
| Agent | Primary Focus | Key Outputs |
|-------|---------------|-------------|
| **01 Systems & Second-Order** | System dynamics, feedback loops, value migration | System map, second-order effects, bottlenecks |
| **02 Inversion Thinking** | Failure modes, fragility, downside scenarios | Kill criteria, fragility analysis, mitigations |
| **03 Capital Allocation** | Opportunity cost, portfolio fit, alternatives | Best alternatives, decision thresholds, required returns |
| **04 Incentives & Timing** | Stakeholder incentives, market timing, power dynamics | Incentive map, timing indicators, value capture analysis |

### Equity Research Agents (06-08)
| Agent | Primary Focus | Key Outputs |
|-------|---------------|-------------|
| **06 Sector Screener** | Ticker identification, competitive landscape | List of relevant tickers, market cap tiers, sector positioning |
| **07 Fundamental Analyst** | Valuation, financial statements, earnings quality | P/E, EV/EBITDA, DCF range, balance sheet risks |
| **08 Technical Analyst** | Price action, chart patterns, momentum | Trend direction, support/resistance, RSI/MACD signals |

### Data Layer Agent (09)
| Agent | Primary Focus | Key Outputs |
|-------|---------------|-------------|
| **09 Financial Data** | Live market data retrieval, API integration | Price snapshots, financial statements, ratios, SEC filings |

**Note:** 09_financial_data is a subagent that other agents (06, 07, 08, CoVe) delegate to for live data retrieval. It does not perform analysis - only data retrieval with source attribution.

### Meta Agents (05)
| Agent | Primary Focus | Key Outputs |
|-------|---------------|-------------|
| **05 Epistemic Reality Check** | Knowledge vs assumptions, confidence calibration | Know/assume/speculate table, overconfidence flags |

### Intake System
| Component | Primary Focus | Key Outputs |
|-----------|---------------|-------------|
| **Intake Conversation Agent** | Conversational task definition, document processing | task.md, reference_materials/, session transcript |

**Note:** The Intake Conversation Agent runs via Claude Code CLI (`/intake`). It has a natural conversation with the user to understand their research question, processes any documents they provide, and outputs a structured task file. Multi-session support allows users to refine their intake over time.

## Where Things Live (intended layout)

```
TheFarm/
├── config/
│   ├── config.py          # Core configuration
│   ├── models.py          # Model routing config (Opus/Sonnet per agent)
│   ├── prompts.py         # Shared prompt snippets
│   └── settings.yaml      # Optional YAML config
├── runner/
│   ├── run.py             # CLI entrypoint
│   ├── pipeline.py        # Pipeline orchestration
│   ├── state.py           # State schema (Pydantic)
│   ├── artifacts.py       # Artifact management
│   ├── db.py              # DuckDB operations
│   ├── llm.py             # Provider abstraction (OpenAI + Anthropic)
│   └── utils.py           # Utilities, SHA256 hashing
├── charters/
│   ├── orchestrator.md    # Orchestrator charter
│   ├── reporting.md       # Report generation charter
│   ├── intake.md          # Legacy intake form charter
│   ├── intake_conversation.md  # Conversational intake charter (primary)
│   ├── agents/            # 9 specialized agent charters (01-09)
│   │   └── 09_financial_data.md  # Data layer subagent (Dexter-inspired)
│   └── cove/              # CoVe verification agents
├── skills/
│   ├── plotting.py        # Publication-quality charts
│   ├── conflicts.py       # Conflict detection
│   ├── output_validation.py
│   ├── summarization.py
│   └── document_ingestion.py
├── schemas/
│   ├── agent_outputs.py   # Per-agent Pydantic models
│   └── intake_session.py  # Intake session, document, and task schemas
├── notebooks/             # Development & validation notebooks
├── inputs/
│   ├── task_template.md
│   ├── intake_template.md
│   └── example_tasks/
└── data/
    ├── runs/<run_id>/     # Per-run artifacts (outside Dropbox!)
    ├── intakes/<intake_id>/  # Intake session storage
    │   ├── transcript.jsonl  # Conversation history
    │   ├── session_meta.json # Session state and metadata
    │   ├── task.md           # Generated task file
    │   ├── intake_summary.md # Key conversation highlights
    │   └── reference_materials/  # User-provided documents
    │       ├── originals/    # Original uploaded files
    │       ├── processed/    # Extracted/converted versions
    │       └── manifest.json # Document inventory
    └── ledger.duckdb      # Audit ledger
```

## Execution Flow (per run)

```
                    ┌─────────────────────────────────────┐
                    │         ENTRY OPTIONS               │
                    ├─────────────────────────────────────┤
                    │  Option A: Direct Task File         │
                    │  python -m runner.run --task X.md   │
                    │                                     │
                    │  Option B: Conversational Intake    │
                    │  claude → /intake                   │
                    │  (multi-turn conversation)          │
                    │  → generates task.md + ref_materials│
                    │  python -m runner.run --intake ID   │
                    └─────────────────────────────────────┘
                                    │
                                    ▼
USER INPUT (task.md + reference_materials/)
        │
        ▼
   ORCHESTRATOR
   - Normalizes input
   - Selects relevant agents
        │
        ▼
   PARALLEL PASS
   - Strategic Agents (01-04)
   - Screener (06) if equity task ──────┐
   - Epistemic (05)                     │
        │                               │
        ▼                               ▼
   ORCHESTRATOR SYNTHESIS          09_FINANCIAL_DATA
   - Conflict resolution           (Data Layer Subagent)
   - Ticker shortlist (if equity)  - Live market data
        │                          - Financial statements
        ▼                          - SEC filings
   SEQUENTIAL DEEP-DIVE            - Analyst estimates
   - Fundamental (07) ─────────────────┤
   - Technical (08) ───────────────────┤
   - Inversion (02) + Epistemic (05)   │
        │                               │
        ▼                               │
   COVE VERIFICATION ──────────────────┘
   - Verifier delegates to 09 for data
        │
        ▼
   REPORTING AGENT
   - 1-3 page structured memo
   - Amazon 6-pager style
        │
        ▼
   OUTPUTS
   - data/runs/<run_id>/
   - DuckDB ledger entry
   - Final memo with ranked recommendations
```

**Data Layer Note:** 09_financial_data is not directly invoked by the Orchestrator. Instead, agents 06, 07, 08, and CoVe_verifier delegate to it when they need live market data. This ensures data accuracy, source attribution, and efficient API usage through caching.

## Data and Storage Details

**CRITICAL:** Follow `DATA_ROOT` convention from master CLAUDE.md:
- **Windows:** `D:\vscode\data\TheFarm\`
- **Linux/AWS:** `/data/TheFarm/`
- **Fallback:** `./data/`

**DuckDB Tables:**
- `runs` - Run metadata
- `steps` - Pipeline step tracking
- `agent_calls` - LLM call logs with tokens/cost
- `state_snapshots` - State checkpoints
- `artifacts` - File hashes and paths

## External Integrations

### LLM Providers (Required)
- **Anthropic:** Claude Opus 4.5 (complex reasoning), Sonnet 4 (structured tasks)
- **OpenAI:** GPT-4o (fallback)

### Market Data (Phase 3)
- Polygon.io (primary market data)
- Schwab API (OAuth for live data)

### Web Search (Phase 3)
- Brave Search (primary)
- Serper.dev (secondary)
- SerpAPI (tertiary)

## Deployment and Operations

**Local Setup:**
```bash
python -m pip install -r requirements.txt
cp .env.example .env  # Add API keys
python -m runner.run --task inputs/example_tasks/ai_gpu_optics.md
```

**CLI Options (Pipeline):**
```bash
--task PATH           # Path to task file (direct mode)
--intake <intake_id>  # Run from intake session (loads task.md + ref_materials)
--run-id ID           # Optional: custom run ID
--max-iterations N    # Default: 2
--parallel-only       # Debug: stop after parallel pass
--resume <run_id>     # Resume from checkpoint
--no-db               # Skip database logging
```

**CLI Options (Intake via Claude Code):**
```bash
claude                # Start Claude Code
> /intake             # Begin new intake conversation
> /intake --resume <intake_id>   # Resume previous session
> /intake --list      # List all intake sessions
```

**Environment Variables (Required):**
- `ANTHROPIC_API_KEY` - Anthropic API key
- `OPENAI_API_KEY` - OpenAI API key
- `DUCKDB_PATH` - Default: `data/ledger.duckdb`

## Known Gaps and Watchouts

- **CoVe (Chain of Verification)** agents are defined but integration may be incomplete
- **09_financial_data** charter is defined; API integration (FMP/Polygon.io) pending implementation
- Web search integration (Phase 3) not yet implemented
- Keep README in sync with the actual package layout after changes
- Extended thinking mode uses significant tokens—monitor costs
- Per-ticker iteration can multiply agent calls rapidly
- 09_financial_data API calls should be cached within a run to avoid duplicate requests

## Tips for Future Contributors

- Read agent charters in `charters/agents/` before modifying agent behavior
- The Orchestrator is the brain—changes there affect the entire pipeline
- Each run creates artifacts in `data/runs/<run_id>/`—check these for debugging
- Use `--parallel-only` to test individual agents without full pipeline
- Validation notebooks in `notebooks/` are the source of truth for expected behavior
- Update `AGENT_CHANGELOG.md` after each session with checkbox format (completed vs. `⧗` in-progress)
