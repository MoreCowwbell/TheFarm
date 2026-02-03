# CODEX MASTER PROMPT — Build “deepmind1” Multi-Agent Diligence System (VS Code, DuckDB, Model-Swappable)

You are Codex. Generate a complete, runnable Python project under:

~/AGENT/deepmind1/

Goal: an automated multi-agent diligence workflow with:
- Orchestrator + 5 core agents + Reporting agent
- Parallel wide-net run first, then orchestrator synthesis, then sequential deep-dive
- Full artifact logging to DuckDB + human-readable run folders
- Model/provider swappable via config + .env (OpenAI + Anthropic)
- Phase-based development with smoke tests between phases
- Jupyter notebooks for debugging each phase
- Clear, deterministic output schemas for each agent
- Versioned prompt/charter files and hashing for reproducibility

STRICT REQUIREMENTS:
- Use relative paths inside the repo (no absolute paths in code).
- Use DuckDB as the primary persistence layer.
- Never commit secrets. Read API keys from `.env`.
- Provide safe defaults that run without tools beyond LLM API calls.
- Every agent call must produce a saved markdown artifact and a DB row.
- Pipeline must be auditable and reproducible.

---

## 0) DELIVERABLES YOU MUST CREATE

Create all files/folders below with complete content:

### Root
- `README.md`
- `.gitignore`
- `.env.example`
- `pyproject.toml` (preferred) OR `requirements.txt`
- `TODOS.md` (phase plan with explicit STOP points)
- `AGENT_instruction.md`
- `AGENT_context.md`
- `Agent_md.md`  (note: exact filename)
- `Makefile` (optional but helpful; include if you can)
- `scripts/` (optional helper scripts)

### Code
- `config/`
  - `config.py`
  - `models.py`
  - `prompts.py`
  - `settings.yaml` (optional; include if it helps)
- `charters/`
  - `orchestrator.md`
  - `reporting.md`
  - `agents/`
    - `01_systems.md`
    - `02_inversion.md`
    - `03_allocator.md`
    - `04_incentives_timing.md`
    - `05_epistemic.md`
- `runner/`
  - `run.py` (main entrypoint)
  - `pipeline.py`
  - `state.py`
  - `artifacts.py`
  - `db.py`
  - `llm.py`
  - `utils.py`
- `skills/` (Phase 2)
  - `__init__.py`
  - `extractors.py`
  - `scoring.py`
  - `memo_builder.py`
  - `conflicts.py`
- `tests/` (Phase 2)
  - `test_state_schema.py`
  - `test_prompt_hashing.py`
  - `test_duckdb_schema.py`
  - `test_pipeline_smoke.py`

### Data directories
- `data/`
  - `runs/.gitkeep`
  - `ledger.duckdb` (do NOT create an actual DB file in repo; create on first run)
- `inputs/`
  - `task_template.md`
  - `example_tasks/`
    - `ai_gpu_optics.md`

### Notebooks (for debugging each phase)
- `notebooks/`
  - `01_phase1_db_and_artifacts.ipynb`
  - `02_phase1_single_agent_call.ipynb`
  - `03_phase1_parallel_then_synth.ipynb`
  - `04_phase1_full_pipeline.ipynb`
  - `05_phase2_skills_and_report.ipynb`
  - `06_phase2_regression_tests.ipynb`

---

## 1) HIGH-LEVEL SYSTEM OVERVIEW

### What “agents” are in this project
All agents are **prompt/charter-defined roles** executed via LLM API calls. They are not separate trained models.

Agents included:
- Orchestrator (process manager)
- Core Agents (5):
  1) Systems & Second-Order
  2) Inversion Thinking (rename; combines inversion + fragility)
  3) Capital Allocation
  4) Incentives & Timing
  5) Epistemic Reality Check
- Reporting Agent

