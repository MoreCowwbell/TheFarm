# Project Context

## Project Goal Summary

**deepmind1 (TheFarm)** is an automated multi-agent diligence workflow system that uses LLM-based agents orchestrated through a structured pipeline to perform investment analysis, strategic decision-making, and research tasks.

**Core Value Proposition:** Transform unstructured research questions into rigorous, auditable, multi-perspective analyses with clear recommendations and documented reasoning chains.

## Current Capabilities

The system employs **8 specialized agents** organized into three categories:

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

### Meta Agents (05)
| Agent | Primary Focus | Key Outputs |
|-------|---------------|-------------|
| **05 Epistemic Reality Check** | Knowledge vs assumptions, confidence calibration | Know/assume/speculate table, overconfidence flags |

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
│   ├── intake.md          # Intake Agent charter
│   ├── agents/            # 8 specialized agent charters (01-08)
│   └── cove/              # CoVe verification agents
├── skills/
│   ├── plotting.py        # Publication-quality charts
│   ├── conflicts.py       # Conflict detection
│   ├── output_validation.py
│   ├── summarization.py
│   └── document_ingestion.py
├── schemas/
│   └── agent_outputs.py   # Per-agent Pydantic models
├── notebooks/             # Development & validation notebooks
├── inputs/
│   ├── task_template.md
│   ├── intake_template.md
│   └── example_tasks/
└── data/
    ├── runs/<run_id>/     # Per-run artifacts (outside Dropbox!)
    └── ledger.duckdb      # Audit ledger
```

## Execution Flow (per run)

```
USER INPUT (task_template.md)
        │
        ▼
   ORCHESTRATOR
   - Normalizes input
   - Selects relevant agents
        │
        ▼
   PARALLEL PASS
   - Strategic Agents (01-04)
   - Screener (06) if equity task
   - Epistemic (05)
        │
        ▼
   ORCHESTRATOR SYNTHESIS
   - Conflict resolution
   - Ticker shortlist (if equity)
        │
        ▼
   SEQUENTIAL DEEP-DIVE
   - Per-ticker: Fundamental (07) + Technical (08)
   - Inversion (02) + Epistemic (05) follow-up
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

**CLI Options:**
```bash
--task PATH           # Required: path to task file
--run-id ID           # Optional: custom run ID
--max-iterations N    # Default: 2
--parallel-only       # Debug: stop after parallel pass
--resume <run_id>     # Resume from checkpoint
--no-db               # Skip database logging
```

**Environment Variables (Required):**
- `ANTHROPIC_API_KEY` - Anthropic API key
- `OPENAI_API_KEY` - OpenAI API key
- `DUCKDB_PATH` - Default: `data/ledger.duckdb`

## Known Gaps and Watchouts

- **CoVe (Chain of Verification)** agents are defined but integration may be incomplete
- Market data providers (Phase 3) not yet implemented
- Web search integration (Phase 3) not yet implemented
- Keep README in sync with the actual package layout after changes
- Extended thinking mode uses significant tokens—monitor costs
- Per-ticker iteration can multiply agent calls rapidly

## Tips for Future Contributors

- Read agent charters in `charters/agents/` before modifying agent behavior
- The Orchestrator is the brain—changes there affect the entire pipeline
- Each run creates artifacts in `data/runs/<run_id>/`—check these for debugging
- Use `--parallel-only` to test individual agents without full pipeline
- Validation notebooks in `notebooks/` are the source of truth for expected behavior
- Update `AGENT_CHANGELOG.md` after each session with checkbox format (completed vs. `⧗` in-progress)
