# deepmind1: Multi-Agent Diligence System — Final Project Plan

## Executive Summary

This document provides a refined, actionable project plan for building **deepmind1**, an automated multi-agent diligence workflow system. The system uses LLM-based agents orchestrated through a structured pipeline to perform investment analysis, strategic decision-making, and research tasks.

**Core Value Proposition:** Transform unstructured research questions into rigorous, auditable, multi-perspective analyses with clear recommendations and documented reasoning chains.

---

## 1. Project Understanding & Analysis

### 1.1 System Overview

deepmind1 is a **prompt-orchestrated multi-agent system** that:
- Ingests structured or free-form research tasks
- Executes parallel analysis through 8 specialized reasoning agents
- Synthesizes findings through an orchestrator
- Performs sequential deep-dives based on initial findings (including equity research)
- Produces auditable, human-readable reports with full provenance

### 1.2 Agent Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INPUT                               │
│                    (task_template.md)                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       ORCHESTRATOR                              │
│   - Normalizes input                                            │
│   - Routes to agents (selects relevant subset)                  │
│   - Synthesizes findings                                        │
│   - Plans sequential deep-dives                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
     ┌────────────────────────┼────────────────────────┐
     │                        │                        │
     ▼                        ▼                        ▼
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│   PARALLEL   │       │   PARALLEL   │       │   PARALLEL   │
│    PASS      │       │    PASS      │       │    PASS      │
│              │       │              │       │              │
│ Strategic    │       │ Equity       │       │ Meta         │
│ Agents       │       │ Research     │       │ Agents       │
│ (01-04)      │       │ (06-08)      │       │ (05)         │
└──────────────┘       └──────────────┘       └──────────────┘
     │                        │                        │
     └────────────────────────┼────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR SYNTHESIS                       │
│   - Conflict resolution, priority ranking                       │
│   - Ticker shortlist from Screener → route to Fundamental/Tech  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    SEQUENTIAL DEEP-DIVE                         │
│   - Targeted follow-up by selected agents                       │
│   - Per-ticker fundamental & technical analysis                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     REPORTING AGENT                             │
│              (1-3 page structured memo)                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        OUTPUTS                                  │
│   - data/runs/<run_id>/                                        │
│   - DuckDB ledger                                               │
│   - Final memo with ranked tickers & analysis                   │
└─────────────────────────────────────────────────────────────────┘
```

### 1.3 Core Agents

The system employs 8 specialized agents organized into three categories:

#### Strategic Reasoning Agents (01-04)

| Agent | Primary Focus | Key Outputs |
|-------|---------------|-------------|
| **01 Systems & Second-Order** | System dynamics, feedback loops, value migration | System map, second-order effects, bottlenecks |
| **02 Inversion Thinking** | Failure modes, fragility, downside scenarios | Kill criteria, fragility analysis, mitigations |
| **03 Capital Allocation** | Opportunity cost, portfolio fit, alternatives | Best alternatives, decision thresholds, required returns |
| **04 Incentives & Timing** | Stakeholder incentives, market timing, power dynamics | Incentive map, timing indicators, value capture analysis |

#### Equity Research Agents (06-08)

| Agent | Primary Focus | Key Outputs |
|-------|---------------|-------------|
| **06 Sector Screener** | Ticker identification, competitive landscape, universe building | List of relevant tickers, market cap tiers, pure-play vs diversified classification, sector positioning |
| **07 Fundamental Analyst** | Valuation, financial statements, earnings quality | P/E, EV/EBITDA, DCF range, balance sheet risks, earnings quality score, capital structure analysis |
| **08 Technical Analyst** | Price action, chart patterns, momentum indicators | Trend direction, support/resistance levels, volume analysis, RSI/MACD signals, entry/exit zones |

#### Meta Agents (05)

| Agent | Primary Focus | Key Outputs |
|-------|---------------|-------------|
| **05 Epistemic Reality Check** | Knowledge vs assumptions, confidence calibration | Know/assume/speculate table, overconfidence flags, data quality assessment |

### 1.4 Equity Research Workflow

When tasks involve stock/investment analysis, the system follows a specialized workflow:

```
┌─────────────────────────────────────────────────────────────────┐
│  TASK: "Diligence on rare earth mineral investment"            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PARALLEL PASS #1                             │
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │ 01 Systems  │  │ 06 Screener │  │ 04 Incent.  │             │
│  │             │  │             │  │             │             │
│  │ Value chain │  │ Find tickers│  │ China/govt  │             │
│  │ dynamics    │  │ MP, LTHM,   │  │ incentives  │             │
│  │             │  │ ALB, SGML...│  │             │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                 ORCHESTRATOR SYNTHESIS                          │
│                                                                 │
│  "Screener found 8 tickers. Shortlist top 4 by relevance:      │
│   MP Materials, Lynas, Albemarle, Sigma Lithium"               │
│                                                                 │
│  "Route to Fundamental + Technical for deep-dive"               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   SEQUENTIAL DEEP-DIVE                          │
│                                                                 │
│  FOR EACH ticker IN [MP, LTHM, ALB, SGML]:                     │
│    ├── 07 Fundamental → Valuation, financials, earnings        │
│    └── 08 Technical   → Chart analysis, entry/exit levels      │
│                                                                 │
│  THEN:                                                          │
│    └── 02 Inversion   → "What kills the rare earth thesis?"    │
│    └── 05 Epistemic   → Confidence check on all assumptions    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    REPORTING AGENT                              │
│                                                                 │
│  Final memo includes:                                           │
│  - Sector overview & thesis                                     │
│  - Ranked ticker recommendations                                │
│  - Per-ticker: valuation summary, technical levels, risks       │
│  - Kill criteria & assumption audit                             │
└─────────────────────────────────────────────────────────────────┘
```

#### Agent Output Examples

**06 Sector Screener Output:**
```markdown
## Rare Earth / Critical Minerals Universe

### Pure-Play Exposure
| Ticker | Company | Mkt Cap | Focus | Notes |
|--------|---------|---------|-------|-------|
| MP | MP Materials | $4.2B | Rare earth | Only US rare earth miner |
| LTHM | Livent | $3.1B | Lithium | Spin-off from FMC |

### Diversified Exposure
| Ticker | Company | Mkt Cap | RE Revenue % | Notes |
|--------|---------|---------|--------------|-------|
| ALB | Albemarle | $15B | ~30% | Lithium + bromine |

### Excluded (with reason)
- VALE: Too diversified, <5% rare earth exposure
- RIO: Minimal direct exposure
```

**07 Fundamental Analyst Output:**
```markdown
## MP Materials (MP) - Fundamental Analysis

### Valuation Summary
| Metric | Value | Sector Avg | Assessment |
|--------|-------|------------|------------|
| P/E (FWD) | 28.4x | 22.1x | Premium |
| EV/EBITDA | 14.2x | 11.8x | Slight premium |
| P/B | 3.1x | 2.4x | Premium |