### Required workflow
1) Ingest `inputs/task.md` (or path passed via CLI)
2) Create run_id and initial state
3) Execute **parallel pass**: call the 5 core agents with the same input state
4) Orchestrator synthesis pass: reconcile, produce sequential plan
5) Execute **sequential deep-dive**: call selected agents in orchestrator-specified order (default all 5)
6) Optional bounded iteration: up to 2 loops if orchestrator requests follow-ups
7) Call Reporting agent to produce a 1–3 page memo
8) Persist everything:
   - human-readable outputs under `data/runs/<run_id>/`
   - DuckDB rows for run/steps/calls/state/artifacts
9) Exit with clear summary in terminal

### Determinism & auditability
- Each charter file is hashed; hash stored in DB.
- Input state snapshot hashed; stored in DB.
- Output hashed; stored in DB.
- DB schema supports analysis across runs.

---

## 2) DATABASE (DuckDB) SCHEMA (MUST IMPLEMENT)

Create schema (via migrations on startup) with tables:

### `runs`
- run_id TEXT PRIMARY KEY
- created_at TIMESTAMP
- status TEXT
- objective TEXT
- horizon TEXT
- task_type TEXT
- config_json TEXT
- config_hash TEXT

### `steps`
- step_id TEXT PRIMARY KEY
- run_id TEXT
- step_name TEXT
- order_index INTEGER
- status TEXT
- started_at TIMESTAMP
- ended_at TIMESTAMP
- notes TEXT

### `agent_calls`
- call_id TEXT PRIMARY KEY
- run_id TEXT
- step_id TEXT
- agent_name TEXT
- provider TEXT
- model TEXT
- temperature DOUBLE
- max_tokens INTEGER
- charter_path TEXT
- charter_hash TEXT
- input_state_hash TEXT
- system_prompt_hash TEXT
- user_prompt_hash TEXT
- output_path TEXT
- output_hash TEXT
- output_md TEXT (optional; store small outputs inline)
- tool_trace_json TEXT (optional)
- tokens_in INTEGER (optional)
- tokens_out INTEGER (optional)
- cost_usd DOUBLE (optional)
- created_at TIMESTAMP

### `state_snapshots`
- snapshot_id TEXT PRIMARY KEY
- run_id TEXT
- label TEXT          -- e.g., "initial", "post_parallel", "post_synth", "final"
- state_json TEXT
- state_hash TEXT
- created_at TIMESTAMP

### `artifacts`
- artifact_id TEXT PRIMARY KEY
- run_id TEXT
- artifact_type TEXT  -- "md" | "json"
- path TEXT
- hash TEXT
- created_at TIMESTAMP

Ensure all inserts happen, and smoke tests confirm rows exist.

---

## 3) STATE SCHEMA (MUST IMPLEMENT)

Define a strict JSON schema in `runner/state.py` (dataclass or pydantic). Include:

- run_id
- task:
  - title
  - objective            (e.g., "invest", "invent", "build")
  - horizon              (e.g., "weeks", "months", "years")
  - task_type            (e.g., "diligence", "stock_pick", "business_idea")
  - constraints          (list)
  - inputs               (freeform text from task.md)
- candidates: list of objects:
  - name
  - type (company/idea/theme)
  - summary
  - status (candidate/shortlist/reject)
  - reasons (list)
- assumptions: list of objects:
  - statement
  - confidence (0-1)
  - fragility (1-5)
  - source_agent
- open_questions: list of objects:
  - question
  - expected_value (1-5)
  - priority (1-5)
  - owner_agent
- conflicts: list of objects:
  - topic
  - agent_positions (dict agent->position)
  - resolution_plan
- decisions:
  - recommendation
  - rationale_bullets
  - triggers_to_change_mind
  - next_actions
- run_log:
  - iterations_used
  - stop_reason

The orchestrator updates this state. Each step snapshots state to DB.

---

## 4) AGENT CHARTERS (MUST BE VERY EXPLICIT)

You must write each charter in `charters/` as a markdown file used as the SYSTEM prompt (or major part of it). Each charter must include:

- Purpose
- Non-negotiable rules
- Required output schema (exact headings)
- Scoring rubric (self-score 1–5 on completeness)
- Common failure modes to avoid
- “Do not do” list

