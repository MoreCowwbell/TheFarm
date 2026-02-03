# deepmind1: Multi-Agent Diligence System — Final Project Plan

## Executive Summary

This document provides a refined, actionable project plan for building **deepmind1**, an automated multi-agent diligence workflow system. The system uses LLM-based agents orchestrated through a structured pipeline to perform investment analysis, strategic decision-making, and research tasks.

**Core Value Proposition:** Transform unstructured research questions into rigorous, auditable, multi-perspective analyses with clear recommendations and documented reasoning chains.

---

## 1. Project Understanding & Analysis

### 1.1 System Overview

deepmind1 is a **prompt-orchestrated multi-agent system** that:
- Ingests structured or free-form research tasks
- Executes parallel analysis through 5 specialized reasoning agents
- Synthesizes findings through an orchestrator
- Performs sequential deep-dives based on initial findings
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
│   - Routes to agents                                            │
│   - Synthesizes findings                                        │
│   - Plans sequential deep-dives                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
           ┌──────────────────┼──────────────────┐
           │                  │                  │
           ▼                  ▼                  ▼
    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
    │   PARALLEL   │  │   PARALLEL   │  │   PARALLEL   │
    │    PASS      │  │    PASS      │  │    PASS      │
    │  (5 Agents)  │  │  (5 Agents)  │  │  (5 Agents)  │
    └──────────────┘  └──────────────┘  └──────────────┘
           │                  │                  │
           └──────────────────┼──────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR SYNTHESIS                       │
│            (Conflict resolution, priority ranking)              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    SEQUENTIAL DEEP-DIVE                         │
│        (Targeted follow-up by selected agents)                  │
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
│   - Final memo                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 1.3 The Five Core Agents

| Agent | Primary Focus | Key Outputs |
|-------|---------------|-------------|
| **01 Systems & Second-Order** | System dynamics, feedback loops, value migration | System map, second-order effects, bottlenecks |
| **02 Inversion Thinking** | Failure modes, fragility, downside scenarios | Kill criteria, fragility analysis, mitigations |
| **03 Capital Allocation** | Opportunity cost, portfolio fit, alternatives | Best alternatives, decision thresholds, required returns |
| **04 Incentives & Timing** | Stakeholder incentives, market timing, power dynamics | Incentive map, timing indicators, value capture analysis |
| **05 Epistemic Reality Check** | Knowledge vs assumptions, confidence calibration | Know/assume/speculate table, overconfidence flags |

### 1.4 Key Design Principles

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

| Agent | Model | Thinking Mode | Max Thinking Tokens | Rationale |
|-------|-------|---------------|---------------------|-----------|
| **Orchestrator** | Opus 4.5 | Extended | 10,000 | Synthesis across 5 agents, conflict resolution, planning |
| **01 Systems** | Opus 4.5 | Extended | 8,000 | Second-order effects require deep reasoning chains |
| **02 Inversion** | Opus 4.5 | Extended | 8,000 | Must find non-obvious failure modes |
| **03 Allocator** | Sonnet 4 | Standard | — | More structured/quantitative analysis |
| **04 Incentives** | Sonnet 4 | Standard | — | Pattern matching, less novel reasoning |
| **05 Epistemic** | Opus 4.5 | Extended | 10,000 | Meta-reasoning, catching what others missed |
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
    "orchestrator": AgentModelConfig(
        model="claude-opus-4-5-20250514",
        thinking=ThinkingMode.EXTENDED,
        max_thinking_tokens=10000,
    ),
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
    "05_epistemic": AgentModelConfig(
        model="claude-opus-4-5-20250514",
        thinking=ThinkingMode.EXTENDED,
        max_thinking_tokens=10000,
    ),
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

#### Phase 2B: Testing & Quality Gates
**Dependencies:** Phase 2A

**Deliverables:**
- [ ] `test_state_schema.py`
- [ ] `test_prompt_hashing.py`
- [ ] `test_duckdb_schema.py`
- [ ] `test_pipeline_smoke.py`
- [ ] `--dry-run` validation mode
- [ ] Notebook: `06_phase2_regression_tests.ipynb`

---

### Phase 3: Production Readiness (Future)

- [ ] Advanced plotting skills
- [ ] File/folder ingestion for Reference Materials
- [ ] Trading desk integration hooks
- [ ] Web interface
- [ ] Multi-tenant support
- [ ] Advanced caching

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
    └── 05_epistemic.md

skills/
├── __init__.py
├── extractors.py      # Output parsing
├── scoring.py         # Confidence scoring
├── memo_builder.py    # Report assembly
└── conflicts.py       # Conflict detection

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
2. All 7 agents produce valid outputs
3. Final memo follows template structure
4. All database tables populated correctly
5. Run folder contains complete artifacts
6. Notebooks execute without errors

### Phase 2 Complete When:
1. All tests pass
2. Skills layer extracts structured data
3. Conflicts detected and tracked
4. `--dry-run` validates plan
5. Error handling covers all categories

---

## 9. Known Limitations

1. **No Real-Time Data:** Agents reason from input only; no live market data
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

---

## 12. Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.1 | 2026-02-03 | Added LLM Provider & Model Strategy (Section 2.6): Claude-first approach, per-agent model tiering, extended thinking configuration, environment overrides, cost optimization path |
| 1.0 | 2026-02-03 | Initial final plan with improvements and recommendations |

---

*Document Version: 1.1*
*Generated: 2026-02-03*
*Status: Final Draft for Review*