### DCF Range: $18 - $32 (current: $24)

### Earnings Quality
- Revenue recognition: Clean
- Accruals ratio: 0.04 (healthy)
- Insider transactions: Net buying last 6mo

### Balance Sheet Risks
- Debt/Equity: 0.3x (low)
- Current ratio: 2.1x (healthy)
- CapEx commitments: $200M expansion (funded)

### Key Assumptions Flagged
- [ASSUMPTION] China export restrictions continue
- [ASSUMPTION] EV adoption rate per IEA forecasts
```

**08 Technical Analyst Output:**
```markdown
## MP Materials (MP) - Technical Analysis

### Trend Assessment
- Primary trend: UPTREND (above 200 DMA)
- Secondary trend: Consolidation (40-day range)

### Key Levels
| Level | Price | Significance |
|-------|-------|--------------|
| Resistance 1 | $28.50 | 52-week high |
| Resistance 2 | $32.00 | 2022 high |
| Support 1 | $21.80 | 50 DMA |
| Support 2 | $18.50 | 200 DMA |

### Momentum Indicators
- RSI (14): 54 (neutral)
- MACD: Bullish crossover 3 days ago
- Volume: Below average, awaiting catalyst

### Entry/Exit Zones
- Accumulation zone: $20-22
- Take profit zone: $28-30
- Stop loss: Below $18 (break of 200 DMA)
```

### 1.5 Key Design Principles

1. **Separation of Concerns:** Reasoning agents decide *what matters*; skills generate *truthful artifacts*; reporting tells *coherent stories from verified outputs*
2. **Auditability:** Every decision has a traceable provenance chain with hashes and timestamps
3. **Reproducibility:** Charter hashes, input/output hashes, and state snapshots enable exact reproduction
4. **No Hallucinated Evidence:** Agents cannot invent figures, data, or citations
5. **Graceful Degradation:** System runs with minimal input; assumptions are explicit and confidence-tagged

---

## 2. Identified Improvements & Recommendations

### 2.1 Structural Improvements

| Issue | Original State | Recommended Improvement |
|-------|----------------|------------------------|
| **MVP Definition** | All features treated equally | Clear Phase 1 MVP vs Phase 2 enhancements |
| **Dependency Mapping** | Implicit dependencies | Explicit dependency graph for build order |
| **Error Recovery** | Basic retry logic | Comprehensive error taxonomy with recovery strategies |
| **Cost Management** | Not addressed | Token budgets, cost tracking, provider fallback |

### 2.2 Technical Improvements

#### 2.2.1 Rate Limiting & Cost Control
```python
# Add to config/config.py
RATE_LIMITS = {
    "openai": {"rpm": 60, "tpm": 90000},
    "anthropic": {"rpm": 50, "tpm": 100000}
}

MAX_COST_PER_RUN_USD = 5.00
TOKEN_BUDGET_PER_AGENT = 4000
```

#### 2.2.2 Enhanced Error Handling
```python
# Error taxonomy for runner/utils.py
class ErrorCategory(Enum):
    TRANSIENT_NETWORK = "transient_network"      # Retry with backoff
    RATE_LIMITED = "rate_limited"                # Exponential backoff
    PROVIDER_ERROR = "provider_error"            # Fallback to alternate
    INVALID_OUTPUT = "invalid_output"            # Re-prompt with guidance
    BUDGET_EXCEEDED = "budget_exceeded"          # Graceful termination
    CHARTER_VIOLATION = "charter_violation"      # Log and continue
```

#### 2.2.3 Output Validation
Add schema validation for agent outputs:
```python
# Add to skills/extractors.py
def validate_agent_output(agent_name: str, output: str) -> ValidationResult:
    """Validate that output contains required sections per charter."""
    required_sections = CHARTER_REQUIREMENTS[agent_name]
    found_sections = extract_markdown_headers(output)
    missing = required_sections - found_sections
    return ValidationResult(valid=len(missing)==0, missing=missing)
```

### 2.3 Operational Improvements

#### 2.3.1 Monitoring & Observability
Add structured logging with run context:
```python
# runner/utils.py
import structlog

logger = structlog.get_logger()

def log_agent_call(run_id, agent_name, status, tokens_used, cost_usd):
    logger.info("agent_call",
        run_id=run_id,
        agent=agent_name,
        status=status,
        tokens=tokens_used,
        cost_usd=cost_usd
    )
```

#### 2.3.2 Health Checks
Add pre-flight validation:
```python
# runner/run.py
def preflight_checks() -> List[str]:
    """Run before pipeline execution."""
    issues = []
    if not os.getenv("OPENAI_API_KEY") and not os.getenv("ANTHROPIC_API_KEY"):
        issues.append("No API keys configured")
    if not Path("charters").exists():
        issues.append("Charters directory missing")
    # ... additional checks
    return issues
```

### 2.4 Security Improvements

1. **Secrets Scanning:** Add pre-commit hook to detect secrets
2. **Input Sanitization:** Validate task inputs before processing
3. **Output Redaction:** Optionally redact sensitive data from logs
4. **API Key Rotation:** Document key rotation procedures

### 2.5 Testing Strategy Enhancement

| Test Type | Coverage Target | Implementation |
|-----------|----------------|----------------|
| Unit Tests | 80% of skills layer | pytest, Phase 2 |
| Integration Tests | Full pipeline paths | pytest-asyncio |
| Contract Tests | Agent output schemas | JSON Schema validation |
| Regression Tests | Charter adherence | Golden file comparison |
| Cost Tests | Budget enforcement | Mock provider responses |

### 2.6 LLM Provider & Model Strategy

#### 2.6.1 Provider Priority

**Primary Provider:** Anthropic (Claude)
**Fallback Provider:** OpenAI (GPT-4o)

Rationale for Claude-first approach:
- Consistent reasoning patterns across agents
- Strong performance on complex multi-step analysis
- Reliable structured output adherence
- Single pricing model for cost predictability
- Easier prompt tuning and debugging

```python
# config/models.py
PROVIDER_PRIORITY = ["anthropic", "openai"]  # Primary, then fallback