### 4.1) Core Agent 01: Systems & Second-Order (`01_systems.md`)
Outputs must include:
- TL;DR (3 bullets max)
- System Map (nodes and edges)
- Second-Order Effects (ranked list)
- Value Migration Over Time (what captures value now vs later)
- Bottlenecks/Constraints
- Candidate Implications (how this changes what we pick/do)
- Assumptions + Confidence
- Open Questions (max 7)
- Recommendation to Orchestrator (next steps and what to ask other agents)

### 4.2) Core Agent 02: Inversion Thinking (`02_inversion.md`)
Combine inversion + fragility. Outputs must include:
- TL;DR
- Terminal Failure Modes (ranked, with detection signals)
- Fragility Analysis (what assumptions break first)
- Downside Scenarios (3–5)
- “Kill Criteria” (clear walk-away conditions)
- Mitigations (if any)
- Assumptions + Confidence
- Open Questions
- Recommendation to Orchestrator

### 4.3) Core Agent 03: Capital Allocation (`03_allocator.md`)
Outputs must include:
- TL;DR
- Best Alternative Uses of Capital (ranked)
- Why This Wins / Loses vs Alternatives
- Portfolio Fit (liquidity, concentration, time/attention)
- Required Return vs Risk
- Decision Thresholds (what must be true to allocate)
- Assumptions + Confidence
- Open Questions
- Recommendation to Orchestrator

### 4.4) Core Agent 04: Incentives & Timing (`04_incentives_timing.md`)
Outputs must include:
- TL;DR
- Incentive Map (who wants what; who pays; who can block)
- Power & Value Capture (pricing power, switching costs, standards)
- Timing/Regime Considerations (cycle, capex, sentiment)
- Key Indicators to Watch (non-data placeholders OK)
- Candidate Implications
- Assumptions + Confidence
- Open Questions
- Recommendation to Orchestrator

### 4.5) Core Agent 05: Epistemic Reality Check (`05_epistemic.md`)
Outputs must include:
- TL;DR
- What We Know vs Assume vs Speculate (table)
- Confidence Audit (top 10 claims w/ confidence)
- Map vs Territory Gaps (where model may be wrong)
- Data Needed (what would reduce uncertainty fastest)
- Overconfidence Flags (false precision, narrative traps)
- Assumptions + Confidence
- Open Questions
- Recommendation to Orchestrator

### 4.6) Orchestrator charter (`orchestrator.md`)
Outputs must include:
- Normalized Task Statement (one sentence)
- Frozen Constraints (bullets)
- Key Findings from Parallel Pass (by agent)
- Conflicts Detected + Resolution Plan
- Ranked Uncertainties (top 5)
- Sequential Plan (agent order + why + what each should focus on)
- Stop Condition (explicit)
- State Updates (what to add/remove in assumptions/candidates/questions)
- Next Step: “RUN SEQUENTIAL” (explicit flag)

Orchestrator must never invent facts; it only structures reasoning and routes.

### 4.7) Reporting charter (`reporting.md`)
Outputs must include:
- TL;DR (5 bullets)
- Recommendation (clear)
- Thesis (short)
- Supporting Reasoning (sections)
- Assumptions (with confidence)
- Risks & Kill Criteria
- Triggers/Monitoring Plan
- Appendix: Agent Summaries (brief)
- Placeholders for plots (explicit insert markers)

Keep length 1–3 pages in markdown.

---

## 5) MODEL PROVIDER ABSTRACTION (MUST IMPLEMENT)

Implement provider-agnostic LLM wrapper in `runner/llm.py` with:
- `call_llm(provider, model, system_prompt, user_prompt, temperature, max_tokens) -> (text, meta)`
- Provider `"openai"` and `"anthropic"` supported.
- Read keys from `.env` using `python-dotenv`.

Add configuration in `config/config.py`:
- DEFAULT_PROVIDER
- DEFAULT_MODEL_OPENAI
- DEFAULT_MODEL_ANTHROPIC
- AGENT_MODEL_MAP dict mapping agent_name -> provider/model/temperature/max_tokens
- RETRIES, TIMEOUTS, BACKOFF

Must be easy to switch providers per agent without editing pipeline code.

