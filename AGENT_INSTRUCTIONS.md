# Agent Instructions for This Repository
> This file serves as the project-specific CLAUDE.md equivalent. See also: AGENT_CONTEXT.md

## Mission and Starting Point
- Always read `AGENT_CONTEXT.md` before coding—it contains the agent architecture, execution flow, and directory layout.
- This is **deepmind1**, a multi-agent diligence system. Understand which component (runner, skills, charters, schemas) you're working in before making changes.

## How to Assist Effectively
- The Orchestrator (`runner/orchestrator.py` + `charters/orchestrator.md`) is the brain of the system. Changes there affect the entire pipeline—proceed carefully.
- Agent charters in `charters/agents/` define behavior. Modify charters for prompt changes; modify `runner/` for execution logic changes.
- When modifying code, state **what changed**, **why**, and **what follow-up work** remains.
- Use validation notebooks in `notebooks/` to verify changes don't break expected behavior.

## Code Style, Layout, and Dependencies
- Target Python 3.11+. Use explicit imports and type hints.
- Use Pydantic models for structured data (see `schemas/` and `runner/state.py`).
- Key dependencies: `duckdb`, `anthropic`, `openai`, `pydantic`, `python-dotenv`, `matplotlib`, `plotly`
- Keep `requirements.txt` aligned with actual imports.

## Database Rules

**DuckDB is the audit ledger.** Every run creates entries in:
- `runs` - Run metadata (run_id, task, timestamps)
- `steps` - Pipeline step tracking
- `agent_calls` - LLM call logs with tokens, cost, duration
- `state_snapshots` - Checkpoint state for resume capability
- `artifacts` - File hashes (SHA256) and paths

**Critical Rules:**
1. Follow `DATA_ROOT` convention (see master CLAUDE.md): `D:\vscode\data\TheFarm\` on Windows, `/data/TheFarm/` on Linux
2. Never hardcode database paths—use `config/config.py` helpers
3. All artifacts get SHA256 hashed and registered in the `artifacts` table
4. Use parameterized queries, never string concatenation

**Example DB operations:**
```python
from runner.db import get_db
db = get_db()
db.execute("INSERT INTO runs (run_id, task_path) VALUES (?, ?)", [run_id, task_path])
```

## Analytics, Plotting, and Alerts

**Plotting module:** `skills/plotting.py`
- Use Plotly for interactive HTML charts, Matplotlib for static PNGs
- All charts saved to `data/runs/<run_id>/charts/`
- Required chart types: valuation comparison (horizontal bar), price charts (candlestick), financial trends (multi-line), scenario waterfalls

**Chart Quality Checklist:**
| Criterion | Requirement |
|-----------|-------------|
| Titles | Descriptive, includes time period |
| Axes | Labeled with units, appropriate scale |
| Legend | Clear, not overlapping data |
| Colors | Colorblind-safe palette |
| Resolution | PNG at 2x scale for print quality |

**Report Quality Gate:** (`skills/report_quality.py`)
- All reports must pass automated checks before being marked "shippable"
- Required sections: Executive Summary, Investment Thesis, Analysis Summary, Recommendation Framework

## Testing, Validation, and Logging
- Validation notebooks in `notebooks/` are the source of truth
- Run validation checkpoints before marking phases complete:
  ```bash
  python -c "import duckdb; db=duckdb.connect('data/ledger.duckdb'); print(db.execute('SHOW TABLES').fetchall())"
  ```
- Keep console logging informative (`logging` module) for debugging pipeline failures
- Each agent call should log: agent name, model used, token count, duration, cost estimate

## Documentation and Runbooks
- Keep `README.md` synchronized with CLI usage, configuration requirements, and deployment steps
- Document new env vars in both `README.md` and `.env.example`
- Agent charter changes should be noted in `AGENT_CHANGELOG.md`

## AGENT_CHANGELOG Expectations
- After each work session, append a dated section to `AGENT_CHANGELOG.md`
- Use checkboxes `[x]` for completed tasks
- Use `⧗` prefix for in-progress tasks that should be resumed
- Keep entries concise; archive older blocks periodically

## Output Rules: Snippets vs. Full Files
- Default to returning only the modified snippet when the change is localized
- Return the entire file when edits touch multiple sections or when global context is critical
- When uncertain, provide the snippet and ask if the user needs the full file

## Environment and Safety
- Required env vars: `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`
- Optional: `POLYGON_API_KEY`, `BRAVE_SEARCH_API_KEY`, Schwab OAuth credentials
- Never commit `.env` files or API keys
- Use `MAX_COST_PER_RUN_USD` to prevent runaway costs

## Model Configuration

**Model assignment per agent:**
| Agent | Model | Thinking Mode | Rationale |
|-------|-------|---------------|-----------|
| Orchestrator | Opus 4.5 | Extended | Complex synthesis, conflict resolution |
| 01 Systems | Opus 4.5 | Extended | Causal chain reasoning |
| 02 Inversion | Opus 4.5 | Extended | Failure mode exploration |
| 03 Allocator | Sonnet 4 | Standard | Structured quantitative analysis |
| 04 Incentives | Sonnet 4 | Standard | Pattern-based mapping |
| 05 Epistemic | Opus 4.5 | Extended | Metacognitive reflection |
| 06 Screener | Sonnet 4 | Standard | Structured search |
| 07 Fundamental | Opus 4.5 | Extended | Complex valuation reasoning |
| 08 Technical | Sonnet 4 | Standard | Rule-based pattern recognition |
| Reporting | Sonnet 4 | Standard | Narrative synthesis from existing content |

## PATH and Directories
- Always use relative paths whenever possible
- Run artifacts go to `data/runs/<run_id>/`
- Charters are in `charters/` (agents in `charters/agents/`)
- Use `inputs/example_tasks/` for test runs

## CLI Quick Reference
```bash
# Basic run
python -m runner.run --task inputs/example_tasks/ai_gpu_optics.md

# Debug modes
python -m runner.run --task PATH --parallel-only      # Stop after parallel pass
python -m runner.run --task PATH --max-agents 1       # Single agent test
python -m runner.run --resume <run_id>                # Resume from checkpoint
```