FALLBACK_TRIGGERS = [
    "rate_limited",
    "provider_unavailable",
    "timeout",
    "5xx_error",
]
```

#### 2.6.2 Model Tiering by Agent

Start with best-performing configuration, optimize for cost later based on token usage data.

**Strategic Reasoning Agents:**

| Agent | Model | Thinking Mode | Max Thinking Tokens | Rationale |
|-------|-------|---------------|---------------------|-----------|
| **Orchestrator** | Opus 4.5 | Extended | 10,000 | Synthesis across 8 agents, conflict resolution, planning |
| **01 Systems** | Opus 4.5 | Extended | 8,000 | Second-order effects require deep reasoning chains |
| **02 Inversion** | Opus 4.5 | Extended | 8,000 | Must find non-obvious failure modes |
| **03 Allocator** | Sonnet 4 | Standard | — | More structured/quantitative analysis |
| **04 Incentives** | Sonnet 4 | Standard | — | Pattern matching, less novel reasoning |
| **05 Epistemic** | Opus 4.5 | Extended | 10,000 | Meta-reasoning, catching what others missed |

**Equity Research Agents:**

| Agent | Model | Thinking Mode | Max Thinking Tokens | Rationale |
|-------|-------|---------------|---------------------|-----------|
| **06 Screener** | Sonnet 4 | Standard | — | Structured search, universe building |
| **07 Fundamental** | Opus 4.5 | Extended | 8,000 | Complex valuation reasoning, connecting financial dots |
| **08 Technical** | Sonnet 4 | Standard | — | Pattern recognition, rule-based analysis |

**Support Agents:**

| Agent | Model | Thinking Mode | Max Thinking Tokens | Rationale |
|-------|-------|---------------|---------------------|-----------|
| **Reporting** | Sonnet 4 | Standard | — | Summarization and formatting |

#### 2.6.3 Extended Thinking Rationale

Extended thinking mode provides value for agents that must:
- Weigh conflicting information (Orchestrator)
- Explore non-obvious failure paths (Inversion)
- Trace complex causal chains (Systems)
- Reflect on reasoning quality (Epistemic)

Standard mode is sufficient for:
- Structured quantitative analysis (Allocator)
- Pattern-based incentive mapping (Incentives)
- Report assembly from existing content (Reporting)

#### 2.6.4 Per-Agent Configuration

```python
# config/models.py
from enum import Enum
from typing import Optional
from pydantic import BaseModel

class ThinkingMode(str, Enum):
    STANDARD = "standard"
    EXTENDED = "extended"

class AgentModelConfig(BaseModel):
    provider: str = "anthropic"
    model: str
    thinking: ThinkingMode = ThinkingMode.STANDARD
    max_thinking_tokens: Optional[int] = None
    temperature: float = 0.7
    max_output_tokens: int = 4096

AGENT_MODEL_CONFIG: dict[str, AgentModelConfig] = {
    # Orchestrator
    "orchestrator": AgentModelConfig(
        model="claude-opus-4-5-20250514",
        thinking=ThinkingMode.EXTENDED,
        max_thinking_tokens=10000,
    ),
    # Strategic Reasoning Agents (01-04)
    "01_systems": AgentModelConfig(
        model="claude-opus-4-5-20250514",
        thinking=ThinkingMode.EXTENDED,
        max_thinking_tokens=8000,
    ),
    "02_inversion": AgentModelConfig(
        model="claude-opus-4-5-20250514",
        thinking=ThinkingMode.EXTENDED,
        max_thinking_tokens=8000,
    ),
    "03_allocator": AgentModelConfig(
        model="claude-sonnet-4-20250514",
        thinking=ThinkingMode.STANDARD,
    ),
    "04_incentives": AgentModelConfig(
        model="claude-sonnet-4-20250514",
        thinking=ThinkingMode.STANDARD,
    ),
    # Meta Agent (05)
    "05_epistemic": AgentModelConfig(
        model="claude-opus-4-5-20250514",
        thinking=ThinkingMode.EXTENDED,
        max_thinking_tokens=10000,
    ),
    # Equity Research Agents (06-08)
    "06_screener": AgentModelConfig(
        model="claude-sonnet-4-20250514",
        thinking=ThinkingMode.STANDARD,
    ),
    "07_fundamental": AgentModelConfig(
        model="claude-opus-4-5-20250514",
        thinking=ThinkingMode.EXTENDED,
        max_thinking_tokens=8000,
    ),
    "08_technical": AgentModelConfig(
        model="claude-sonnet-4-20250514",
        thinking=ThinkingMode.STANDARD,
    ),
    # Support Agent
    "reporting": AgentModelConfig(
        model="claude-sonnet-4-20250514",
        thinking=ThinkingMode.STANDARD,
    ),
}

# Fallback configuration for all agents
FALLBACK_CONFIG = AgentModelConfig(
    provider="openai",
    model="gpt-4o",
    thinking=ThinkingMode.STANDARD,
)
```

#### 2.6.5 Environment Overrides

Allow per-agent model overrides via environment variables for testing and cost optimization:

```bash
# .env overrides (optional)
AGENT_ORCHESTRATOR_MODEL=claude-sonnet-4-20250514
AGENT_01_SYSTEMS_MODEL=claude-haiku-3-5-20241022
AGENT_05_EPISTEMIC_THINKING=standard
```

```python
# config/models.py - environment override logic
import os

def get_agent_config(agent_name: str) -> AgentModelConfig:
    """Get config with environment overrides."""
    base_config = AGENT_MODEL_CONFIG.get(agent_name, FALLBACK_CONFIG)

    # Check for env overrides
    env_prefix = f"AGENT_{agent_name.upper()}"
    if model_override := os.getenv(f"{env_prefix}_MODEL"):
        base_config = base_config.model_copy(update={"model": model_override})
    if thinking_override := os.getenv(f"{env_prefix}_THINKING"):
        base_config = base_config.model_copy(
            update={"thinking": ThinkingMode(thinking_override)}
        )

    return base_config
```

#### 2.6.6 Cost Optimization Path

1. **Phase 1:** Start with Opus 4.5 + Extended Thinking for complex agents
2. **Monitor:** Track token usage per agent via `cost_tracking` table
3. **Analyze:** Identify agents with highest burn rates
4. **Test:** A/B test Sonnet vs Opus on high-burn agents
5. **Downgrade:** Only switch to cheaper models when quality is validated

```python
# Example: Query to identify optimization candidates
SELECT
    agent_name,
    SUM(tokens_in + tokens_out) as total_tokens,
    SUM(cost_usd) as total_cost,
    AVG(cost_usd) as avg_cost_per_call