---

## 6) ARTIFACT MANAGEMENT (MUST IMPLEMENT)

In `runner/artifacts.py`:
- Create run folder `data/runs/<run_id>/`
- Save:
  - `task.md` copy
  - `state_initial.json`
  - Each agent output `01_systems.md`, etc.
  - Orchestrator synthesis
  - Sequential outputs
  - Final memo
  - `meta.json` with model/version + prompt hashes

All saved files must be referenced in DuckDB `artifacts` table.

Also compute SHA256 hash of:
- each charter file
- user prompt
- system prompt
- each output

Store hashes in DuckDB.

---

## 7) CLI ENTRYPOINT (MUST IMPLEMENT)

`python -m runner.run --task inputs/example_tasks/ai_gpu_optics.md`

CLI options:
- `--task` (path)
- `--run-id` (optional, else generate)
- `--max-iterations` default 2
- `--parallel-only` for debugging
- `--no-db` optional (but default uses DB)
- `--dry-run` (prints plan; no API calls)

---

## 8) TODOS.md (MUST BE VERY DETAILED WITH STOP POINTS)

Write `TODOS.md` with:

### Phase 1A: Repo scaffold + config + DB schema
- [ ] Create folders/files
- [ ] Implement DuckDB schema creation/migration on startup
- [ ] Smoke test via notebook `01_phase1_db_and_artifacts.ipynb`
**STOP POINT:** confirm DuckDB tables exist and can insert a dummy run

### Phase 1B: Artifact saving + hashing utilities
- [ ] Implement hashing functions
- [ ] Implement run folder creation
- [ ] Save dummy artifact + insert `artifacts` row
- [ ] Notebook `01_phase1_db_and_artifacts.ipynb` updated
**STOP POINT:** confirm file exists + DB artifact row + correct hash

### Phase 1C: Single agent call end-to-end
- [ ] Implement LLM wrapper for OpenAI + Anthropic
- [ ] Read `.env`
- [ ] Run one agent charter with a small task input
- [ ] Save output md + log `agent_calls`
- [ ] Notebook `02_phase1_single_agent_call.ipynb`
**STOP POINT:** confirm one agent output saved + DB row populated

### Phase 1D: Parallel pass + Orchestrator synthesis
- [ ] Run 5 agents in parallel (ThreadPoolExecutor or asyncio)
- [ ] Snapshot state before/after parallel
- [ ] Orchestrator reads outputs and emits sequential plan
- [ ] Notebook `03_phase1_parallel_then_synth.ipynb`
**STOP POINT:** confirm 5 outputs + orchestrator output + state snapshot rows

### Phase 1E: Full pipeline (parallel → synth → sequential → report)
- [ ] Execute sequential plan (default 5 agents)
- [ ] Bounded iterations (max 2)
- [ ] Call reporting agent and produce final memo
- [ ] Notebook `04_phase1_full_pipeline.ipynb`
**STOP POINT:** confirm final memo generated + all DB rows + run summary

### Phase 2A: Skills layer (deterministic parsing + conflict detection)
- [ ] Implement extractors to parse assumptions/open questions into structured state
- [ ] Implement conflict detector
- [ ] Use skills to update state automatically after each output
- [ ] Notebook `05_phase2_skills_and_report.ipynb`
**STOP POINT:** confirm state is being enriched automatically

### Phase 2B: Regression tests + quality gates
- [ ] Implement tests and minimal evaluation harness
- [ ] Add `--dry-run` plan validation
- [ ] Notebook `06_phase2_regression_tests.ipynb`
**STOP POINT:** tests pass; pipeline stable

Also include a section:
- “Known limitations”
- “Next upgrades” (tools, retrieval, trading desk layer later)

---

## 9) NOTEBOOKS (MUST BE INCLUDED)
Each notebook must:
- Use relative paths
- Be runnable after `pip install -e .` (or equivalent)
- Explain what it checks and print key DB queries results
- Avoid hardcoding secrets

Notebooks should:
- Connect to duckdb
- Query tables and show recent rows
- Open saved artifacts to confirm content exists