FROM cost_tracking
GROUP BY agent_name
ORDER BY total_cost DESC;
```

---

## 3. Refined Phase Plan

### Phase 1: Foundation (MVP)

#### Phase 1A: Project Scaffold & Infrastructure
**Duration:** Foundation sprint
**Dependencies:** None

**Deliverables:**
- [ ] Directory structure per specification
- [ ] `pyproject.toml` with dependencies
- [ ] `.env.example` with all required variables
- [ ] `.gitignore` (comprehensive)
- [ ] DuckDB schema creation script
- [ ] Basic configuration system

**Validation Checkpoint:**
```bash
# Must pass before proceeding
python -c "import duckdb; db=duckdb.connect('data/ledger.duckdb'); print(db.execute('SHOW TABLES').fetchall())"
# Expected: runs, steps, agent_calls, state_snapshots, artifacts
```

#### Phase 1B: Artifact & Hashing System
**Dependencies:** Phase 1A

**Deliverables:**
- [ ] SHA256 hashing utilities
- [ ] Run folder creation (`data/runs/<run_id>/`)
- [ ] Artifact saving with DB registration
- [ ] Charter file hashing on load
- [ ] Notebook: `01_phase1_db_and_artifacts.ipynb`

**Validation Checkpoint:**
```python
# Test artifact round-trip
artifact_id = save_artifact(run_id, "test.md", "# Test")
row = db.execute("SELECT hash FROM artifacts WHERE artifact_id=?", [artifact_id]).fetchone()
assert row[0] == hashlib.sha256("# Test".encode()).hexdigest()
```

#### Phase 1C: Single Agent End-to-End
**Dependencies:** Phase 1B

**Deliverables:**
- [ ] LLM wrapper (`runner/llm.py`) for OpenAI + Anthropic
- [ ] Provider configuration with model mapping
- [ ] Single agent execution with full logging
- [ ] Output parsing and validation
- [ ] Notebook: `02_phase1_single_agent_call.ipynb`

**Validation Checkpoint:**
```bash
python -m runner.run --task inputs/example_tasks/ai_gpu_optics.md --parallel-only --max-agents 1
# Verify: data/runs/<run_id>/01_systems.md exists
# Verify: agent_calls table has 1 row
```

#### Phase 1D: Parallel Pass + Orchestrator Synthesis
**Dependencies:** Phase 1C

**Deliverables:**
- [ ] ThreadPoolExecutor-based parallel execution
- [ ] State snapshot before/after parallel pass
- [ ] Orchestrator synthesis prompt and charter
- [ ] Conflict detection (basic)
- [ ] Sequential plan generation
- [ ] Notebook: `03_phase1_parallel_then_synth.ipynb`

**Validation Checkpoint:**
```bash
python -m runner.run --task inputs/example_tasks/ai_gpu_optics.md --parallel-only
# Verify: 5 agent outputs + orchestrator_synthesis.md
# Verify: state_snapshots table has "post_parallel" entry
```

#### Phase 1E: Full Pipeline with Reporting
**Dependencies:** Phase 1D

**Deliverables:**
- [ ] Sequential deep-dive execution
- [ ] Bounded iteration logic (max 2)
- [ ] Reporting agent integration
- [ ] Final memo generation
- [ ] Run summary CLI output
- [ ] Notebook: `04_phase1_full_pipeline.ipynb`

**Validation Checkpoint:**
```bash
python -m runner.run --task inputs/example_tasks/ai_gpu_optics.md
# Verify: Complete run folder with all outputs
# Verify: final_memo.md exists and follows template
# Verify: All DB tables populated correctly
```

---

### Phase 2: Enhancement & Hardening

#### Phase 2A: Skills Layer
**Dependencies:** Phase 1E

**Deliverables:**
- [ ] Structured extractors (assumptions, questions, conflicts)
- [ ] Automatic state enrichment after each agent
- [ ] Conflict detection and tracking
- [ ] Basic plotting skills (stubs)
- [ ] Notebook: `05_phase2_skills_and_report.ipynb`

#### Phase 2B: Equity Research Agents
**Dependencies:** Phase 2A

**Deliverables:**
- [ ] 06 Sector Screener agent charter and integration
- [ ] 07 Fundamental Analyst agent charter and integration
- [ ] 08 Technical Analyst agent charter and integration
- [ ] Equity research workflow in orchestrator
- [ ] Per-ticker iteration logic in pipeline
- [ ] Notebook: `07_phase2_equity_research.ipynb`

**Validation Checkpoint:**
```bash
python -m runner.run --task inputs/example_tasks/rare_earth_diligence.md
# Verify: 06_screener.md identifies relevant tickers
# Verify: 07_fundamental.md and 08_technical.md generated per shortlisted ticker
# Verify: Final memo includes ranked ticker recommendations
```

#### Phase 2C: Testing & Quality Gates
**Dependencies:** Phase 2B

**Deliverables:**
- [ ] `test_state_schema.py`
- [ ] `test_prompt_hashing.py`
- [ ] `test_duckdb_schema.py`
- [ ] `test_pipeline_smoke.py`
- [ ] `test_equity_workflow.py`
- [ ] `--dry-run` validation mode
- [ ] Notebook: `08_phase2_regression_tests.ipynb`

---

### Phase 3: Market Data Integration

#### Phase 3A: Market Data Skills
**Dependencies:** Phase 2C

**Available Data Providers:**

| Provider | Tier | Capabilities | Use Case |
|----------|------|--------------|----------|
| **Polygon.io** | Advanced (paid) | Real-time quotes, OHLCV history, fundamentals, options, news | Primary source for all market data |
| **Schwab API** | Brokerage | Quotes, research, account data, trading | Secondary source, trading integration |
| **yfinance** | Free | Quotes, history, basic fundamentals | Fallback when paid sources unavailable |

**Provider Priority:**
1. **Polygon.io** (primary) - Best data quality, real-time, comprehensive
2. **Schwab API** (secondary) - Research data, account integration
3. **yfinance** (fallback) - Free tier, no API key required

**Deliverables:**
- [ ] `skills/market_data.py` - Unified API wrapper with provider abstraction
- [ ] Polygon.io integration (real-time quotes, OHLCV, fundamentals)
- [ ] Schwab API integration (research, quotes)
- [ ] yfinance fallback integration
- [ ] Quote fetching: price, volume, market cap, bid/ask
- [ ] Fundamentals fetching: P/E, EV/EBITDA, revenue, earnings, balance sheet
- [ ] Historical price data (1min to daily bars)
- [ ] Options chain data (via Polygon)
- [ ] Rate limiting and caching per provider
- [ ] Provider health checks and automatic failover

**Market Data Skill Interface:**
```python
# skills/market_data.py
from typing import Optional, List
from pydantic import BaseModel
from enum import Enum

class DataProvider(str, Enum):
    POLYGON = "polygon"
    SCHWAB = "schwab"
    YFINANCE = "yfinance"

class QuoteData(BaseModel):
    ticker: str
    price: float
    bid: Optional[float]
    ask: Optional[float]
    market_cap: Optional[float]
    pe_ratio: Optional[float]
    volume: int
    timestamp: str
    source: DataProvider

class FundamentalsData(BaseModel):
    ticker: str
    # Income Statement
    revenue_ttm: Optional[float]
    net_income_ttm: Optional[float]
    eps_ttm: Optional[float]
    gross_margin: Optional[float]
    operating_margin: Optional[float]
    # Valuation
    pe_ratio: Optional[float]
    forward_pe: Optional[float]
    ev_ebitda: Optional[float]
    price_to_book: Optional[float]
    price_to_sales: Optional[float]
    # Balance Sheet
    total_debt: Optional[float]
    total_cash: Optional[float]
    debt_to_equity: Optional[float]
    current_ratio: Optional[float]
    # Metadata
    source: DataProvider
    as_of_date: str