---

## 10) AGENT_instruction.md / AGENT_context.md / Agent_md.md
These are meta-dev files to help develop the project.

Create them as follows:

### `AGENT_instruction.md`
- How to run the project
- How to add a new agent
- How to change model routing
- How to interpret run artifacts and DB tables
- Debugging workflow and common errors
- Coding standards for this repo

### `AGENT_context.md`
- Brief description of the objective of the system
- The 5 agents and what they do
- The hybrid loop concept
- The separation between reasoning agents and deterministic skills
- How future “Trading Desk” plug-in would attach (placeholder)

### `Agent_md.md`
- A developer log template:
  - date, change, reason, impact, follow-ups
- A checklist for prompt/charter edits
- A rubric for “did the agent adhere to schema?”

---

## 11) IMPLEMENTATION DETAILS (IMPORTANT)

### Parallelization
Use safe Python parallelism:
- Prefer `concurrent.futures.ThreadPoolExecutor` for network-bound calls.
- Ensure each call logs independently, and failures are captured with status.

### Error handling
- Retry transient network errors (configurable).
- If a provider fails, allow fallback to the other provider if configured.
- Log failures in DB (status field in `steps` and `agent_calls` notes/tool_trace_json).

### Prompt construction
- System prompt = charter content + shared policy snippet from `config/prompts.py`.
- User prompt = task inputs + current state JSON (compact).
- Must include “OUTPUT FORMAT” instruction and require the headings.

### Reproducibility
- Save exact prompts used into artifacts (optional) or hash them.
- Must store charter hashes in DB.

---

## 12) EXAMPLE TASK FILE
Create `inputs/example_tasks/ai_gpu_optics.md` with:
- Title
- Objective: invest
- Horizon: 6–18 months
- Constraints (bullets)
- Prompt: AI → GPU → datacenter → optics; identify 2–3 public companies and reasoning
- Note: “No web browsing. Use reasoning. Flag assumptions.”

This is for smoke testing the pipeline.

---

## 13) FINAL OUTPUT REQUIREMENTS
After generating the codebase, ensure:
- `python -m runner.run --task inputs/example_tasks/ai_gpu_optics.md`
  produces:
  - run folder in `data/runs/<run_id>/`
  - DuckDB database in `data/ledger.duckdb`
  - 5 parallel agent outputs + orchestrator + sequential outputs + final memo
  - console summary with paths + run_id

---

## 14) CODING STYLE REQUIREMENTS
- Python 3.11+ compatible.
- Type hints for core functions.
- Docstrings for public functions.
- Avoid heavy frameworks. Keep dependencies minimal:
  - duckdb
  - python-dotenv
  - pydantic (optional but recommended)
  - rich (optional for CLI)
  - pytest (Phase 2)
  - jupyter (for notebooks)

---

## 15) DO THIS NOW
Generate all files with full contents. Do not omit any deliverable.
Where something is “Phase 2”, still create the files with stub implementations and TODOs, but keep Phase 1 runnable.

## ADDENDUM — FIGURES, PLOTS, AND DATA OWNERSHIP (REPORTING CLARIFICATION)

### Clarification of Responsibility
The **Reporting Agent does NOT decide what figures or plots to generate**.

Instead, plots and figures are:
- **Requested explicitly by the Orchestrator**
- **Owned by upstream agents and/or deterministic skills**
- **Assembled and formatted by the Reporting Agent**

This enforces separation of reasoning vs presentation.

---

## Figure Ownership Model

### 1) Orchestrator (Decides *WHAT* plots are required)
The Orchestrator must:
- Explicitly specify required figures in its output under a section:
  **“Required Figures & Data Artifacts”**
- For each figure, define:
  - figure_id
  - purpose (what question it answers)
  - source agent or skill
  - data requirements (if any)
  - acceptable proxy if data unavailable

Example:
- `FIG-01: AI infrastructure value-chain map (systems agent)`
- `FIG-02: Sector rotation snapshot (trading desk macro agent)`
- `FIG-03: Options positioning heatmap for SPX proxy (options skill)`
- `FIG-04: Support/resistance + invalidation levels (microstructure agent)`

The Orchestrator never generates plots itself.

---

### 2) Core Agents (Request or Flag Needed Figures)
Each core agent may:
- Propose figures that would materially reduce uncertainty
- Specify:
  - what the figure would show
  - why it matters
  - what data is required
  - fallback if unavailable

These proposals are advisory and routed to the Orchestrator.

---

### 3) Skills Layer (Generates Figures Deterministically)
All figure generation MUST happen in the **skills layer**, not inside LLM reasoning.

Create or extend skills such as:
- `skills/plot_system_map.py`
- `skills/plot_macro_snapshot.py`
- `skills/plot_price_levels.py`
- `skills/plot_options_positioning.py`
- `skills/plot_scenario_trees.py`

Each plotting skill must:
- Accept structured input data
- Produce a saved figure file (PNG/SVG)
- Return metadata:
  - file path
  - figure_id
  - caption
  - assumptions used

Plots are saved under:
`data/runs/<run_id>/figures/`

---

### 4) Reporting Agent (Assembles, Does Not Invent)
The Reporting Agent must:
- Embed or reference only figures explicitly requested by the Orchestrator
- Use figure placeholders only if a requested figure failed to generate
- Include:
  - figure number
  - caption (from skill metadata)
  - short interpretation tied to the thesis

The Reporting Agent must never:
- Invent figures
- Decide which plots “would be nice”
- Generate synthetic charts from imaginary data

---

## Reporting Charter Update (Explicit Rule)
Add the following rule to `charters/reporting.md`:

> **Figures Rule:**  
> The Reporting Agent may only include figures explicitly listed by the Orchestrator under “Required Figures & Data Artifacts” and generated by deterministic skills. If a figure is unavailable, the Reporting Agent must insert a clearly marked placeholder and explain why.

---

## Phase 2 Implementation Note
In Phase 2:
- Extend the Orchestrator state schema to include:
  - `required_figures: []`
  - `generated_figures: []`
- Add plotting skills incrementally, starting with:
  - system/value-chain diagrams
  - basic macro regime snapshots
  - simple price level charts (for stock tasks)

This keeps Phase 1 reasoning clean while making Phase 2 reporting fully data-backed.

---

## Design Rationale (Do Not Change)
- Reasoning agents decide *what matters*
- Skills generate *truthful artifacts*
- Reporting tells a *coherent story from verified outputs*
- No agent is allowed to hallucinate visual evidence

Below is a **clean addendum** you can paste **after the original prompt** (and after the previous addendum). It introduces a **structured input form** and how the Orchestrator must consume it, without changing any existing instructions.

---

```markdown
## ADDENDUM — STRUCTURED TASK INPUT (ORCHESTRATOR INTAKE FORM)

### Purpose
Users need a consistent way to “talk to the Orchestrator” and provide high-quality context without writing ad-hoc prompts.

This project must support:
- a **minimal input** (one paragraph prompt), AND
- a **rich, structured intake form** with optional sections,
- including the ability to point to folders/files for context ingestion.

The Orchestrator is responsible for normalizing all inputs into a canonical internal task representation.

---

## Task Intake Design

### 1) Primary Input Mechanism
The system ingests a **task markdown file** (default path passed via CLI):

```

inputs/task.md

```

This file follows a **structured but optional schema**.

The pipeline MUST run even if only the minimal required fields are provided.

---

## 2) Task Input Schema (Human-Writable Markdown)

Create a template at:

```

inputs/task_template.md

````

The template MUST include the following sections.

### REQUIRED (minimum viable task)

```markdown
# Task Title

## One-Line Ask
(Plain English description of what you want the system to decide or analyze.)

## Objective
(one of: invest | invent | build | explore | decide)

## Time Horizon
(e.g. days–weeks | months | 6–18 months | multi-year)

## Constraints
- (optional bullet list; can be empty)
````

If the user provides only these sections, the system must still run.

---

### OPTIONAL — HIGH-VALUE CONTEXT (recommended)

```markdown
## Background / Context
(Why this matters, what prompted the task, prior beliefs.)