class OHLCVBar(BaseModel):
    timestamp: str
    open: float
    high: float
    low: float
    close: float
    volume: int

class PriceHistory(BaseModel):
    ticker: str
    bars: List[OHLCVBar]
    timeframe: str  # "1min", "5min", "1hour", "1day"
    source: DataProvider

# Provider configuration
PROVIDER_CONFIG = {
    "polygon": {
        "api_key_env": "POLYGON_API_KEY",
        "base_url": "https://api.polygon.io",
        "rate_limit_rpm": 100,  # Advanced tier
        "priority": 1,
    },
    "schwab": {
        "api_key_env": "SCHWAB_API_KEY",
        "client_id_env": "SCHWAB_CLIENT_ID",
        "priority": 2,
    },
    "yfinance": {
        "priority": 3,  # Fallback, no API key needed
    },
}

async def get_quote(ticker: str, provider: Optional[DataProvider] = None) -> QuoteData:
    """Fetch current quote data. Auto-selects best available provider."""
    ...

async def get_fundamentals(ticker: str, provider: Optional[DataProvider] = None) -> FundamentalsData:
    """Fetch fundamental data for a ticker."""
    ...

async def get_price_history(
    ticker: str,
    timeframe: str = "1day",
    period: str = "1y",
    provider: Optional[DataProvider] = None
) -> PriceHistory:
    """Fetch historical price data for technical analysis."""
    ...

async def get_options_chain(ticker: str, expiration: Optional[str] = None) -> dict:
    """Fetch options chain (Polygon only)."""
    ...

async def validate_ticker(ticker: str) -> bool:
    """Check if ticker exists and is tradeable."""
    ...
```

**Polygon.io Specific Features:**
```python
# skills/polygon_client.py
from polygon import RESTClient

class PolygonMarketData:
    def __init__(self, api_key: str):
        self.client = RESTClient(api_key)

    async def get_ticker_details(self, ticker: str) -> dict:
        """Company info, description, SIC code, etc."""
        return self.client.get_ticker_details(ticker)

    async def get_financials(self, ticker: str, limit: int = 4) -> List[dict]:
        """Quarterly/annual financials from SEC filings."""
        return list(self.client.vx.list_stock_financials(ticker, limit=limit))

    async def get_aggregates(
        self,
        ticker: str,
        multiplier: int,
        timespan: str,  # minute, hour, day, week, month
        from_date: str,
        to_date: str
    ) -> List[OHLCVBar]:
        """Historical OHLCV bars."""
        aggs = self.client.get_aggs(ticker, multiplier, timespan, from_date, to_date)
        return [OHLCVBar(...) for a in aggs]

    async def get_last_quote(self, ticker: str) -> QuoteData:
        """Real-time last quote."""
        return self.client.get_last_quote(ticker)

    async def get_related_companies(self, ticker: str) -> List[str]:
        """Find similar/related tickers for screening."""
        return self.client.get_related_companies(ticker)
```

**Schwab API Features:**
```python
# skills/schwab_client.py
class SchwabMarketData:
    """Schwab API for quotes, research, and account integration."""

    async def get_quote(self, ticker: str) -> QuoteData:
        """Real-time quote from Schwab."""
        ...

    async def get_research(self, ticker: str) -> dict:
        """Analyst ratings, price targets, research reports."""
        ...

    async def get_account_positions(self) -> List[dict]:
        """Current portfolio positions (for context in analysis)."""
        ...
```

#### Phase 3B: Enhanced Equity Agents
**Dependencies:** Phase 3A

**Deliverables:**
- [ ] Fundamental Analyst uses Polygon financials + Schwab research
- [ ] Technical Analyst uses Polygon OHLCV for real chart analysis
- [ ] Screener validates tickers via Polygon and fetches basic data
- [ ] Data provenance tracking (source, timestamp, data freshness)
- [ ] Graceful fallback: Polygon → Schwab → yfinance
- [ ] Agent prompts include actual data, not just reasoning

**Example: Fundamental Agent with Live Data:**
```python
# Before calling 07_fundamental agent, inject real data
fundamentals = await get_fundamentals("MP")
price_history = await get_price_history("MP", timeframe="1day", period="1y")

agent_context = f"""
## Live Market Data for {ticker}

### Current Quote
Price: ${fundamentals.price}
Market Cap: ${fundamentals.market_cap:,.0f}

### Valuation Metrics (as of {fundamentals.as_of_date})
P/E Ratio: {fundamentals.pe_ratio}
Forward P/E: {fundamentals.forward_pe}
EV/EBITDA: {fundamentals.ev_ebitda}
P/B: {fundamentals.price_to_book}

### Financials (TTM)
Revenue: ${fundamentals.revenue_ttm:,.0f}
Net Income: ${fundamentals.net_income_ttm:,.0f}
EPS: ${fundamentals.eps_ttm}
Gross Margin: {fundamentals.gross_margin:.1%}
Operating Margin: {fundamentals.operating_margin:.1%}

### Balance Sheet
Total Debt: ${fundamentals.total_debt:,.0f}
Total Cash: ${fundamentals.total_cash:,.0f}
Debt/Equity: {fundamentals.debt_to_equity}
Current Ratio: {fundamentals.current_ratio}

Data Source: {fundamentals.source.value}
"""

# Agent now reasons with actual data, not hallucinated numbers
```

#### Phase 3C: Web Research Skills
**Dependencies:** Phase 3A

**Available Search Providers:**

| Provider | Capabilities | Use Case |
|----------|--------------|----------|
| **Brave Search** | Web search, news, no tracking | Primary search for general queries |
| **Serper** | Google Search API, fast, cost-effective | Fast Google results, good rate limits |
| **SerpAPI** | Google Search API, news, images, knowledge graph | Comprehensive search with structured results |

**Provider Priority:**
1. **Brave Search** (primary) - Fast, privacy-focused, good for news
2. **Serper** (secondary) - Fast Google results, cost-effective
3. **SerpAPI** (tertiary) - Comprehensive Google results, knowledge graph

**Deliverables:**
- [ ] `skills/web_search.py` - Unified search interface
- [ ] Brave Search integration (web, news)
- [ ] Serper integration (Google search, fast)
- [ ] SerpAPI integration (Google search, news, knowledge graph)
- [ ] Search result parsing and summarization
- [ ] Rate limiting and caching
- [ ] Source credibility scoring (optional)

**Web Search Skill Interface:**
```python
# skills/web_search.py
from typing import Optional, List
from pydantic import BaseModel
from enum import Enum

class SearchProvider(str, Enum):
    BRAVE = "brave"
    SERPER = "serper"
    SERPAPI = "serpapi"

class SearchResult(BaseModel):
    title: str
    url: str
    snippet: str
    source: str
    published_date: Optional[str]
    provider: SearchProvider