## Prior Hypotheses
(Optional. What you currently believe might be true.)

## Non-Goals
(What you explicitly do NOT want the system to do.)

## Risk Appetite
(low | medium | high | asymmetric | capital-preserving)

## Capital / Effort Budget
(Optional. Rough scale of capital, time, or effort.)

## Known Unknowns
(Optional. Questions you already know you don’t have answers to.)

## What Would Change My Mind
(Optional. Early articulation of falsification triggers.)
```

---

### OPTIONAL — FILES, DATA, AND ARTIFACTS

```markdown
## Reference Materials
You may reference:
- local folders
- specific files
- prior memos
- datasets
- plots

List paths relative to project root, for example:
- data/external/ai_reports/
- data/market/spx_options.parquet
- notes/previous_thesis.md
```

Rules:

* The Orchestrator must acknowledge referenced paths.
* In Phase 1, files are **not automatically parsed** unless trivial (e.g. markdown).
* The Orchestrator must decide whether to:

  * ignore,
  * summarize,
  * defer to Phase 2 skills,
  * or flag as required follow-up ingestion.

---

### OPTIONAL — MODE OVERRIDES (advanced users)

```markdown
## Orchestration Preferences (Optional)
- Preferred depth: shallow | normal | deep
- Allow iterations: yes | no (default yes, max 2)
- Emphasize agents:
  - Systems
  - Inversion
  - Capital Allocation
  - Incentives & Timing
  - Epistemic
- De-emphasize agents:
  - (list if any)
```

These are **advisory only**. The Orchestrator may override them and must explain why if it does.

---

## 3) Orchestrator Responsibilities for Task Intake

Upon reading the task file, the Orchestrator MUST:

1. **Normalize the input**

   * Extract required fields
   * Capture optional context
   * Resolve ambiguities
   * Restate the task in one precise sentence

2. **Declare an Intake Summary**
   In its first output, include a section:

   ```
   ## Task Intake Summary
   ```

   with:

   * Interpreted objective
   * Assumed scope
   * Missing but important context
   * Any ambiguities or conflicts in the input

3. **Decide Sufficiency**
   Explicitly state one of:

   * “Sufficient to proceed”
   * “Proceed with assumptions”
   * “Insufficient — requires clarification” (must list questions)

4. **Populate Initial State**

   * Fill `task`, `constraints`, and `initial assumptions`
   * Initialize `open_questions` from missing context
   * Snapshot state as `state_initial`

---

## 4) CLI Behavior (No Changes Required)

The existing CLI remains valid:

```bash
python -m runner.run --task inputs/example_tasks/ai_gpu_optics.md
```

If the task file omits optional sections:

* The Orchestrator fills gaps with explicit assumptions.
* These assumptions MUST be surfaced and tagged with confidence.

---

## 5) Design Rules (Non-Negotiable)

* The Orchestrator must **never silently infer user intent**.
* Any assumption made due to missing input must be:

  * explicit
  * confidence-tagged
  * listed under “Assumptions Introduced by Intake”
* The system must remain usable with a single paragraph prompt.

---

## 6) Rationale

This intake form:

* makes human–agent interaction repeatable,
* prevents prompt drift,
* improves downstream agent quality,
* allows gradual adoption (basic → advanced),
* and cleanly supports future ingestion of folders, datasets, and trading-desk inputs.

Do not collapse this into a single free-form prompt.

```

---

This completes the **input side of the architecture**:

- You now have:
  - structured intake
  - orchestrator normalization
  - explicit assumption handling
  - clean extensibility for file/data ingestion

If you want next, the logical follow-ups are:
- defining **which intake fields map to which agents**
- or designing a **“task sufficiency score”** the Orchestrator computes before running expensive analysis
```
Below is a **single, self-contained Codex prompt block** you can copy-paste **as an amendment** after your prior two prompts.
It does **not** restate or rewrite anything earlier; it only adds the structured-intake requirement and its implications.

---

````markdown
## ADDENDUM — STRUCTURED TASK INTAKE & ORCHESTRATOR NORMALIZATION (CODEX INSTRUCTION)

You must extend the project to include a **structured task intake mechanism** that allows a user to provide anything from a minimal prompt to a richly contextualized input with optional references to files and folders.

This addendum does NOT replace any prior instructions. It strictly augments them.

---

## 1) REQUIRED INPUT FORM (HUMAN-WRITABLE MARKDOWN)

Create the following files:

- `inputs/task_template.md`
- `inputs/example_tasks/ai_gpu_optics.md` (must follow the template)

The system must accept a task file that may include **only the minimum required fields**, yet also support **many optional sections**.

### REQUIRED SECTIONS (minimum viable task)
The pipeline MUST run if only these are present:

```markdown
# Task Title

## One-Line Ask
(Plain English description of what decision or analysis is requested.)

## Objective
(one of: invest | invent | build | explore | decide)

## Time Horizon
(e.g. days–weeks | months | 6–18 months | multi-year)

## Constraints
(Optional bullet list; may be empty.)
````

---

### OPTIONAL HIGH-VALUE CONTEXT SECTIONS

Support (but do not require) the following sections:

```markdown
## Background / Context
## Prior Hypotheses
## Non-Goals
## Risk Appetite
## Capital / Effort Budget
## Known Unknowns
## What Would Change My Mind
```

---

### OPTIONAL FILE & DATA REFERENCES

Support explicit user references to local files and folders:

```markdown
## Reference Materials
- data/external/ai_reports/
- notes/previous_thesis.md
- data/market/spx_options.parquet
```

Rules:

* Paths are relative to project root.
* Phase 1: do NOT automatically parse non-trivial files.
* Orchestrator must acknowledge referenced paths and decide:
  ignore | summarize | defer | request follow-up ingestion.

---

### OPTIONAL ORCHESTRATION PREFERENCES

Support advisory-only overrides:

```markdown
## Orchestration Preferences
- Preferred depth: shallow | normal | deep
- Allow iterations: yes | no
- Emphasize agents:
  - Systems
  - Inversion
  - Capital Allocation
  - Incentives & Timing
  - Epistemic
- De-emphasize agents:
  - (optional)
```

The Orchestrator may override these preferences but must explain why.

---

## 2) ORCHESTRATOR INTAKE RESPONSIBILITIES (MANDATORY)

After reading the task file, the Orchestrator MUST:

1. Normalize all input into a canonical internal representation.
2. Restate the task as a **single precise decision sentence**.
3. Explicitly list:

   * ambiguities
   * missing but important context
   * assumptions introduced due to missing input (with confidence).
4. Decide and state one of:

   * “Sufficient to proceed”
   * “Proceed with assumptions”
   * “Insufficient — requires clarification” (list questions).
5. Populate initial shared state accordingly and snapshot it as `state_initial`.

The Orchestrator must NEVER silently infer user intent.

---

## 3) STATE SCHEMA EXTENSION

Extend the shared state schema to include:

* `task.intake_notes`
* `task.assumptions_introduced_by_intake`
* `task.referenced_paths`
* `task.orchestration_preferences`

All must be persisted in DuckDB snapshots.

---

## 4) REPORTING INTERACTION (NO CHANGE TO PRIOR RULES)

The Reporting Agent uses only:

* normalized task
* orchestrator-approved assumptions
* verified agent outputs
* orchestrator-specified figures (per prior addendum)

No free-form reinterpretation of user intent is allowed.

---

## 5) NON-NEGOTIABLE DESIGN RULES

* The system must remain usable with a single-paragraph task.
* Any assumption added due to missing input must be explicit and confidence-tagged.
* Structured intake improves agent quality but must never block execution unless explicitly declared “insufficient” by the Orchestrator.

Implement this addendum fully while preserving all prior architecture, agent roles, and constraints.

```

---

This block is **drop-in safe** after your two prior prompts and cleanly completes the **human → orchestrator interface**.

If you want next, I can:
- design the **exact CLI flags** that map to intake overrides, or
- define a **task sufficiency scoring function** the Orchestrator computes before running costly phases.
```