class NewsResult(BaseModel):
    title: str
    url: str
    snippet: str
    source: str
    published_date: str
    thumbnail: Optional[str]
    provider: SearchProvider

class WebSearchResponse(BaseModel):
    query: str
    results: List[SearchResult]
    news: List[NewsResult]
    provider: SearchProvider

# Provider configuration
SEARCH_PROVIDER_CONFIG = {
    "brave": {
        "api_key_env": "BRAVE_SEARCH_API_KEY",
        "base_url": "https://api.search.brave.com/res/v1",
        "rate_limit_rpm": 60,
        "priority": 1,
    },
    "serper": {
        "api_key_env": "SERPER_API_KEY",
        "base_url": "https://google.serper.dev",
        "rate_limit_rpm": 100,
        "priority": 2,
    },
    "serpapi": {
        "api_key_env": "SERPAPI_API_KEY",
        "priority": 3,
    },
}

async def web_search(
    query: str,
    num_results: int = 10,
    provider: Optional[SearchProvider] = None
) -> WebSearchResponse:
    """Search the web. Auto-selects best available provider."""
    ...

async def news_search(
    query: str,
    num_results: int = 10,
    freshness: str = "week",  # day, week, month
    provider: Optional[SearchProvider] = None
) -> List[NewsResult]:
    """Search for recent news articles."""
    ...

async def company_news(ticker: str, days: int = 7) -> List[NewsResult]:
    """Get recent news for a specific company/ticker."""
    ...

async def sector_news(sector: str, days: int = 7) -> List[NewsResult]:
    """Get recent news for a sector (e.g., 'rare earth minerals')."""
    ...
```

**Brave Search Client:**
```python
# skills/brave_search.py
import httpx

class BraveSearchClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.search.brave.com/res/v1"

    async def search(
        self,
        query: str,
        count: int = 10,
        freshness: Optional[str] = None,  # pd (24h), pw (week), pm (month)
        search_type: str = "web"  # web, news
    ) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/{search_type}/search",
                headers={"X-Subscription-Token": self.api_key},
                params={"q": query, "count": count, "freshness": freshness}
            )
            return response.json()

    async def news(self, query: str, count: int = 10) -> List[NewsResult]:
        """Fetch news results."""
        data = await self.search(query, count, search_type="news")
        return [NewsResult(...) for r in data.get("results", [])]
```

**Serper Client:**
```python
# skills/serper_client.py
import httpx

class SerperClient:
    """Serper.dev - Fast, cost-effective Google Search API."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://google.serper.dev"

    async def search(self, query: str, num: int = 10) -> dict:
        """Google search via Serper."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/search",
                headers={"X-API-KEY": self.api_key, "Content-Type": "application/json"},
                json={"q": query, "num": num}
            )
            return response.json()

    async def news(self, query: str, num: int = 10) -> List[NewsResult]:
        """Google News search via Serper."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/news",
                headers={"X-API-KEY": self.api_key, "Content-Type": "application/json"},
                json={"q": query, "num": num}
            )
            data = response.json()
            return [NewsResult(...) for r in data.get("news", [])]

    async def images(self, query: str, num: int = 10) -> List[dict]:
        """Google Images search via Serper."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/images",
                headers={"X-API-KEY": self.api_key, "Content-Type": "application/json"},
                json={"q": query, "num": num}
            )
            return response.json().get("images", [])
```

**SerpAPI Client:**
```python
# skills/serpapi_client.py
from serpapi import GoogleSearch

class SerpAPIClient:
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def search(self, query: str, num: int = 10) -> dict:
        """Google search via SerpAPI."""
        search = GoogleSearch({
            "q": query,
            "num": num,
            "api_key": self.api_key
        })
        return search.get_dict()

    async def news(self, query: str, num: int = 10) -> List[NewsResult]:
        """Google News search."""
        search = GoogleSearch({
            "q": query,
            "tbm": "nws",  # News search
            "num": num,
            "api_key": self.api_key
        })
        data = search.get_dict()
        return [NewsResult(...) for r in data.get("news_results", [])]

    async def knowledge_graph(self, query: str) -> Optional[dict]:
        """Get knowledge graph data if available."""
        data = await self.search(query)
        return data.get("knowledge_graph")
```

**Use Cases for Agents:**

| Agent | Web Search Use Case |
|-------|---------------------|
| **01 Systems** | Industry trends, regulatory changes, supply chain news |
| **06 Screener** | Discover companies in sector, validate ticker existence |
| **07 Fundamental** | Recent earnings news, analyst coverage, management changes |
| **08 Technical** | Catalyst events, sentiment shifts |
| **02 Inversion** | Negative news, lawsuits, regulatory risks |
| **05 Epistemic** | Verify claims, check assumption against recent news |

**Example: Screener with Web Search:**
```python
# Before 06_screener runs, gather sector context
sector_news = await news_search("rare earth minerals mining", freshness="month")
web_context = await web_search("rare earth mining companies US listed")

agent_context = f"""
## Recent Sector News (Last 30 Days)

{format_news_results(sector_news)}

## Web Research Results

{format_search_results(web_context)}

Use this information to identify relevant tickers and assess sector dynamics.
Flag any news that materially affects the investment thesis.
"""
```

---

### Phase 4: Production Readiness (Future)

- [ ] Advanced plotting skills (generate actual charts)
- [ ] File/folder ingestion for Reference Materials
- [ ] Trading desk integration hooks
- [ ] Web interface
- [ ] Multi-tenant support
- [ ] Advanced caching
- [ ] SEC filing ingestion (10-K, 10-Q parsing)

---

## 4. Refined Database Schema

### 4.1 Core Tables (No Changes)

The original schema is well-designed. Maintain as specified:
- `runs`
- `steps`
- `agent_calls`
- `state_snapshots`
- `artifacts`

### 4.2 Recommended Additions

```sql
-- Track costs and budgets (with model details for optimization analysis)
CREATE TABLE IF NOT EXISTS cost_tracking (
    tracking_id TEXT PRIMARY KEY,
    run_id TEXT NOT NULL,
    agent_name TEXT NOT NULL,
    provider TEXT NOT NULL,
    model TEXT NOT NULL,
    thinking_mode TEXT DEFAULT 'standard',
    thinking_tokens INTEGER DEFAULT 0,
    tokens_in INTEGER,
    tokens_out INTEGER,
    cost_usd DOUBLE,
    cumulative_run_cost DOUBLE,
    latency_ms INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Track errors for debugging
CREATE TABLE IF NOT EXISTS error_log (
    error_id TEXT PRIMARY KEY,
    run_id TEXT,
    step_id TEXT,
    call_id TEXT,
    error_category TEXT,
    error_message TEXT,
    stack_trace TEXT,
    recovery_action TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Track charter versions
CREATE TABLE IF NOT EXISTS charter_versions (
    version_id TEXT PRIMARY KEY,
    agent_name TEXT NOT NULL,
    charter_path TEXT NOT NULL,
    charter_hash TEXT NOT NULL,
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 5. Refined State Schema

```python
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from enum import Enum
from datetime import datetime

class ObjectiveType(str, Enum):
    INVEST = "invest"
    INVENT = "invent"
    BUILD = "build"
    EXPLORE = "explore"
    DECIDE = "decide"

class TimeHorizon(str, Enum):
    DAYS_WEEKS = "days-weeks"
    MONTHS = "months"
    SIX_TO_EIGHTEEN_MONTHS = "6-18 months"
    MULTI_YEAR = "multi-year"

class CandidateStatus(str, Enum):
    CANDIDATE = "candidate"
    SHORTLIST = "shortlist"
    REJECT = "reject"

class Candidate(BaseModel):
    name: str
    type: str  # company/idea/theme
    summary: str
    status: CandidateStatus
    reasons: List[str]

class Assumption(BaseModel):
    statement: str
    confidence: float = Field(ge=0.0, le=1.0)
    fragility: int = Field(ge=1, le=5)
    source_agent: str
    introduced_by_intake: bool = False

class OpenQuestion(BaseModel):
    question: str
    expected_value: int = Field(ge=1, le=5)
    priority: int = Field(ge=1, le=5)
    owner_agent: str

class Conflict(BaseModel):
    topic: str
    agent_positions: Dict[str, str]
    resolution_plan: Optional[str]

class Decisions(BaseModel):
    recommendation: Optional[str]
    rationale_bullets: List[str] = []
    triggers_to_change_mind: List[str] = []
    next_actions: List[str] = []

class TaskInput(BaseModel):
    title: str
    one_line_ask: str
    objective: ObjectiveType
    horizon: TimeHorizon
    constraints: List[str] = []
    inputs: str  # freeform from task.md
    # Extended intake fields
    background_context: Optional[str]
    prior_hypotheses: Optional[str]
    non_goals: Optional[str]
    risk_appetite: Optional[str]
    capital_effort_budget: Optional[str]
    known_unknowns: Optional[str]
    what_would_change_mind: Optional[str]
    # Intake metadata
    intake_notes: Optional[str]
    assumptions_introduced_by_intake: List[Assumption] = []
    referenced_paths: List[str] = []
    orchestration_preferences: Dict[str, any] = {}

class RunLog(BaseModel):
    iterations_used: int = 0
    stop_reason: Optional[str]

class PipelineState(BaseModel):
    run_id: str
    task: TaskInput
    candidates: List[Candidate] = []
    assumptions: List[Assumption] = []
    open_questions: List[OpenQuestion] = []
    conflicts: List[Conflict] = []
    decisions: Decisions = Decisions()
    run_log: RunLog = RunLog()
    # Phase 2 additions
    required_figures: List[Dict] = []
    generated_figures: List[Dict] = []
```

---

## 6. File Deliverables Summary

### Root Files
| File | Purpose | Phase |
|------|---------|-------|
| `README.md` | Project overview and quick start | 1A |
| `.gitignore` | Git ignore patterns | 1A |
| `.env.example` | Environment variable template | 1A |
| `pyproject.toml` | Dependencies and project config | 1A |
| `TODOS.md` | Development phase tracking | 1A |
| `AGENT_instruction.md` | How to run and extend | 1A |
| `AGENT_context.md` | System design context | 1A |
| `Agent_md.md` | Developer log and checklists | 1A |
| `Makefile` | Common commands | 1A |

### Code Structure
```
config/
├── config.py          # Core configuration
├── models.py          # Model routing config
├── prompts.py         # Shared prompt snippets
└── settings.yaml      # Optional YAML config

runner/
├── __init__.py
├── run.py             # CLI entrypoint
├── pipeline.py        # Pipeline orchestration
├── state.py           # State schema (Pydantic)
├── artifacts.py       # Artifact management
├── db.py              # DuckDB operations
├── llm.py             # Provider abstraction
└── utils.py           # Utilities, hashing

charters/
├── orchestrator.md
├── reporting.md
└── agents/
    ├── 01_systems.md
    ├── 02_inversion.md
    ├── 03_allocator.md
    ├── 04_incentives_timing.md
    ├── 05_epistemic.md
    ├── 06_screener.md         # Equity: ticker identification
    ├── 07_fundamental.md      # Equity: valuation & financials
    └── 08_technical.md        # Equity: chart & momentum analysis

skills/
├── __init__.py
├── extractors.py        # Output parsing
├── scoring.py           # Confidence scoring
├── memo_builder.py      # Report assembly
├── conflicts.py         # Conflict detection
├── financials.py        # Financial data parsing
│
├── # Market Data (Phase 3A)
├── market_data.py       # Unified market data interface
├── polygon_client.py    # Polygon.io API client
├── schwab_client.py     # Schwab API client
├── yfinance_client.py   # yfinance fallback client
│
├── # Web Search (Phase 3C)
├── web_search.py        # Unified search interface
├── brave_search.py      # Brave Search API client
├── serper_client.py     # Serper.dev (Google) client
└── serpapi_client.py    # SerpAPI (Google) client

tests/
├── test_state_schema.py
├── test_prompt_hashing.py
├── test_duckdb_schema.py
└── test_pipeline_smoke.py

notebooks/
├── 01_phase1_db_and_artifacts.ipynb
├── 02_phase1_single_agent_call.ipynb
├── 03_phase1_parallel_then_synth.ipynb
├── 04_phase1_full_pipeline.ipynb
├── 05_phase2_skills_and_report.ipynb
└── 06_phase2_regression_tests.ipynb

data/
├── runs/.gitkeep
└── ledger.duckdb      # Created at runtime

inputs/
├── task_template.md
└── example_tasks/
    └── ai_gpu_optics.md
```

---

## 7. CLI Interface

```bash
# Basic usage
python -m runner.run --task inputs/example_tasks/ai_gpu_optics.md

# Options
python -m runner.run \
    --task PATH           # Required: path to task file
    --run-id ID           # Optional: custom run ID (else auto-generated)
    --max-iterations N    # Default: 2
    --parallel-only       # Debug: stop after parallel pass
    --sequential-only     # Debug: skip parallel, run sequential only
    --no-db               # Skip database logging
    --dry-run             # Print plan without API calls
    --provider PROVIDER   # Override default provider for all agents
    --model MODEL         # Override default model for all agents
    --no-thinking         # Disable extended thinking for all agents
    --verbose             # Detailed logging

# Model override examples
python -m runner.run --task inputs/task.md --model claude-sonnet-4-20250514  # Cost-saving run
python -m runner.run --task inputs/task.md --no-thinking                      # Disable extended thinking
python -m runner.run --task inputs/task.md --provider openai --model gpt-4o   # Use OpenAI
```

---

## 8. Success Criteria

### Phase 1 Complete When:
1. Full pipeline executes end-to-end with example task
2. Strategic agents (01-05) produce valid outputs
3. Final memo follows template structure
4. All database tables populated correctly
5. Run folder contains complete artifacts
6. Notebooks execute without errors

### Phase 2 Complete When:
1. All tests pass
2. Skills layer extracts structured data
3. Equity research agents (06-08) integrated
4. Per-ticker deep-dive workflow functional
5. Conflicts detected and tracked
6. `--dry-run` validates plan
7. Error handling covers all categories

### Phase 3 Complete When:
1. Market data skills fetch live quotes and fundamentals
2. Equity agents use real data when available
3. Graceful fallback when data unavailable
4. Data provenance tracked in artifacts

---

## 9. Known Limitations

1. **No Real-Time Data (Phase 1-2):** Agents reason from input only; no live market data until Phase 3
2. **No Web Browsing:** Explicit constraint; agents flag assumptions
3. **English Only:** No multi-language support in Phase 1-2
4. **Single User:** No authentication or multi-tenancy
5. **Local Only:** No cloud deployment configuration
6. **No RAG:** No retrieval-augmented generation in Phase 1

---

## 10. Future Roadmap

| Priority | Feature | Target Phase |
|----------|---------|--------------|
| High | Advanced plotting skills | Phase 2+ |
| High | File/folder ingestion | Phase 2+ |
| Medium | Trading desk integration | Phase 3 |
| Medium | Web UI | Phase 3 |
| Low | Multi-tenant support | Phase 4 |
| Low | RAG integration | Phase 4 |

---

## 11. Appendix: Example Task File

```markdown
# AI GPU Optics Investment Analysis

## One-Line Ask
Identify 2-3 public companies positioned to benefit from AI infrastructure
buildout, specifically in the GPU-to-datacenter-to-optics value chain.

## Objective
invest

## Time Horizon
6-18 months

## Constraints
- Public companies only
- No web browsing; use reasoning
- Flag all assumptions explicitly
- Focus on optics/interconnect layer

## Background / Context
AI training and inference require massive GPU clusters. These clusters
need high-bandwidth interconnects. Optical components are a potential
bottleneck and value capture point.

## Prior Hypotheses
- Coherent Corp (COHR) and II-VI (now Coherent) may benefit
- Nvidia's networking revenue is underappreciated
- Hyperscalers may vertically integrate

## Risk Appetite
medium

## Known Unknowns
- Actual datacenter capex allocation breakdown
- Optical transceiver ASP trends
- Competitive dynamics in 800G/1.6T transceivers
```

### Example 2: Equity Research Task (Rare Earth Minerals)

```markdown
# Rare Earth Minerals Investment Diligence

## One-Line Ask
Identify 2-4 public companies with meaningful exposure to rare earth minerals
and critical materials for the energy transition, with full fundamental and
technical analysis.

## Objective
invest

## Time Horizon
6-18 months

## Constraints
- Public companies only (US-listed preferred)
- Include both pure-play and diversified exposure
- Perform fundamental analysis on shortlisted tickers
- Perform technical analysis with entry/exit levels
- Flag all assumptions, especially around China policy

## Background / Context
Rare earth elements are critical for EV motors, wind turbines, and defense
applications. Supply is concentrated in China (~60% of mining, ~90% of
processing). Western governments are incentivizing domestic production.

## Prior Hypotheses
- MP Materials (MP) is the only US-based rare earth miner
- Lynas (LTHM) has non-China processing capacity
- Lithium names (ALB, LTHM, SQM) may have rare earth adjacency
- Vertical integration risk from automakers

## Risk Appetite
medium-high

## Analysis Requirements
- Sector screening: Identify all relevant tickers
- Fundamental: P/E, EV/EBITDA, balance sheet, earnings quality
- Technical: Trend, support/resistance, entry zones
- Risks: China policy, commodity price sensitivity, CapEx execution

## Known Unknowns
- Actual rare earth demand growth rates
- DOE/DOD subsidy timelines
- China export restriction probability
- Processing capacity expansion timelines
```

---

## 12. Environment Variables

### Required (Phase 1)
```bash
# .env.example

# LLM Providers (at least one required)
ANTHROPIC_API_KEY=sk-ant-...          # Primary LLM provider
OPENAI_API_KEY=sk-...                  # Fallback LLM provider

# Database
DUCKDB_PATH=data/ledger.duckdb         # Default path for ledger
```

### Required (Phase 3 - Market Data & Search)
```bash
# Market Data Providers
POLYGON_API_KEY=...                    # Polygon.io (primary market data)
SCHWAB_API_KEY=...                     # Schwab API key
SCHWAB_CLIENT_ID=...                   # Schwab OAuth client ID
SCHWAB_CLIENT_SECRET=...               # Schwab OAuth client secret
SCHWAB_REFRESH_TOKEN=...               # Schwab OAuth refresh token

# Web Search Providers
BRAVE_SEARCH_API_KEY=...               # Brave Search (primary)
SERPER_API_KEY=...                     # Serper.dev (secondary, fast Google)
SERPAPI_API_KEY=...                    # SerpAPI (tertiary, comprehensive)
```

### Optional (Per-Agent Overrides)
```bash
# Model overrides for cost optimization
AGENT_ORCHESTRATOR_MODEL=claude-sonnet-4-20250514
AGENT_01_SYSTEMS_MODEL=claude-haiku-3-5-20241022
AGENT_05_EPISTEMIC_THINKING=standard

# Run configuration
MAX_COST_PER_RUN_USD=10.00
DEFAULT_MAX_ITERATIONS=2
```

---

## 13. Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.5 | 2026-02-03 | Added Serper.dev as secondary search provider (fast, cost-effective Google Search). Updated provider priority: Brave → Serper → SerpAPI. Added SerperClient implementation. |
| 1.4 | 2026-02-03 | Added Phase 3C Web Research Skills: Brave Search (primary), SerpAPI (fallback) integrations. Web/news search for all agents. Use cases per agent type. Updated file structure and environment variables. |
| 1.3 | 2026-02-03 | Enhanced Phase 3 Market Data: Added Polygon.io (primary), Schwab API (secondary), yfinance (fallback) integrations. Detailed provider config, data models, and client implementations. Added environment variables section. |
| 1.2 | 2026-02-03 | Added Equity Research Agents (06-08): Sector Screener, Fundamental Analyst, Technical Analyst. New equity research workflow with per-ticker deep-dive. Phase 2B for equity agents, Phase 3 for market data integration. Updated architecture diagram, model tiering, and file structure. |
| 1.1 | 2026-02-03 | Added LLM Provider & Model Strategy (Section 2.6): Claude-first approach, per-agent model tiering, extended thinking configuration, environment overrides, cost optimization path |
| 1.0 | 2026-02-03 | Initial final plan with improvements and recommendations |

---

*Document Version: 1.5*
*Generated: 2026-02-03*
*Status: Final Draft for Review*
