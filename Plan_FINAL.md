# deepmind1: Multi-Agent Diligence System — Final Project Plan

## Executive Summary

This document provides a refined, actionable project plan for building **deepmind1**, an automated multi-agent diligence workflow system. The system uses LLM-based agents orchestrated through a structured pipeline to perform investment analysis, strategic decision-making, and research tasks.

**Core Value Proposition:** Transform unstructured research questions into rigorous, auditable, multi-perspective analyses with clear recommendations and documented reasoning chains.

---

## 1. Project Understanding & Analysis

### 1.1 System Overview

deepmind1 is a **prompt-orchestrated multi-agent system** that:
- Ingests research tasks via conversational intake or direct task files
- Executes parallel analysis through 9 specialized agents (8 reasoning + 1 data layer)
- Synthesizes findings through an orchestrator
- Performs sequential deep-dives based on initial findings (including equity research)
- Produces auditable, human-readable reports with full provenance

### 1.2 Agent Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      ENTRY OPTIONS                               │
├─────────────────────────────────────────────────────────────────┤
│  Option A: Direct Task File                                      │
│  python -m runner.run --task task.md                            │
│                                                                  │
│  Option B: Conversational Intake (via Claude Code CLI)          │
│  claude → /intake → multi-turn conversation                      │
│  → generates task.md + reference_materials/                      │
│  python -m runner.run --intake <intake_id>                      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                USER INPUT (task.md + ref_materials/)            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       ORCHESTRATOR                              │
│   - Normalizes input, loads reference materials                 │
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
└──────────────┘       └──────┬───────┘       └──────────────┘
     │                        │                        │
     │                        ▼                        │
     │               ┌──────────────┐                  │
     │               │ 09_FINANCIAL │ (Data Layer)     │
     │               │    DATA      │                  │
     │               │ - Live APIs  │                  │
     │               │ - SEC filings│                  │
     │               │ - Agentic    │                  │
     │               │   routing    │                  │
     │               └──────────────┘                  │
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

The system employs 9 specialized agents organized into five categories:

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

#### Data Layer Agent (09)

| Agent | Primary Focus | Key Outputs |
|-------|---------------|-------------|
| **09 Financial Data** | Live market data retrieval, API integration, agentic tool routing | Price snapshots, financial statements, ratios, analyst estimates, SEC filings |

**Note:** 09_financial_data is a specialized subagent inspired by the Dexter project's agentic tool routing pattern. It is NOT directly invoked by the Orchestrator, but rather delegated to by agents 06, 07, 08, 04, and CoVe_verifier when they need live financial data. Key features:
- **Agentic routing:** Translates natural language data requests into specific API calls
- **Source attribution:** All data includes source, freshness timestamp, and confidence level
- **CoVe integration:** Data provenance enables downstream claim verification
- **Caching:** Results cached within a run to avoid duplicate API calls

#### Intake System

| Component | Primary Focus | Key Outputs |
|-----------|---------------|-------------|
| **Intake Conversation Agent** | Conversational task definition, document processing, multi-session support | task.md, reference_materials/, session transcript, intake_summary.md |

**Note:** The Intake Conversation Agent runs via Claude Code CLI (`/intake`). Instead of filling out a form, users have a natural brainstorming conversation to articulate their research question. The agent processes uploaded documents (PDFs, URLs, Excel, images) and makes them available to all downstream agents.

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

#### Equity Agent Charter Prompts

The following prompt patterns guide each equity research agent's analysis approach:

**06 Sector Screener - Stock Screening Prompt:**
```markdown
## Charter: AI Stock Screener

Create a screening checklist for identifying high-quality stocks in the target sector:

### Screening Criteria
1. **Valuation Filters**
   - P/E ratio relative to sector
   - EV/EBITDA vs peers
   - Price-to-book threshold

2. **Growth Prospects**
   - Revenue growth rate (3Y CAGR)
   - Earnings growth trajectory
   - TAM expansion potential

3. **Financial Health**
   - Debt/Equity ratio
   - Current ratio
   - Free cash flow generation
   - Interest coverage

4. **Competitive Advantage**
   - Market share position
   - Barriers to entry
   - Pricing power indicators
   - IP/regulatory moat

5. **Risk Factors**
   - Concentration risk (customer/supplier)
   - Regulatory exposure
   - Currency/commodity sensitivity
   - Management track record

### Output Requirements
- Universe of tickers meeting criteria
- Classification: Pure-play vs Diversified
- Market cap tier: Large/Mid/Small
- Exclusions with reasoning
```

**07 Fundamental Analyst - Market Analyst Prompt:**
```markdown
## Charter: Professional Stock Market Analyst

Analyze the stock based on comprehensive fundamental factors:

### Analysis Framework
1. **Business Model Assessment**
   - Revenue streams and mix
   - Unit economics
   - Scalability factors
   - Customer acquisition/retention

2. **Financial Ratio Analysis**
   - Profitability: ROE, ROA, ROIC
   - Efficiency: Asset turnover, inventory days
   - Liquidity: Current ratio, quick ratio
   - Leverage: Debt/Equity, interest coverage

3. **Management Quality**
   - Track record on capital allocation
   - Insider ownership and transactions
   - Compensation alignment
   - Strategic execution history

4. **Competitive Edge**
   - Porter's Five Forces assessment
   - Sustainable advantages
   - Disruption vulnerabilities

5. **Long-term Potential**
   - Industry growth drivers
   - Company positioning for trends
   - Optionality and pivots

### Output Requirements
- Clear valuation range (DCF, comps)
- Bull/Base/Bear case scenarios
- Key assumptions flagged
- Investment thesis summary
```

**08 Technical Analyst - Chart Breakdown Prompt:**
```markdown
## Charter: Technical Chart Analyst

Interpret the stock's technical setup using key indicators:

### Technical Framework
1. **Trend Analysis**
   - Primary trend (200 DMA relationship)
   - Secondary trend (50 DMA, recent highs/lows)
   - Trend strength assessment

2. **Moving Averages**
   - 20/50/200 DMA positions
   - Golden/Death cross status
   - MA slope and spacing

3. **Momentum Indicators**
   - RSI (14): Overbought/oversold/neutral
   - MACD: Signal line crossovers, histogram
   - Stochastic: Fast/slow readings

4. **Support/Resistance**
   - Key horizontal levels
   - Trendline support/resistance
   - Fibonacci retracements (if applicable)

5. **Volume Analysis**
   - Volume trend vs price
   - Accumulation/distribution patterns
   - Volume at price levels

### Output Requirements
- Trend direction and strength
- Key levels table (support/resistance)
- Momentum assessment
- Entry/exit zones (not predictions)
- Likely scenarios based on technicals

NOTE: Present likely scenarios, NOT predictions.
```

**03 Capital Allocator - Risk Manager Prompt Enhancement:**
```markdown
## Charter Enhancement: Portfolio Risk Management

When analyzing position sizing and risk:

### Risk Framework
1. **Risk Appetite Assessment**
   - Time horizon alignment
   - Drawdown tolerance
   - Correlation with existing positions

2. **Position Sizing**
   - Maximum position size (% of portfolio)
   - Scaling approach (all-in vs tranches)
   - Stop-loss placement rationale

3. **Diversification Check**
   - Sector concentration
   - Factor exposure overlap
   - Geographic diversification

4. **Risk Controls**
   - Hard stop levels
   - Trailing stop methodology
   - Rebalancing triggers

NOTE: Define percentage allocations and risk controls,
NOT specific buy/sell recommendations.
```

**News Impact Analyzer Skill - For Multiple Agents:**
```markdown
## Skill: News Impact Analysis

When processing news events for any agent:

### Analysis Framework
1. **Event Classification**
   - Type: Earnings, M&A, Regulatory, Macro, Management, Product
   - Magnitude: Material / Minor / Noise
   - Timeline: Immediate / Near-term / Long-term

2. **Impact Assessment**
   - Direct effects on company fundamentals
   - Indirect effects on sector/peers
   - Sentiment impact vs fundamental impact

3. **Balanced View**
   - Short-term market reaction likelihood
   - Long-term fundamental impact
   - Overreaction/underreaction potential

### Output Requirements
- Event summary
- Impact classification
- Short-term vs long-term view
- Uncertainty flags

NOTE: Provide balanced analysis without buy/sell advice.
```

**Daily Market Routine - Orchestrator Enhancement:**
```markdown
## Orchestrator: Daily Market Analysis Routine

When running daily market check tasks:

### 10-Minute Routine
1. **Index Check** (2 min)
   - S&P 500, NASDAQ, Russell 2000 status
   - Overnight futures/global markets
   - VIX level and trend

2. **News Scan** (3 min)
   - Top market-moving headlines
   - Sector-specific news for watchlist
   - Earnings calendar check

3. **Watchlist Review** (3 min)
   - Price changes on positions
   - Approaching key levels
   - Volume anomalies

4. **Risk Check** (2 min)
   - Portfolio heat map
   - Concentration alerts
   - Upcoming catalysts

### Output: Brief Daily Summary
- Market mood (risk-on/risk-off/neutral)
- Watchlist alerts
- Today's focus areas
```

### 1.5 Chain-of-Verification (CoVe) Module

The CoVe module is an **on-demand verification pipeline** triggered by the Orchestrator to reduce hallucinations and confirmation bias in high-stakes outputs. It enforces separation between generation and verification.

#### When CoVe is Triggered

The Orchestrator activates CoVe when:

| Trigger Condition | Example |
|-------------------|---------|
| **Numerical claims** | Valuation figures, P/E ratios, price targets |
| **Investment recommendations** | "Buy MP at $20-22" |
| **Factual assertions** | "MP is the only US rare earth miner" |
| **High confidence statements** | Claims without hedging language |
| **Final memo generation** | Before Reporting Agent produces output |
| **User requests verification** | Explicit ask for fact-checking |

#### CoVe Agent Roles

```
┌─────────────────────────────────────────────────────────────────┐
│                    CoVe MODULE FLOW                             │
│                  (Triggered by Orchestrator)                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│              AGENT A: GENERATOR (Source Agent)                  │
│                                                                 │
│  Input: Original agent output (e.g., 07_fundamental)            │
│  Output:                                                        │
│    - Draft Answer (concise)                                     │
│    - Atomic Claims List (checkable statements)                  │
│    - Assumptions (explicit)                                     │
│    - Known Unknowns                                             │
│                                                                 │
│  Rule: No self-verification                                     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│              AGENT B: SKEPTIC (Verification Planner)            │
│                                                                 │
│  Input: Atomic claims list from Agent A                         │
│  Output: 3-7 Verification Questions (VQs)                       │
│                                                                 │
│  VQ Design Rules:                                               │
│    - 1 VQ checks core conclusion                                │
│    - 1 VQ checks key numbers/thresholds                         │
│    - 1 VQ checks counterexamples/edge cases                     │
│    - 1 VQ checks missing assumptions                            │
│                                                                 │
│  Each VQ includes:                                              │
│    - Target claim(s)                                            │
│    - What would falsify it                                      │
│    - What evidence would support it                             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│              AGENT C: INDEPENDENT VERIFIER                      │
│                                                                 │
│  Input: Atomic claims + VQs (NOT the draft answer)              │
│                                                                 │
│  CRITICAL CONSTRAINTS:                                          │
│    - Cannot read Agent A's draft answer                         │
│    - Cannot defend the draft                                    │
│    - Must start from first principles                           │
│    - Can use web search / market data skills                    │
│    - If no evidence: mark as "Unverified"                       │
│                                                                 │
│  Output per VQ:                                                 │
│    - Verdict: Supported / Contradicted / Unverified / Unclear   │
│    - Reasoning: short, factual                                  │
│    - Correction: if contradicted                                │
│    - Confidence: High / Medium / Low                            │
│    - Dependencies: what else must be true                       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│              AGENT D: EDITOR (Finalizer)                        │
│                                                                 │
│  Input: Draft + Verification Results                            │
│                                                                 │
│  Rules:                                                         │
│    - Remove or weaken Contradicted claims                       │
│    - Hedge Unverified claims with caveats                       │
│    - Preserve Supported claims                                  │
│    - Add "Unclear" items as open questions                      │
│                                                                 │
│  Output:                                                        │
│    - Final Verified Answer                                      │
│    - Caveats / Conditions                                       │
│    - Open Questions (if blockers remain)                        │
│    - Verification Summary (what changed)                        │
└─────────────────────────────────────────────────────────────────┘
```

#### CoVe Output Schema

```python
# runner/cove.py
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class ClaimType(str, Enum):
    CORE = "core"           # Must be verified to ship
    SUPPORTING = "supporting"  # Should be verified
    COSMETIC = "cosmetic"   # Nice to verify

class Verdict(str, Enum):
    SUPPORTED = "supported"
    CONTRADICTED = "contradicted"
    UNVERIFIED = "unverified"
    UNCLEAR = "unclear"

class Confidence(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class AtomicClaim(BaseModel):
    claim_id: str
    statement: str
    claim_type: ClaimType
    source_agent: str
    source_section: Optional[str]

class VerificationQuestion(BaseModel):
    vq_id: str
    target_claims: List[str]  # claim_ids
    question: str
    falsifier: str  # What would prove this wrong
    supporting_evidence: str  # What would confirm this

class VerificationResult(BaseModel):
    vq_id: str
    verdict: Verdict
    reasoning: str
    correction: Optional[str]
    confidence: Confidence
    dependencies: List[str]
    sources_checked: List[str]  # URLs, data sources consulted

class CoVeOutput(BaseModel):
    run_id: str
    source_agent: str
    draft_answer: str
    atomic_claims: List[AtomicClaim]
    verification_questions: List[VerificationQuestion]
    verification_results: List[VerificationResult]
    final_answer: str
    caveats: List[str]
    open_questions: List[str]
    verification_summary: str
```

#### CoVe Stop Conditions

| Condition | Action |
|-----------|--------|
| Any **core** claim is `Contradicted` | **Must revise** - cannot ship |
| ≥2 **core** claims are `Unverified` | **Must qualify** or request clarification |
| All **core** claims are `Supported` | **Ship** final answer |
| **Supporting** claims contradicted | Revise or remove, but can still ship |

#### Integration with Existing Agents

CoVe wraps around existing agent outputs:

```python
# runner/pipeline.py
async def run_agent_with_cove(
    agent_name: str,
    agent_output: str,
    cove_trigger: bool = False
) -> str:
    """Optionally run CoVe on agent output."""

    if not cove_trigger:
        return agent_output

    # Step 1: Extract atomic claims
    claims = await cove_generator.extract_claims(agent_output)

    # Step 2: Generate verification questions
    vqs = await cove_skeptic.generate_vqs(claims)

    # Step 3: Independent verification (can use web search, market data)
    results = await cove_verifier.verify(claims, vqs)

    # Step 4: Edit and finalize
    final = await cove_editor.finalize(agent_output, results)

    # Store CoVe artifacts
    save_cove_artifacts(run_id, agent_name, claims, vqs, results, final)

    return final.final_answer
```

#### Example: CoVe on Fundamental Analyst Output

**Input (07_fundamental claim):**
> "MP Materials trades at P/E of 28.4x vs sector average of 22.1x"

**Agent A (Generator) - Atomic Claims:**
```markdown
1. [CORE] MP Materials current P/E is 28.4x
2. [CORE] Rare earth sector average P/E is 22.1x
3. [SUPPORTING] MP trades at a premium to sector
```

**Agent B (Skeptic) - Verification Questions:**
```markdown
VQ1: What is MP's actual trailing P/E ratio as of today?
     Falsifier: P/E is significantly different from 28.4x
     Evidence: Quote from Polygon/yfinance

VQ2: What is the actual sector average P/E?
     Falsifier: Sector avg differs from 22.1x by >10%
     Evidence: Peer comparison data

VQ3: Are there valid reasons MP should trade at premium/discount?
     Falsifier: MP has structural issues justifying discount
     Evidence: Recent earnings, guidance, competitive position
```

**Agent C (Verifier) - Results:**
```markdown
VQ1: SUPPORTED (High confidence)
     Polygon API returns P/E of 27.9x (within 2%)

VQ2: UNVERIFIED (Medium confidence)
     Cannot find consistent "rare earth sector" definition
     Peers vary: LTHM 18x, ALB 12x, no clear avg

VQ3: SUPPORTED (Medium confidence)
     Only integrated US producer, strategic value premium
```

**Agent D (Editor) - Final Output:**
```markdown
MP Materials trades at P/E of ~28x. Direct sector comparison is
difficult due to peer heterogeneity (lithium-focused peers trade
at 12-18x), but MP's premium may be justified by its position as
the only integrated US rare earth producer.

Caveat: "Sector average" claim removed - peer set is not well-defined.
```

#### Model Configuration for CoVe Agents

| CoVe Agent | Model | Thinking Mode | Rationale |
|------------|-------|---------------|-----------|
| **Generator** | Sonnet 4 | Standard | Extraction task, structured output |
| **Skeptic** | Opus 4.5 | Extended | Must find non-obvious failure modes |
| **Verifier** | Opus 4.5 | Extended | Independent reasoning, can use skills |
| **Editor** | Sonnet 4 | Standard | Synthesis and formatting |

#### Database Schema for CoVe

```sql
-- Track CoVe verification runs
CREATE TABLE IF NOT EXISTS cove_runs (
    cove_id TEXT PRIMARY KEY,
    run_id TEXT NOT NULL,
    source_agent TEXT NOT NULL,
    trigger_reason TEXT,
    claims_total INTEGER,
    claims_core INTEGER,
    claims_supported INTEGER,
    claims_contradicted INTEGER,
    claims_unverified INTEGER,
    verdict TEXT,  -- 'shipped', 'revised', 'blocked'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Track individual claim verifications
CREATE TABLE IF NOT EXISTS cove_claims (
    claim_id TEXT PRIMARY KEY,
    cove_id TEXT NOT NULL,
    statement TEXT,
    claim_type TEXT,
    verdict TEXT,
    confidence TEXT,
    correction TEXT,
    sources_checked TEXT,  -- JSON array
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 1.6 Reporting Agent & Report Quality Standards

The Reporting Agent produces the final deliverable: a **sell-side quality research memo** structured with the **Amazon memo philosophy**. This is the user-facing artifact that synthesizes all agent outputs.

#### 1.6.1 Amazon Memo Philosophy

The Amazon-style memo emphasizes **clarity over brevity** and **structured thinking over bullet points**:

| Principle | Application in Reports |
|-----------|------------------------|
| **Narrative prose** | Key findings written in full sentences, not just bullets |
| **"So what?" test** | Every section must answer: "Why does this matter for the decision?" |
| **Data-backed claims** | Quantitative support for qualitative statements |
| **Disagree and commit** | Document dissenting views before final recommendation |
| **Start with the conclusion** | Executive summary leads with recommendation |
| **Appendices for depth** | Main memo is 1-3 pages; supporting detail in appendices |

#### 1.6.2 Sell-Side Quality Standards

Reports must meet the quality bar of professional sell-side research:

| Quality Dimension | Standard | Enforcement |
|-------------------|----------|-------------|
| **Data Accuracy** | All figures verified via CoVe or market data | Automated verification |
| **Source Attribution** | Every data point has provenance | Source field required |
| **Visual Quality** | Publication-ready charts | Style guide compliance |
| **Logical Flow** | Clear thesis → evidence → conclusion | Template structure |
| **Risk Balance** | Bull AND bear cases presented | Required sections |
| **Actionability** | Clear recommendations with triggers | Decision framework |
| **Timeliness** | Data freshness noted | Timestamp requirements |

#### 1.6.3 Reporting Agent Charter

```markdown
## Charter: Reporting Agent

You are a senior equity research analyst at a top-tier investment bank. Your role
is to synthesize multi-agent analysis into a professional research memo that meets
publication standards.

### Writing Philosophy (Amazon Memo Style)

1. **Lead with the answer**: Executive summary states recommendation first
2. **Narrative over bullets**: Use prose to explain reasoning, bullets for lists only
3. **Every claim supported**: Link statements to source agents or data
4. **Assume intelligent reader**: No jargon explanation, but define non-obvious terms
5. **Honest uncertainty**: Use confidence language ("likely", "suggests", "unclear")

### Report Structure

Your output MUST follow this structure:

#### 1. Executive Summary (1/2 page max)
- **Recommendation**: Clear action (Buy/Hold/Sell or equivalent decision)
- **Key Thesis**: 2-3 sentences on why
- **Price Target / Decision Threshold**: Quantitative anchor
- **Risk Level**: Low/Medium/High with primary risk factor

#### 2. Investment Thesis (1 page)
- **The Opportunity**: What asymmetry exists?
- **Key Drivers**: 3-5 factors that make this work
- **Why Now**: Timing rationale and catalysts
- **Differentiated View**: What the market is missing

#### 3. Analysis Summary (1-2 pages)
- **Systems Analysis**: Value chain, second-order effects
- **Fundamental Assessment**: Valuation, financials, quality
- **Technical Setup**: Entry zones, risk levels (if equity)
- **Risk Analysis**: Kill criteria, fragility points
- **Epistemic Check**: What we know vs assume vs speculate

#### 4. Recommendation Framework
- **Base Case**: Most likely outcome with probability
- **Bull Case**: Upside scenario with triggers
- **Bear Case**: Downside scenario with triggers
- **Action Items**: Specific next steps

#### 5. Appendices
- Detailed per-ticker analysis (if equity)
- Supporting data tables
- Verification summary (CoVe output)
- Assumption audit

### Visual Requirements

Include the following charts where applicable:
- Valuation comparison (peer multiples)
- Price chart with key levels (technical)
- Financial trends (revenue, margins, cash flow)
- Scenario analysis (bull/base/bear outcomes)

### Quality Checklist (Self-Verify Before Output)

Before producing final output, verify:
- [ ] Executive summary stands alone (reader gets key message)
- [ ] All numerical claims have sources
- [ ] Bull AND bear cases are balanced
- [ ] Recommendation is clear and actionable
- [ ] Charts are referenced in text
- [ ] Assumptions are flagged explicitly
- [ ] "So what?" answered for each section
```

#### 1.6.4 Report Template

```markdown
# [TOPIC] — Investment Analysis

**Date:** [YYYY-MM-DD]
**Analyst:** deepmind1 Multi-Agent System
**Run ID:** [run_id]

---

## Executive Summary

**RECOMMENDATION: [BUY / HOLD / SELL / PROCEED / WAIT / DECLINE]**

[2-3 sentence thesis explaining the recommendation]

| Metric | Value |
|--------|-------|
| Price Target / Decision Threshold | $XX - $XX |
| Confidence Level | [High / Medium / Low] |
| Time Horizon | [X months] |
| Primary Risk | [One-line risk description] |

---

## Investment Thesis

### The Opportunity
[Prose paragraph explaining the asymmetry or value proposition]

### Key Drivers
1. **[Driver 1]**: [Explanation]
2. **[Driver 2]**: [Explanation]
3. **[Driver 3]**: [Explanation]

### Why Now
[Prose paragraph on timing and catalysts]

### Differentiated View
[What consensus is missing; our edge]

---

## Analysis Summary

### Systems & Value Chain
[Summary from 01_systems agent]

**Key Finding:** [One-line takeaway]

### Fundamental Assessment
[Summary from 07_fundamental if equity; otherwise relevant quantitative analysis]

| Metric | Value | vs Peers | Assessment |
|--------|-------|----------|------------|
| [Metric 1] | X | Y | [Premium/Discount/Fair] |

**Key Finding:** [One-line takeaway]

### Technical Setup (if applicable)
[Summary from 08_technical]

| Level Type | Price | Significance |
|------------|-------|--------------|
| Entry Zone | $X - $Y | [Why] |
| Stop Loss | $Z | [Why] |
| Target | $W | [Why] |

### Risk Analysis
[Summary from 02_inversion]

**Kill Criteria:**
1. [Condition that would invalidate thesis]
2. [Condition that would invalidate thesis]

### Epistemic Audit
[Summary from 05_epistemic]

| Category | Count | Key Items |
|----------|-------|-----------|
| Known Facts | X | [List] |
| Assumptions | Y | [List highest-fragility] |
| Speculations | Z | [List] |

---

## Recommendation Framework

### Scenario Analysis

| Scenario | Probability | Outcome | Key Trigger |
|----------|-------------|---------|-------------|
| Bull | XX% | [Outcome] | [Trigger] |
| Base | XX% | [Outcome] | [Default path] |
| Bear | XX% | [Outcome] | [Trigger] |

### Action Items
1. **Immediate:** [Action]
2. **Near-term:** [Action]
3. **Monitor:** [What to watch]

---

## Appendices

### A. Detailed Ticker Analysis
[Per-ticker summaries from equity agents]

### B. Verification Summary
[CoVe output summary: X claims verified, Y revised, Z flagged]

### C. Data Sources
[List of data sources with timestamps]

### D. Agent Outputs
[Links to full agent output artifacts]

---

*This report was generated by deepmind1 multi-agent system.*
*Data as of: [timestamp]*
*Report version: 1.0*
```

#### 1.6.5 Plotting Skills Specification

The Reporting Agent has access to plotting skills for generating publication-quality visualizations.

**Library Stack:**
- **Primary:** `plotly` (interactive HTML charts, embeddable)
- **Secondary:** `matplotlib` (static PNG for PDF export)
- **Data:** `pandas` for data manipulation

**Chart Types by Use Case:**

| Use Case | Chart Type | Library | Output |
|----------|------------|---------|--------|
| Peer valuation | Horizontal bar | plotly | HTML + PNG |
| Price history | Candlestick/Line | plotly | HTML + PNG |
| Scenario outcomes | Waterfall/Tornado | plotly | HTML + PNG |
| Financial trends | Multi-line | matplotlib | PNG |
| Market share | Donut/Pie | plotly | HTML |
| Correlation matrix | Heatmap | plotly | HTML |
| Risk distribution | Box plot | plotly | HTML |

**Visual Style Guide:**

```python
# skills/plotting.py
CHART_STYLE = {
    "colors": {
        "primary": "#1f77b4",     # Blue for main series
        "secondary": "#ff7f0e",   # Orange for comparison
        "positive": "#2ca02c",    # Green for gains
        "negative": "#d62728",    # Red for losses
        "neutral": "#7f7f7f",     # Gray for context
        "accent": "#9467bd",      # Purple for highlights
    },
    "font": {
        "family": "Inter, Arial, sans-serif",
        "title_size": 16,
        "label_size": 12,
        "tick_size": 10,
    },
    "layout": {
        "background": "#ffffff",
        "grid_color": "#e5e5e5",
        "margin": {"l": 60, "r": 40, "t": 60, "b": 60},
    },
}
```

**Required Chart Functions:**

```python
# skills/plotting.py
from typing import List, Dict, Optional
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

class ReportPlotter:
    """Publication-quality charts for research reports."""

    def valuation_comparison(
        self,
        tickers: List[str],
        metrics: Dict[str, Dict[str, float]],  # {ticker: {metric: value}}
        metric_name: str = "P/E Ratio",
        highlight_ticker: Optional[str] = None,
    ) -> go.Figure:
        """Horizontal bar chart comparing valuation metrics across peers."""
        ...

    def price_chart(
        self,
        ticker: str,
        ohlcv: pd.DataFrame,
        support_levels: List[float] = [],
        resistance_levels: List[float] = [],
        moving_averages: List[int] = [50, 200],
    ) -> go.Figure:
        """Candlestick chart with technical levels."""
        ...

    def scenario_waterfall(
        self,
        base_value: float,
        scenarios: Dict[str, float],  # {scenario_name: impact}
        title: str = "Scenario Analysis",
    ) -> go.Figure:
        """Waterfall chart showing scenario impacts on base case."""
        ...

    def financial_trends(
        self,
        ticker: str,
        financials: pd.DataFrame,  # columns: date, revenue, net_income, etc.
        metrics: List[str] = ["revenue", "net_income"],
    ) -> go.Figure:
        """Multi-line chart of financial trends over time."""
        ...

    def risk_matrix(
        self,
        risks: List[Dict],  # [{name, probability, impact}]
        title: str = "Risk Assessment Matrix",
    ) -> go.Figure:
        """Scatter plot of risks by probability vs impact."""
        ...

    def confidence_gauge(
        self,
        confidence: float,  # 0.0 to 1.0
        label: str = "Overall Confidence",
    ) -> go.Figure:
        """Gauge chart showing confidence level."""
        ...

    def save_chart(
        self,
        fig: go.Figure,
        run_id: str,
        chart_name: str,
        formats: List[str] = ["html", "png"],
    ) -> Dict[str, str]:
        """Save chart to run folder in multiple formats."""
        paths = {}
        for fmt in formats:
            path = f"data/runs/{run_id}/charts/{chart_name}.{fmt}"
            if fmt == "html":
                fig.write_html(path)
            elif fmt == "png":
                fig.write_image(path, width=1200, height=600, scale=2)
            paths[fmt] = path
        return paths
```

**Chart Quality Checklist:**

| Criterion | Requirement |
|-----------|-------------|
| **Titles** | Descriptive, includes time period if applicable |
| **Axes** | Labeled with units, appropriate scale |
| **Legend** | Clear, not overlapping data |
| **Colors** | Consistent with style guide, colorblind-safe |
| **Annotations** | Key levels/events highlighted |
| **Source** | Data source noted in subtitle or caption |
| **Resolution** | PNG at 2x scale for print quality |

#### 1.6.6 Report Quality Gate

Before a report is marked as "shippable," it must pass automated and manual quality gates:

**Automated Checks:**

```python
# skills/report_quality.py
from typing import List, Tuple
from pydantic import BaseModel

class QualityCheckResult(BaseModel):
    check_name: str
    passed: bool
    message: str
    severity: str  # "blocker", "warning", "info"

def check_report_quality(report_md: str, run_id: str) -> List[QualityCheckResult]:
    """Run all quality checks on a report."""
    results = []

    # Structure checks
    results.append(check_required_sections(report_md))
    results.append(check_executive_summary_length(report_md))
    results.append(check_recommendation_present(report_md))

    # Content checks
    results.append(check_numerical_claims_sourced(report_md))
    results.append(check_bull_bear_balance(report_md))
    results.append(check_assumption_flags(report_md))

    # Visual checks
    results.append(check_charts_referenced(report_md, run_id))
    results.append(check_charts_exist(run_id))

    # CoVe checks
    results.append(check_cove_verification(run_id))

    return results

REQUIRED_SECTIONS = [
    "Executive Summary",
    "Investment Thesis",
    "Analysis Summary",
    "Recommendation Framework",
]

def check_required_sections(report_md: str) -> QualityCheckResult:
    """Verify all required sections are present."""
    missing = []
    for section in REQUIRED_SECTIONS:
        if section.lower() not in report_md.lower():
            missing.append(section)

    return QualityCheckResult(
        check_name="required_sections",
        passed=len(missing) == 0,
        message=f"Missing sections: {missing}" if missing else "All sections present",
        severity="blocker" if missing else "info",
    )

def check_bull_bear_balance(report_md: str) -> QualityCheckResult:
    """Ensure both bull and bear cases are discussed."""
    has_bull = "bull" in report_md.lower()
    has_bear = "bear" in report_md.lower()

    return QualityCheckResult(
        check_name="bull_bear_balance",
        passed=has_bull and has_bear,
        message="Both bull and bear cases present" if (has_bull and has_bear) else "Missing bull or bear case",
        severity="blocker" if not (has_bull and has_bear) else "info",
    )

def check_cove_verification(run_id: str) -> QualityCheckResult:
    """Check that CoVe was run and no core claims were contradicted."""
    # Query cove_runs table for this run
    # Check verdict != 'blocked'
    ...
```

**Quality Gate Thresholds:**

| Gate Level | Criteria | Action if Failed |
|------------|----------|------------------|
| **Blocker** | Missing required section, no recommendation, unverified core claims | Cannot ship; must fix |
| **Warning** | Missing bull/bear balance, unsourced numbers, no charts | Flag for review; can ship with acknowledgment |
| **Info** | Style suggestions, length recommendations | Logged; optional fix |

**Shippable Report Definition:**

A report is "shippable" when:
1. Zero **blocker** quality checks failed
2. All **core** CoVe claims are `Supported` or `Unverified with caveat`
3. Recommendation is explicit (not "further analysis needed")
4. At least one visual/chart is included
5. Executive summary is ≤ 1/2 page

### 1.7 Intake System (Form + Agent)

The Intake System ensures users provide sufficient context for agents to perform optimally. It combines a **structured form template** with an **Intake Agent** that can interactively gather missing context. All fields are **optional** but contribute to an **Intake Quality Score** that predicts analysis depth.

#### 1.7.1 Intake Form Template

```markdown
# Task Intake Form

> **Instructions:** Fill in as many fields as you can. All fields are optional,
> but more context = better analysis. The Intake Agent will review and may ask
> follow-up questions before the pipeline runs.

---

## 1. CORE REQUEST

### Title
<!-- Short, descriptive title for this analysis -->


### One-Line Ask
<!-- What do you want to know or decide? Complete this sentence:
     "Help me understand/decide/find..." -->


### Objective Type
<!-- Choose one: invest | build | explore | decide | invent -->


### Time Horizon
<!-- Choose one: days-weeks | months | 6-18 months | multi-year -->


---

## 2. CONTEXT & BACKGROUND

### Background Context
<!-- What led to this question? What's the situation?
     Include any relevant history, events, or market conditions. -->


### Domain/Industry
<!-- What sector, industry, or domain does this relate to?
     e.g., "rare earth minerals", "enterprise SaaS", "biotech" -->


### Geographic Focus
<!-- Any geographic constraints or focus areas?
     e.g., "US-listed only", "Asia-Pacific markets", "Global" -->


---

## 3. PRIOR THINKING

### Prior Hypotheses
<!-- What do you already believe or suspect? List your current hypotheses.
     Be honest—agents will stress-test these, not just confirm them.

     Example:
     - "MP Materials is undervalued due to US rare earth scarcity"
     - "The market is overestimating EV adoption speed" -->


### Information You Already Have
<!-- What research have you already done? What sources have you consulted?
     This avoids redundant work.

     Example:
     - "Read MP Materials 10-K, seems solid balance sheet"
     - "Spoke with industry expert who mentioned China export risks" -->


### Reference Materials
<!-- Paths to any files, reports, or data you want agents to consider.
     Leave blank if none.

     Example:
     - inputs/reference/mp_materials_10k.pdf
     - inputs/reference/rare_earth_industry_report.pdf -->


---

## 4. CONSTRAINTS & PREFERENCES

### Hard Constraints
<!-- Non-negotiable requirements. Agents will respect these strictly.

     Example:
     - "Public companies only"
     - "No exposure to China-domiciled companies"
     - "Budget under $50K" -->


### Soft Preferences
<!-- Nice-to-haves, but can be relaxed if needed.

     Example:
     - "Prefer US-listed over ADRs"
     - "Would like dividend-paying stocks" -->


### Non-Goals (Explicitly Out of Scope)
<!-- What should agents NOT spend time on?

     Example:
     - "Don't analyze lithium—already have exposure"
     - "Not interested in ETFs, individual stocks only" -->


---

## 5. RISK & DECISION FRAMEWORK

### Risk Appetite
<!-- Choose one: conservative | moderate | aggressive
     Or describe: "Can tolerate 20% drawdown for 3x upside potential" -->


### Decision Stakes
<!-- How important is this decision? What's at stake?

     Example:
     - "Deploying $100K of personal capital"
     - "Recommending to investment committee"
     - "Exploratory research, no immediate action" -->


### What Would Change Your Mind?
<!-- What evidence would make you abandon your current view?
     This helps Inversion and Epistemic agents focus.

     Example:
     - "If China lifts export restrictions, thesis breaks"
     - "If management sells >10% of holdings, red flag" -->


### Kill Criteria (Deal-Breakers)
<!-- Automatic disqualifiers. If true, don't proceed.

     Example:
     - "Debt/Equity > 2x"
     - "Insider selling in last 6 months"
     - "No US production capacity" -->


---

## 6. OUTPUT PREFERENCES

### Desired Depth
<!-- Choose one: quick-scan | standard | deep-dive | exhaustive -->


### Specific Questions to Answer
<!-- List specific questions you want addressed. Agents will ensure these
     are answered in the final report.

     Example:
     1. "What's the realistic TAM for rare earth in EVs by 2030?"
     2. "Who are MP Materials' main customers and contract terms?"
     3. "What happens if China bans exports entirely?" -->


### Comparison Requests
<!-- Want specific comparisons?

     Example:
     - "Compare MP Materials vs Lynas on valuation and production capacity"
     - "How does this opportunity compare to my current LTHM position?" -->


### Report Format Preferences
<!-- Any preferences for the final output?

     Example:
     - "Include technical chart with entry/exit levels"
     - "Want scenario analysis with probabilities"
     - "Keep executive summary under 1 page" -->


---

## 7. ADDITIONAL CONTEXT (FREE-FORM)

### Anything Else?
<!-- Anything that doesn't fit above but might be relevant.
     The more context, the better the analysis. -->


---

## INTAKE METADATA (Auto-filled)

- **Submitted at:** [timestamp]
- **Intake Quality Score:** [calculated after submission]
- **Missing High-Value Fields:** [list]
- **Intake Agent Review:** [pending/complete]
```

#### 1.7.2 Intake Agent Charter

The Intake Agent reviews submitted forms and interactively gathers missing context through targeted questions.

```markdown
## Charter: Intake Agent

You are the Intake Agent for deepmind1. Your role is to review user-submitted
task intake forms and gather additional context that will help downstream
agents perform better analysis.

### Core Principles

1. **Respect user time**: Ask only high-value questions
2. **Adapt to objective**: Different objectives need different context
3. **Don't interrogate**: 3-5 questions max per session
4. **Explain why**: Tell users why each question matters
5. **Accept "I don't know"**: Missing info is fine; flag it as assumption

### Review Process

1. **Parse submitted form** → Extract filled vs empty fields
2. **Calculate quality score** → Identify gaps
3. **Select questions** → Based on objective type and gaps
4. **Ask interactively** → One question at a time, conversational
5. **Synthesize** → Produce enriched TaskInput for Orchestrator

### Question Selection Logic

For each objective type, prioritize these fields:

**INVEST objectives:**
- MUST have: time_horizon, risk_appetite
- HIGH VALUE: prior_hypotheses, kill_criteria, what_would_change_mind
- HELPFUL: decision_stakes, comparison_requests

**BUILD objectives:**
- MUST have: constraints, time_horizon
- HIGH VALUE: non_goals, prior_hypotheses
- HELPFUL: reference_materials, specific_questions

**EXPLORE objectives:**
- MUST have: domain, specific_questions
- HIGH VALUE: prior_hypotheses, information_already_have
- HELPFUL: desired_depth

**DECIDE objectives:**
- MUST have: decision_stakes, time_horizon
- HIGH VALUE: kill_criteria, what_would_change_mind, constraints
- HELPFUL: risk_appetite, comparison_requests

### Question Templates

Use these templates, adapting tone to be conversational:

**For missing time_horizon:**
"What's your timeline for this? Are you looking at:
- Days to weeks (tactical)
- A few months (near-term)
- 6-18 months (medium-term)
- Multi-year (strategic)

This helps us calibrate how much weight to put on near-term catalysts vs long-term fundamentals."

**For missing risk_appetite:**
"How much volatility can you stomach? For context:
- Conservative: Prioritize capital preservation, accept lower returns
- Moderate: Balanced approach, can handle normal market swings
- Aggressive: Comfortable with significant drawdowns for higher upside

Or describe in your own terms—e.g., 'Can handle 30% drawdown if thesis intact.'"

**For missing prior_hypotheses:**
"What's your current thinking on this? Even half-formed hunches help.
Our agents will stress-test your hypotheses, not just confirm them.
If you're truly starting from zero, that's fine too—just say so."

**For missing what_would_change_mind:**
"What would make you walk away from this opportunity?
This helps our Inversion agent focus on the most decision-relevant risks.
Example: 'If I learned management was selling shares, I'd reconsider.'"

**For missing kill_criteria:**
"Are there any automatic deal-breakers?
Things that, if true, would immediately disqualify an option.
Example: 'No companies with debt/equity > 2x' or 'Must have US operations.'"

**For missing specific_questions:**
"Are there particular questions you want answered?
We'll make sure the final report addresses these explicitly.
Example: 'What's the bear case for this sector?' or 'How does X compare to Y?'"

### Output Format

After gathering context, produce an enriched intake summary:

```yaml
intake_summary:
  title: "[from form]"
  one_line_ask: "[from form or synthesized]"
  objective: "[invest|build|explore|decide|invent]"
  time_horizon: "[from form or gathered]"

  context_gathered:
    - field: "risk_appetite"
      value: "moderate - can handle 20% drawdown"
      source: "user response to question 2"
    - field: "prior_hypotheses"
      value: ["MP is undervalued", "China risk is overstated"]
      source: "original form"

  flags_for_orchestrator:
    - "User has existing LTHM position - note for Allocator"
    - "Explicit kill criterion: no China exposure"
    - "User wants technical entry levels in report"

  assumptions_from_gaps:
    - field: "geographic_focus"
      assumed: "US-listed"
      confidence: "medium"
      rationale: "User mentioned 'public companies' without specifying"

  quality_score: 0.78
  quality_notes: "Strong on constraints and hypotheses, light on risk framework"
```

### Interaction Style

- Be concise and friendly, not formal
- Use bullet points for options
- Acknowledge what they've already provided
- Don't repeat questions they've answered
- If they say "skip" or "I don't know", move on gracefully
```

#### 1.7.3 Intake Quality Score

The Intake Quality Score predicts how well agents can perform given the provided context. It's **informational, not blocking**—low scores generate warnings, not errors.

**Scoring Formula:**

```python
# skills/intake_quality.py
from typing import Dict, List, Optional
from pydantic import BaseModel
from enum import Enum

class FieldImportance(str, Enum):
    CRITICAL = "critical"      # 15 points
    HIGH = "high"              # 10 points
    MEDIUM = "medium"          # 5 points
    LOW = "low"                # 2 points

class ObjectiveType(str, Enum):
    INVEST = "invest"
    BUILD = "build"
    EXPLORE = "explore"
    DECIDE = "decide"
    INVENT = "invent"

# Field weights vary by objective type
FIELD_WEIGHTS: Dict[ObjectiveType, Dict[str, FieldImportance]] = {
    ObjectiveType.INVEST: {
        "one_line_ask": FieldImportance.CRITICAL,
        "time_horizon": FieldImportance.CRITICAL,
        "risk_appetite": FieldImportance.HIGH,
        "prior_hypotheses": FieldImportance.HIGH,
        "kill_criteria": FieldImportance.HIGH,
        "what_would_change_mind": FieldImportance.HIGH,
        "constraints": FieldImportance.MEDIUM,
        "domain": FieldImportance.MEDIUM,
        "decision_stakes": FieldImportance.MEDIUM,
        "background_context": FieldImportance.LOW,
        "non_goals": FieldImportance.LOW,
        "specific_questions": FieldImportance.LOW,
    },
    ObjectiveType.BUILD: {
        "one_line_ask": FieldImportance.CRITICAL,
        "constraints": FieldImportance.CRITICAL,
        "time_horizon": FieldImportance.HIGH,
        "non_goals": FieldImportance.HIGH,
        "prior_hypotheses": FieldImportance.MEDIUM,
        "reference_materials": FieldImportance.MEDIUM,
        "specific_questions": FieldImportance.MEDIUM,
        "background_context": FieldImportance.LOW,
        "domain": FieldImportance.LOW,
    },
    ObjectiveType.EXPLORE: {
        "one_line_ask": FieldImportance.CRITICAL,
        "domain": FieldImportance.CRITICAL,
        "specific_questions": FieldImportance.HIGH,
        "prior_hypotheses": FieldImportance.MEDIUM,
        "information_already_have": FieldImportance.MEDIUM,
        "desired_depth": FieldImportance.MEDIUM,
        "background_context": FieldImportance.LOW,
        "time_horizon": FieldImportance.LOW,
    },
    ObjectiveType.DECIDE: {
        "one_line_ask": FieldImportance.CRITICAL,
        "decision_stakes": FieldImportance.CRITICAL,
        "time_horizon": FieldImportance.HIGH,
        "kill_criteria": FieldImportance.HIGH,
        "what_would_change_mind": FieldImportance.HIGH,
        "constraints": FieldImportance.HIGH,
        "risk_appetite": FieldImportance.MEDIUM,
        "prior_hypotheses": FieldImportance.MEDIUM,
        "comparison_requests": FieldImportance.MEDIUM,
        "background_context": FieldImportance.LOW,
    },
    ObjectiveType.INVENT: {
        "one_line_ask": FieldImportance.CRITICAL,
        "constraints": FieldImportance.HIGH,
        "non_goals": FieldImportance.HIGH,
        "background_context": FieldImportance.MEDIUM,
        "prior_hypotheses": FieldImportance.MEDIUM,
        "reference_materials": FieldImportance.MEDIUM,
        "time_horizon": FieldImportance.LOW,
    },
}

IMPORTANCE_POINTS = {
    FieldImportance.CRITICAL: 15,
    FieldImportance.HIGH: 10,
    FieldImportance.MEDIUM: 5,
    FieldImportance.LOW: 2,
}

class IntakeQualityResult(BaseModel):
    score: float  # 0.0 to 1.0
    grade: str  # A, B, C, D, F
    points_earned: int
    points_possible: int
    filled_fields: List[str]
    missing_fields: List[Dict[str, str]]  # [{field, importance, impact}]
    warnings: List[str]
    suggestions: List[str]

def calculate_intake_quality(
    intake: Dict,
    objective: ObjectiveType
) -> IntakeQualityResult:
    """Calculate quality score for an intake form submission."""

    weights = FIELD_WEIGHTS.get(objective, FIELD_WEIGHTS[ObjectiveType.EXPLORE])

    points_earned = 0
    points_possible = 0
    filled_fields = []
    missing_fields = []

    for field, importance in weights.items():
        points = IMPORTANCE_POINTS[importance]
        points_possible += points

        value = intake.get(field)
        if value and str(value).strip():
            points_earned += points
            filled_fields.append(field)
        else:
            missing_fields.append({
                "field": field,
                "importance": importance.value,
                "impact": f"-{points} points",
            })

    score = points_earned / points_possible if points_possible > 0 else 0

    # Grade assignment
    if score >= 0.9:
        grade = "A"
    elif score >= 0.75:
        grade = "B"
    elif score >= 0.6:
        grade = "C"
    elif score >= 0.4:
        grade = "D"
    else:
        grade = "F"

    # Generate warnings for critical missing fields
    warnings = []
    for mf in missing_fields:
        if mf["importance"] == "critical":
            warnings.append(f"Missing critical field: {mf['field']}")

    # Generate suggestions
    suggestions = []
    high_value_missing = [mf for mf in missing_fields if mf["importance"] in ["critical", "high"]]
    if high_value_missing:
        suggestions.append(
            f"Consider adding: {', '.join(mf['field'] for mf in high_value_missing[:3])}"
        )

    if score < 0.5:
        suggestions.append(
            "Low context score may result in more assumptions and less specific analysis"
        )

    return IntakeQualityResult(
        score=round(score, 2),
        grade=grade,
        points_earned=points_earned,
        points_possible=points_possible,
        filled_fields=filled_fields,
        missing_fields=missing_fields,
        warnings=warnings,
        suggestions=suggestions,
    )
```

**Quality Score Interpretation:**

| Grade | Score | Interpretation | System Behavior |
|-------|-------|----------------|-----------------|
| **A** | ≥90% | Excellent context | Full analysis, minimal assumptions |
| **B** | 75-89% | Good context | Good analysis, few assumptions |
| **C** | 60-74% | Adequate context | Standard analysis, moderate assumptions |
| **D** | 40-59% | Limited context | Basic analysis, many assumptions flagged |
| **F** | <40% | Minimal context | Will run, but warns extensively |

**Example Output:**

```
┌─────────────────────────────────────────────────────────────┐
│                   INTAKE QUALITY REPORT                      │
├─────────────────────────────────────────────────────────────┤
│ Score: 72/100 (72%)                          Grade: C       │
├─────────────────────────────────────────────────────────────┤
│ ✓ Filled: one_line_ask, time_horizon, constraints,         │
│           prior_hypotheses, domain                           │
│                                                              │
│ ✗ Missing (High Value):                                      │
│   - risk_appetite (HIGH) → -10 pts                          │
│   - kill_criteria (HIGH) → -10 pts                          │
│   - what_would_change_mind (HIGH) → -10 pts                 │
│                                                              │
│ ⚠ Warnings:                                                  │
│   None                                                       │
│                                                              │
│ 💡 Suggestions:                                              │
│   - Consider adding: risk_appetite, kill_criteria           │
│   - Intake Agent can help gather missing context            │
├─────────────────────────────────────────────────────────────┤
│ [Continue with current input] [Run Intake Agent] [Edit Form]│
└─────────────────────────────────────────────────────────────┘
```

#### 1.7.4 Objective-Specific Question Sets

The Intake Agent adapts its questions based on the declared objective:

**INVEST Objective — Investment Analysis**
```yaml
required_context:
  - time_horizon: "Investment timeline affects valuation methods and catalyst importance"
  - risk_appetite: "Calibrates position sizing and stop-loss recommendations"

high_value_questions:
  - "What's your current portfolio exposure to this sector?"
  - "Are there specific valuation thresholds that would make this attractive?"
  - "What macro conditions would invalidate this thesis?"
  - "Do you have a target position size in mind?"

adaptive_questions:
  if_short_horizon:
    - "Are there near-term catalysts you're watching?"
    - "What's your exit trigger?"
  if_long_horizon:
    - "What structural trends support this investment?"
    - "How important is dividend/income vs appreciation?"
```

**BUILD Objective — Building/Creating Something**
```yaml
required_context:
  - constraints: "Technical, budget, timeline, resource constraints"
  - success_criteria: "How will you know if this succeeded?"

high_value_questions:
  - "What's the MVP vs full vision?"
  - "Who are the stakeholders and what do they care about?"
  - "What have you already tried or ruled out?"
  - "Are there existing solutions you're replacing or improving on?"

adaptive_questions:
  if_technical:
    - "What's the existing tech stack?"
    - "Any integration requirements?"
  if_process:
    - "Who needs to approve this?"
    - "What's the change management plan?"
```

**EXPLORE Objective — Research/Learning**
```yaml
required_context:
  - domain: "What area are you exploring?"
  - depth: "Surface scan or deep understanding?"

high_value_questions:
  - "What do you already know about this topic?"
  - "Are there specific aspects you're most curious about?"
  - "Who is the audience for this research?"
  - "What would make this exploration 'complete'?"

adaptive_questions:
  if_new_domain:
    - "Want a glossary of key terms included?"
    - "Should we map the key players/companies in this space?"
  if_familiar_domain:
    - "What's the specific angle you want to explore?"
    - "Any recent developments you want focus on?"
```

**DECIDE Objective — Making a Decision**
```yaml
required_context:
  - decision_stakes: "What's riding on this decision?"
  - options: "What are the alternatives you're considering?"

high_value_questions:
  - "What's the cost of being wrong?"
  - "What's the cost of delaying this decision?"
  - "Who else is involved in making this decision?"
  - "What information would make this decision obvious?"

adaptive_questions:
  if_reversible:
    - "If this doesn't work, what's the fallback?"
  if_irreversible:
    - "What's your confidence threshold for proceeding?"
    - "What additional diligence would increase confidence?"
```

#### 1.7.5 Intake Pipeline Integration

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER                                      │
└─────────────────────────────────────────────────────────────────┘
                              │
                    Submits intake form
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    INTAKE PARSER                                 │
│                                                                  │
│   - Validates markdown structure                                 │
│   - Extracts field values                                        │
│   - Calculates initial quality score                            │
│   - Identifies objective type                                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │ Score >= 75%?   │
                    └─────────────────┘
                     /              \
                   Yes              No
                   /                  \
                  ▼                    ▼
    ┌──────────────────┐    ┌──────────────────────────────────┐
    │ Skip to          │    │        INTAKE AGENT               │
    │ Orchestrator     │    │                                    │
    │ (user can still  │    │  - Reviews gaps                   │
    │  request agent)  │    │  - Asks 3-5 targeted questions    │
    └──────────────────┘    │  - User responds (or skips)       │
                            │  - Enriches TaskInput              │
                            │  - Recalculates quality score     │
                            └──────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ENRICHED TASK INPUT                          │
│                                                                  │
│   - All user-provided fields                                    │
│   - Agent-gathered context                                      │
│   - Flagged assumptions (from gaps)                             │
│   - Quality score + warnings                                    │
│   - Orchestration hints                                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       ORCHESTRATOR                               │
│                                                                  │
│   Receives enriched context, including:                         │
│   - intake_quality_score: 0.82                                  │
│   - assumptions_from_gaps: [...]                                │
│   - flags_for_agents: [...]                                     │
│   - user_specific_questions: [...]                              │
└─────────────────────────────────────────────────────────────────┘
```

**CLI Integration:**

```bash
# Run with intake form
python -m runner.run --intake inputs/my_task_intake.md

# Run with intake agent (interactive)
python -m runner.run --intake inputs/my_task_intake.md --intake-agent

# Skip intake agent even if score is low
python -m runner.run --intake inputs/my_task_intake.md --skip-intake-agent

# Show quality score without running pipeline
python -m runner.run --intake inputs/my_task_intake.md --check-intake-only
```

#### 1.7.6 Intake Agent Model Configuration

| Agent | Model | Thinking Mode | Rationale |
|-------|-------|---------------|-----------|
| **Intake Agent** | Sonnet 4 | Standard | Conversational, structured extraction, no deep reasoning needed |

```python
# Add to config/models.py
AGENT_MODEL_CONFIG["intake"] = AgentModelConfig(
    model="claude-sonnet-4-20250514",
    thinking=ThinkingMode.STANDARD,
    temperature=0.7,  # Slightly higher for conversational warmth
    max_output_tokens=2048,
)
```

### 1.8 Key Design Principles

1. **Separation of Concerns:** Reasoning agents decide *what matters*; skills generate *truthful artifacts*; reporting tells *coherent stories from verified outputs*
2. **Auditability:** Every decision has a traceable provenance chain with hashes and timestamps
3. **Reproducibility:** Charter hashes, input/output hashes, and state snapshots enable exact reproduction
4. **No Hallucinated Evidence:** Agents cannot invent figures, data, or citations
5. **Graceful Degradation:** System runs with minimal input; assumptions are explicit and confidence-tagged

### 1.9 Orchestrator Charter

The Orchestrator is the central coordinator of the pipeline. This charter defines its decision-making logic, agent selection criteria, and synthesis responsibilities.

#### 1.9.1 Orchestrator Responsibilities

```markdown
## Charter: Orchestrator Agent

You are the Orchestrator for deepmind1. You coordinate the multi-agent analysis
pipeline, making decisions about which agents to invoke, how to resolve conflicts,
and when to iterate for deeper analysis.

### Core Responsibilities

1. **Input Normalization** - Parse enriched TaskInput from Intake
2. **Agent Selection** - Choose relevant agents based on objective type
3. **Parallel Dispatch** - Send task context to selected agents
4. **Synthesis** - Aggregate and reconcile agent outputs
5. **Conflict Resolution** - Resolve disagreements between agents
6. **Sequential Planning** - Plan deep-dives based on initial findings
7. **Iteration Control** - Decide when to iterate vs terminate
8. **CoVe Triggering** - Determine when verification is needed
9. **Reporting Handoff** - Prepare synthesized context for Reporting agent

### Decision Framework

You must make decisions at each pipeline stage. Document your reasoning.
```

#### 1.9.2 Agent Selection Logic

The Orchestrator selects agents based on objective type and task requirements:

```python
# runner/orchestrator.py
from typing import List, Set
from enum import Enum

class AgentCategory(str, Enum):
    STRATEGIC = "strategic"      # 01-04
    EQUITY = "equity"            # 06-08
    META = "meta"                # 05
    COVE = "cove"                # CoVe agents

# Agent Selection Matrix by Objective
AGENT_SELECTION_MATRIX = {
    "invest": {
        "required": ["01_systems", "02_inversion", "03_allocator", "05_epistemic"],
        "conditional": {
            "06_screener": "if task mentions stocks/tickers/equity",
            "07_fundamental": "if screener returns tickers",
            "08_technical": "if screener returns tickers",
            "04_incentives": "if stakeholder dynamics mentioned",
        },
        "skip": [],
    },
    "build": {
        "required": ["01_systems", "02_inversion", "05_epistemic"],
        "conditional": {
            "04_incentives": "if stakeholders/politics mentioned",
        },
        "skip": ["03_allocator", "06_screener", "07_fundamental", "08_technical"],
    },
    "explore": {
        "required": ["01_systems", "05_epistemic"],
        "conditional": {
            "02_inversion": "if risks/downsides requested",
            "04_incentives": "if stakeholders mentioned",
        },
        "skip": ["03_allocator", "06_screener", "07_fundamental", "08_technical"],
    },
    "decide": {
        "required": ["01_systems", "02_inversion", "03_allocator", "05_epistemic"],
        "conditional": {
            "04_incentives": "always for decisions",
        },
        "skip": ["06_screener", "07_fundamental", "08_technical"],
    },
    "invent": {
        "required": ["01_systems", "02_inversion", "05_epistemic"],
        "conditional": {
            "04_incentives": "if market dynamics relevant",
        },
        "skip": ["03_allocator", "06_screener", "07_fundamental", "08_technical"],
    },
}

def select_agents(objective: str, task_input: dict) -> List[str]:
    """Select agents based on objective and task content."""
    matrix = AGENT_SELECTION_MATRIX.get(objective, AGENT_SELECTION_MATRIX["explore"])

    agents = list(matrix["required"])

    # Evaluate conditional agents
    task_text = str(task_input).lower()
    for agent, condition in matrix["conditional"].items():
        if evaluate_condition(condition, task_text, task_input):
            agents.append(agent)

    return agents

def evaluate_condition(condition: str, task_text: str, task_input: dict) -> bool:
    """Evaluate whether a conditional agent should be included."""
    if "stocks" in condition and any(kw in task_text for kw in ["stock", "ticker", "equity", "company"]):
        return True
    if "screener returns" in condition:
        # Check if screener has already run and returned tickers
        return task_input.get("_screener_tickers", []) != []
    if "stakeholder" in condition and "stakeholder" in task_text:
        return True
    if "always" in condition:
        return True
    return False
```

#### 1.9.3 Orchestrator Synthesis Protocol

After parallel pass, the Orchestrator must synthesize agent outputs:

```markdown
### Synthesis Steps

1. **Collect Outputs** - Gather all agent markdown outputs
2. **Extract Key Findings** - Identify main conclusions per agent
3. **Detect Conflicts** - Find contradictions between agents
4. **Prioritize Findings** - Rank by confidence and relevance
5. **Plan Deep-Dives** - Identify areas needing more analysis
6. **Update State** - Populate PipelineState with findings

### Synthesis Output Format

```yaml
synthesis:
  key_findings:
    - finding: "Core thesis from Systems analysis"
      source: "01_systems"
      confidence: "high"
    - finding: "Key risk from Inversion"
      source: "02_inversion"
      confidence: "medium"

  conflicts:
    - topic: "Valuation premium justified?"
      positions:
        03_allocator: "Premium too high, wait for pullback"
        07_fundamental: "Premium justified by growth"
      resolution_needed: true

  deep_dive_plan:
    - action: "Per-ticker fundamental analysis"
      tickers: ["MP", "LTHM", "ALB"]
      agents: ["07_fundamental", "08_technical"]
    - action: "Stress test China scenario"
      agents: ["02_inversion"]

  open_questions:
    - question: "What's the timeline for DOE subsidies?"
      owner: "01_systems"
      priority: "high"

  cove_triggers:
    - agent: "07_fundamental"
      reason: "Numerical claims about P/E ratios"
```
```

#### 1.9.4 Iteration Control Logic

```python
# runner/orchestrator.py
class IterationDecision(BaseModel):
    should_iterate: bool
    reason: str
    focus_areas: List[str]
    max_iterations_remaining: int

def decide_iteration(
    state: PipelineState,
    synthesis: dict,
    current_iteration: int,
    max_iterations: int = 2
) -> IterationDecision:
    """Decide whether to run another iteration."""

    # Stop conditions
    if current_iteration >= max_iterations:
        return IterationDecision(
            should_iterate=False,
            reason="Max iterations reached",
            focus_areas=[],
            max_iterations_remaining=0,
        )

    # Check for unresolved critical conflicts
    critical_conflicts = [c for c in synthesis.get("conflicts", [])
                         if c.get("resolution_needed")]

    # Check for high-priority open questions
    critical_questions = [q for q in synthesis.get("open_questions", [])
                         if q.get("priority") == "high"]

    # Check for CoVe failures
    cove_failures = [r for r in state.cove_results
                    if r.verdict == "contradicted" and r.claim_type == "core"]

    should_iterate = bool(critical_conflicts or critical_questions or cove_failures)

    return IterationDecision(
        should_iterate=should_iterate,
        reason=_build_iteration_reason(critical_conflicts, critical_questions, cove_failures),
        focus_areas=_identify_focus_areas(synthesis),
        max_iterations_remaining=max_iterations - current_iteration - 1,
    )
```

#### 1.9.5 CoVe Trigger Decision

```python
# runner/orchestrator.py
COVE_TRIGGER_RULES = {
    "01_systems": {
        "auto_trigger": False,
        "conditions": ["explicit user request"],
    },
    "02_inversion": {
        "auto_trigger": True,
        "conditions": ["kill criteria assertions", "probability claims"],
    },
    "03_allocator": {
        "auto_trigger": True,
        "conditions": ["numerical thresholds", "return expectations"],
    },
    "04_incentives": {
        "auto_trigger": False,
        "conditions": ["explicit user request"],
    },
    "05_epistemic": {
        "auto_trigger": False,  # Meta-agent, self-verifying
        "conditions": [],
    },
    "06_screener": {
        "auto_trigger": False,  # Outputs lists, not claims
        "conditions": [],
    },
    "07_fundamental": {
        "auto_trigger": True,
        "conditions": ["valuation figures", "financial ratios", "price targets"],
    },
    "08_technical": {
        "auto_trigger": False,  # Levels derived from data
        "conditions": ["explicit user request"],
    },
    "reporting": {
        "auto_trigger": True,  # Always verify before shipping
        "conditions": ["final report generation"],
    },
}

def should_trigger_cove(agent_name: str, output: str) -> bool:
    """Determine if CoVe should run on agent output."""
    rules = COVE_TRIGGER_RULES.get(agent_name, {"auto_trigger": False})

    if not rules["auto_trigger"]:
        return False

    # Check for trigger conditions in output
    conditions = rules.get("conditions", [])
    output_lower = output.lower()

    for condition in conditions:
        if "numerical" in condition and _has_numerical_claims(output):
            return True
        if "valuation" in condition and any(kw in output_lower for kw in ["p/e", "ev/ebitda", "dcf", "valuation"]):
            return True
        if "kill criteria" in condition and "kill" in output_lower:
            return True
        if "final report" in condition:
            return True

    return False
```

#### 1.9.6 Stop Conditions

The Orchestrator stops the pipeline when:

| Condition | Action | Reason |
|-----------|--------|--------|
| Max iterations reached | Stop, generate report | Resource limit |
| All open questions resolved | Stop, generate report | Analysis complete |
| No conflicts remaining | Stop, generate report | Consensus achieved |
| CoVe core claim contradicted (unresolvable) | Stop with warning | Cannot ship invalid claims |
| Budget exceeded | Stop with partial report | Cost limit |
| User cancellation | Stop immediately | User request |

### 1.10 Agent Data Contracts

Each agent has a defined input/output contract to ensure chain of custody.

#### 1.10.1 Universal Agent Input

All agents receive a standardized context package:

```python
# schemas/agent_input.py
from pydantic import BaseModel
from typing import List, Dict, Optional, Any

class AgentContext(BaseModel):
    """Universal input context for all agents."""

    # Task Context
    run_id: str
    task_title: str
    one_line_ask: str
    objective: str
    time_horizon: str
    constraints: List[str]
    background_context: Optional[str]
    prior_hypotheses: Optional[str]

    # User Preferences
    risk_appetite: Optional[str]
    kill_criteria: List[str]
    specific_questions: List[str]

    # Pipeline Context
    iteration_number: int
    previous_agent_outputs: Dict[str, str]  # agent_name -> summary
    orchestrator_guidance: Optional[str]     # Specific instructions for this call

    # Data Context (populated by skills before agent call)
    market_data: Optional[Dict[str, Any]]    # If equity analysis
    web_search_results: Optional[List[Dict]] # If web search ran
    reference_materials: Optional[str]       # Parsed reference docs

    # State Context
    current_candidates: List[Dict]
    current_assumptions: List[Dict]
    current_conflicts: List[Dict]
    open_questions: List[Dict]
```

#### 1.10.2 Per-Agent Output Schemas

**01_Systems Output:**
```python
class SystemsOutput(BaseModel):
    """Required output structure for 01_systems agent."""

    system_map: str                    # Markdown describing system dynamics
    value_chain: List[Dict[str, str]]  # [{node, role, value_capture}]
    feedback_loops: List[Dict]         # Identified feedback mechanisms
    second_order_effects: List[str]    # Non-obvious consequences
    bottlenecks: List[str]             # Constraints and chokepoints
    key_dependencies: List[str]        # Critical dependencies

    # Required sections in markdown
    required_sections: ClassVar[List[str]] = [
        "System Overview",
        "Value Chain Analysis",
        "Second-Order Effects",
        "Key Bottlenecks",
    ]
```

**02_Inversion Output:**
```python
class InversionOutput(BaseModel):
    """Required output structure for 02_inversion agent."""

    kill_criteria: List[Dict[str, str]]     # [{criterion, trigger, severity}]
    failure_modes: List[Dict]               # How this could fail
    fragility_analysis: Dict[str, int]      # {factor: fragility_score 1-5}
    downside_scenarios: List[Dict]          # Bear cases
    mitigations: List[Dict[str, str]]       # [{risk, mitigation}]

    required_sections: ClassVar[List[str]] = [
        "Kill Criteria",
        "Failure Modes",
        "Fragility Assessment",
        "Downside Scenarios",
        "Mitigations",
    ]
```

**03_Allocator Output:**
```python
class AllocatorOutput(BaseModel):
    """Required output structure for 03_allocator agent."""

    opportunity_cost: str                   # What else could capital do
    alternatives: List[Dict[str, str]]      # [{alternative, pros, cons}]
    position_sizing: Optional[Dict]         # If invest objective
    decision_thresholds: List[Dict]         # When to act
    required_return: Optional[float]        # Hurdle rate
    portfolio_fit: Optional[str]            # How it fits existing portfolio

    required_sections: ClassVar[List[str]] = [
        "Opportunity Cost",
        "Alternatives Analysis",
        "Decision Framework",
    ]
```

**05_Epistemic Output:**
```python
class EpistemicOutput(BaseModel):
    """Required output structure for 05_epistemic agent."""

    know_assume_speculate: Dict[str, List[str]]  # Categorized claims
    overconfidence_flags: List[str]              # Claims that seem too certain
    data_quality_issues: List[str]               # Data reliability concerns
    assumption_audit: List[Dict]                 # [{assumption, fragility, source}]
    confidence_calibration: Dict[str, str]       # Suggested confidence levels

    required_sections: ClassVar[List[str]] = [
        "What We Know",
        "What We Assume",
        "What We Speculate",
        "Overconfidence Alerts",
        "Data Quality Assessment",
    ]
```

**06_Screener Output:**
```python
class ScreenerOutput(BaseModel):
    """Required output structure for 06_screener agent."""

    universe: List[Dict]                    # All identified tickers
    pure_play: List[Dict[str, str]]        # [{ticker, company, rationale}]
    diversified: List[Dict[str, str]]      # [{ticker, company, exposure_pct}]
    excluded: List[Dict[str, str]]         # [{ticker, reason}]
    shortlist: List[str]                   # Top tickers for deep-dive
    sector_dynamics: str                   # Sector overview

    required_sections: ClassVar[List[str]] = [
        "Sector Overview",
        "Pure-Play Exposure",
        "Diversified Exposure",
        "Excluded Tickers",
        "Shortlist for Deep-Dive",
    ]
```

**07_Fundamental Output:**
```python
class FundamentalOutput(BaseModel):
    """Required output structure for 07_fundamental agent."""

    ticker: str
    valuation_summary: Dict[str, Any]       # Metrics table
    dcf_range: Optional[Dict[str, float]]   # {low, mid, high}
    earnings_quality: str                   # Assessment
    balance_sheet_risks: List[str]
    bull_case: Dict[str, Any]
    bear_case: Dict[str, Any]
    base_case: Dict[str, Any]
    key_assumptions: List[str]              # Flagged assumptions

    required_sections: ClassVar[List[str]] = [
        "Valuation Summary",
        "Earnings Quality",
        "Balance Sheet Assessment",
        "Bull Case",
        "Bear Case",
        "Key Assumptions",
    ]
```

**08_Technical Output:**
```python
class TechnicalOutput(BaseModel):
    """Required output structure for 08_technical agent."""

    ticker: str
    trend_assessment: Dict[str, str]        # {primary, secondary, strength}
    key_levels: List[Dict]                  # [{type, price, significance}]
    momentum_indicators: Dict[str, Any]     # RSI, MACD, etc.
    volume_analysis: str
    entry_zones: List[Dict[str, float]]     # Suggested accumulation
    exit_zones: List[Dict[str, float]]      # Take profit levels
    stop_loss: Dict[str, float]             # Risk management

    required_sections: ClassVar[List[str]] = [
        "Trend Assessment",
        "Key Levels",
        "Momentum Analysis",
        "Entry/Exit Zones",
    ]
```

#### 1.10.3 Output Validation

```python
# skills/output_validation.py
from typing import Type
from pydantic import BaseModel, ValidationError

AGENT_OUTPUT_SCHEMAS = {
    "01_systems": SystemsOutput,
    "02_inversion": InversionOutput,
    "03_allocator": AllocatorOutput,
    "04_incentives": IncentivesOutput,
    "05_epistemic": EpistemicOutput,
    "06_screener": ScreenerOutput,
    "07_fundamental": FundamentalOutput,
    "08_technical": TechnicalOutput,
}

class OutputValidationResult(BaseModel):
    valid: bool
    agent_name: str
    missing_sections: List[str]
    parse_errors: List[str]
    warnings: List[str]

def validate_agent_output(agent_name: str, output_markdown: str) -> OutputValidationResult:
    """Validate that agent output contains required sections."""

    schema = AGENT_OUTPUT_SCHEMAS.get(agent_name)
    if not schema:
        return OutputValidationResult(
            valid=True,
            agent_name=agent_name,
            missing_sections=[],
            parse_errors=["No schema defined for agent"],
            warnings=[],
        )

    required_sections = getattr(schema, "required_sections", [])
    output_lower = output_markdown.lower()

    missing = []
    for section in required_sections:
        if section.lower() not in output_lower:
            missing.append(section)

    return OutputValidationResult(
        valid=len(missing) == 0,
        agent_name=agent_name,
        missing_sections=missing,
        parse_errors=[],
        warnings=[f"Missing {len(missing)} required sections"] if missing else [],
    )
```

### 1.11 Agent Selection Matrix

Quick reference for which agents are relevant for each objective type:

| Agent | INVEST | BUILD | EXPLORE | DECIDE | INVENT |
|-------|--------|-------|---------|--------|--------|
| **01 Systems** | ✓ Required | ✓ Required | ✓ Required | ✓ Required | ✓ Required |
| **02 Inversion** | ✓ Required | ✓ Required | ○ Conditional | ✓ Required | ✓ Required |
| **03 Allocator** | ✓ Required | ✗ Skip | ✗ Skip | ✓ Required | ✗ Skip |
| **04 Incentives** | ○ Conditional | ○ Conditional | ○ Conditional | ✓ Required | ○ Conditional |
| **05 Epistemic** | ✓ Required | ✓ Required | ✓ Required | ✓ Required | ✓ Required |
| **06 Screener** | ○ If equity | ✗ Skip | ✗ Skip | ✗ Skip | ✗ Skip |
| **07 Fundamental** | ○ Per ticker | ✗ Skip | ✗ Skip | ✗ Skip | ✗ Skip |
| **08 Technical** | ○ Per ticker | ✗ Skip | ✗ Skip | ✗ Skip | ✗ Skip |

**Legend:**
- ✓ Required: Always runs for this objective
- ○ Conditional: Runs if specific conditions met
- ✗ Skip: Not relevant for this objective

**Conditional Triggers:**

| Agent | Trigger Condition |
|-------|-------------------|
| 04 Incentives | Task mentions stakeholders, politics, power dynamics |
| 06 Screener | Task mentions stocks, tickers, equity, companies, or sector |
| 07 Fundamental | Screener returns tickers in shortlist |
| 08 Technical | Screener returns tickers in shortlist |
| 02 Inversion (EXPLORE) | Task explicitly requests risk analysis |

### 1.12 Conflict Resolution Protocol

When agents disagree, the Orchestrator follows this resolution protocol:

#### 1.12.1 Conflict Detection

```python
# skills/conflicts.py
from typing import List, Dict
from pydantic import BaseModel

class ConflictType(str, Enum):
    FACTUAL = "factual"           # Disagreement on facts
    INTERPRETIVE = "interpretive" # Same facts, different conclusions
    VALUATION = "valuation"       # Different valuations
    TIMING = "timing"             # Different timing views
    RISK = "risk"                 # Different risk assessments

class DetectedConflict(BaseModel):
    conflict_id: str
    conflict_type: ConflictType
    topic: str
    agents_involved: List[str]
    positions: Dict[str, str]     # {agent: position}
    severity: str                 # "critical", "moderate", "minor"
    resolution_required: bool
    suggested_resolution: Optional[str]

def detect_conflicts(agent_outputs: Dict[str, str]) -> List[DetectedConflict]:
    """Scan agent outputs for contradictions."""
    conflicts = []

    # Compare each pair of agents
    agents = list(agent_outputs.keys())
    for i, agent_a in enumerate(agents):
        for agent_b in agents[i+1:]:
            output_a = agent_outputs[agent_a]
            output_b = agent_outputs[agent_b]

            # Check for valuation conflicts (Allocator vs Fundamental)
            if "03_allocator" in [agent_a, agent_b] and "07_fundamental" in [agent_a, agent_b]:
                conflicts.extend(_check_valuation_conflict(agent_a, output_a, agent_b, output_b))

            # Check for risk assessment conflicts (Inversion vs others)
            if "02_inversion" in [agent_a, agent_b]:
                conflicts.extend(_check_risk_conflict(agent_a, output_a, agent_b, output_b))

    return conflicts
```

#### 1.12.2 Resolution Strategies

| Conflict Type | Resolution Strategy | Decision Authority |
|---------------|--------------------|--------------------|
| **Factual** | Verify via CoVe or market data | CoVe Verifier |
| **Interpretive** | Present both views in report | User decides |
| **Valuation** | Show range (agent A low, agent B high) | Report both |
| **Timing** | Present as scenario analysis | User decides |
| **Risk** | Default to more conservative view | Inversion wins |

#### 1.12.3 Resolution Protocol

```markdown
### Conflict Resolution Steps

1. **Identify Conflict** - Detect contradiction between agents
2. **Classify Type** - Factual, interpretive, valuation, timing, risk
3. **Assess Severity** - Critical (blocks recommendation), Moderate, Minor
4. **Apply Resolution Strategy:**
   - **Factual conflicts** → Route to CoVe for verification
   - **Interpretive conflicts** → Document both views, flag for user
   - **Valuation conflicts** → Present range with sources
   - **Risk conflicts** → Bias toward conservative (Inversion) view
5. **Document Resolution** - Record in PipelineState
6. **Update Recommendation** - Adjust confidence based on conflicts

### Unresolvable Conflicts

If conflict cannot be resolved:
1. Flag as "Open Conflict" in report
2. Present both positions clearly
3. Reduce overall confidence score
4. Request user guidance in report

### Example Conflict Resolution

**Conflict:** 03_Allocator says "too expensive at $28" vs 07_Fundamental says "fair value is $32"

**Resolution:**
- Type: Valuation
- Strategy: Present range
- Output: "Valuation range: $28 (conservative, Allocator) to $32 (base case, Fundamental).
  Entry below $26 provides margin of safety per both views."
```

#### 1.12.4 Conflict Hierarchy

When conflicts must be resolved with a "winner," apply this hierarchy:

| Scenario | Winning Agent | Rationale |
|----------|---------------|-----------|
| Risk vs Opportunity | 02_Inversion | Conservative default |
| Data vs Interpretation | CoVe result | Facts over opinion |
| Valuation disagreement | Lower valuation | Margin of safety |
| Timing disagreement | Longer timeline | Conservative default |
| Assumptions conflict | 05_Epistemic | Meta-analysis authority |

### 1.13 Checkpoint & Resume Protocol

The pipeline supports checkpointing for recovery from failures.

#### 1.13.1 Checkpoint Schema

```python
# runner/checkpoint.py
from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime

class CheckpointStage(str, Enum):
    INTAKE_COMPLETE = "intake_complete"
    PARALLEL_COMPLETE = "parallel_complete"
    SYNTHESIS_COMPLETE = "synthesis_complete"
    DEEPDIVE_COMPLETE = "deepdive_complete"
    COVE_COMPLETE = "cove_complete"
    REPORT_COMPLETE = "report_complete"

class Checkpoint(BaseModel):
    checkpoint_id: str
    run_id: str
    stage: CheckpointStage
    timestamp: datetime
    state_snapshot: Dict          # Serialized PipelineState
    agent_outputs: Dict[str, str] # Completed agent outputs
    pending_agents: List[str]     # Agents not yet run
    iteration: int
    recoverable: bool
    error_context: Optional[str]  # If checkpoint due to error

def save_checkpoint(run_id: str, stage: CheckpointStage, state: PipelineState) -> str:
    """Save a checkpoint for potential resume."""
    checkpoint = Checkpoint(
        checkpoint_id=generate_id(),
        run_id=run_id,
        stage=stage,
        timestamp=datetime.now(),
        state_snapshot=state.model_dump(),
        agent_outputs=_collect_agent_outputs(run_id),
        pending_agents=_get_pending_agents(state),
        iteration=state.run_log.iterations_used,
        recoverable=True,
    )

    # Save to database
    db.execute("""
        INSERT INTO checkpoints (checkpoint_id, run_id, stage, data, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, [checkpoint.checkpoint_id, run_id, stage.value,
          checkpoint.model_dump_json(), checkpoint.timestamp])

    return checkpoint.checkpoint_id
```

#### 1.13.2 Resume Logic

```python
# runner/checkpoint.py
def resume_from_checkpoint(run_id: str, checkpoint_id: Optional[str] = None) -> PipelineState:
    """Resume a pipeline run from the last checkpoint."""

    if checkpoint_id:
        checkpoint = load_checkpoint(checkpoint_id)
    else:
        # Find latest checkpoint for this run
        checkpoint = get_latest_checkpoint(run_id)

    if not checkpoint:
        raise ValueError(f"No checkpoint found for run {run_id}")

    if not checkpoint.recoverable:
        raise ValueError(f"Checkpoint {checkpoint.checkpoint_id} is not recoverable")

    # Restore state
    state = PipelineState(**checkpoint.state_snapshot)

    # Log resume
    logger.info("pipeline_resume",
                run_id=run_id,
                checkpoint=checkpoint.checkpoint_id,
                stage=checkpoint.stage,
                pending_agents=checkpoint.pending_agents)

    return state, checkpoint.stage, checkpoint.pending_agents
```

#### 1.13.3 CLI Integration

```bash
# Resume from last checkpoint
python -m runner.run --resume <run_id>

# Resume from specific checkpoint
python -m runner.run --resume <run_id> --checkpoint <checkpoint_id>

# List checkpoints for a run
python -m runner.run --list-checkpoints <run_id>
```

### 1.14 Output Summarization Protocol

Before passing to Reporting, agent outputs are summarized to manage context limits.

#### 1.14.1 Summarization Strategy

```python
# skills/summarization.py
MAX_TOKENS_PER_AGENT = 1500  # Summarized output limit
MAX_TOTAL_CONTEXT = 12000    # Total context for Reporting agent

class AgentSummary(BaseModel):
    agent_name: str
    key_findings: List[str]      # Top 3-5 findings
    recommendation: Optional[str]
    confidence: str              # high/medium/low
    conflicts_raised: List[str]
    open_questions: List[str]
    full_output_path: str        # Path to complete output

def summarize_for_reporting(agent_outputs: Dict[str, str]) -> Dict[str, AgentSummary]:
    """Summarize agent outputs for Reporting agent context."""
    summaries = {}

    for agent_name, output in agent_outputs.items():
        # Extract key sections
        key_findings = extract_key_findings(output, max_items=5)
        recommendation = extract_recommendation(output)
        conflicts = extract_conflicts_raised(output)
        questions = extract_open_questions(output)

        summaries[agent_name] = AgentSummary(
            agent_name=agent_name,
            key_findings=key_findings,
            recommendation=recommendation,
            confidence=assess_confidence(output),
            conflicts_raised=conflicts,
            open_questions=questions,
            full_output_path=f"data/runs/{run_id}/{agent_name}.md",
        )

    return summaries

def build_reporting_context(summaries: Dict[str, AgentSummary], state: PipelineState) -> str:
    """Build context package for Reporting agent."""
    context_parts = []

    # Add orchestrator synthesis
    context_parts.append("## Orchestrator Synthesis\n" + state.orchestrator_synthesis)

    # Add agent summaries
    context_parts.append("## Agent Summaries\n")
    for agent_name, summary in summaries.items():
        context_parts.append(f"### {agent_name}\n")
        context_parts.append(f"**Key Findings:**\n")
        for finding in summary.key_findings:
            context_parts.append(f"- {finding}\n")
        if summary.recommendation:
            context_parts.append(f"**Recommendation:** {summary.recommendation}\n")
        context_parts.append(f"**Confidence:** {summary.confidence}\n")

    # Add conflicts
    if state.conflicts:
        context_parts.append("## Open Conflicts\n")
        for conflict in state.conflicts:
            context_parts.append(f"- {conflict.topic}: {conflict.agent_positions}\n")

    # Add decisions
    if state.decisions.recommendation:
        context_parts.append(f"## Preliminary Recommendation\n{state.decisions.recommendation}\n")

    return "\n".join(context_parts)
```

### 1.15 Key Design Principles (Updated)

1. **Separation of Concerns:** Reasoning agents decide *what matters*; skills generate *truthful artifacts*; reporting tells *coherent stories from verified outputs*
2. **Auditability:** Every decision has a traceable provenance chain with hashes and timestamps
3. **Reproducibility:** Charter hashes, input/output hashes, and state snapshots enable exact reproduction
4. **No Hallucinated Evidence:** Agents cannot invent figures, data, or citations
5. **Graceful Degradation:** System runs with minimal input; assumptions are explicit and confidence-tagged
6. **Chain of Custody:** Every data handoff between components is explicitly defined
7. **Fail-Safe Defaults:** When agents conflict, bias toward conservative interpretation
8. **Resumability:** Pipeline can recover from failures via checkpoints

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
| **Reporting** | Sonnet 4 | Standard | — | Synthesis, narrative writing, Amazon memo style; structured output with templates |

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
    # CoVe Agents (Phase 2C)
    "cove_generator": AgentModelConfig(
        model="claude-sonnet-4-20250514",
        thinking=ThinkingMode.STANDARD,
    ),
    "cove_skeptic": AgentModelConfig(
        model="claude-opus-4-5-20250514",
        thinking=ThinkingMode.EXTENDED,
        max_thinking_tokens=6000,
    ),
    "cove_verifier": AgentModelConfig(
        model="claude-opus-4-5-20250514",
        thinking=ThinkingMode.EXTENDED,
        max_thinking_tokens=8000,
    ),
    "cove_editor": AgentModelConfig(
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
- [ ] `charters/orchestrator.md` - Full Orchestrator charter with:
  - [ ] Agent selection logic (objective → agent mapping)
  - [ ] Synthesis protocol
  - [ ] Iteration control logic
  - [ ] CoVe trigger rules
  - [ ] Stop conditions
- [ ] `runner/orchestrator.py` - Orchestrator implementation
  - [ ] `select_agents()` function per selection matrix
  - [ ] `synthesize_outputs()` function
  - [ ] `decide_iteration()` function
  - [ ] `should_trigger_cove()` function
- [ ] `skills/conflicts.py` - Conflict detection
  - [ ] `detect_conflicts()` function
  - [ ] Conflict type classification
  - [ ] Resolution strategy selection
- [ ] Sequential plan generation
- [ ] Notebook: `03_phase1_parallel_then_synth.ipynb`

**Validation Checkpoint:**
```bash
python -m runner.run --task inputs/example_tasks/ai_gpu_optics.md --parallel-only
# Verify: 5 agent outputs + orchestrator_synthesis.md
# Verify: state_snapshots table has "post_parallel" entry
# Verify: Conflicts detected and logged (if any)
# Verify: Agent selection follows matrix for 'invest' objective
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

#### Phase 1F: Intake System
**Dependencies:** Phase 1C (LLM wrapper needed for Intake Agent)

The intake system supports two modes:
1. **Form-based intake** (legacy) - Fill out `intake_template.md` directly
2. **Conversational intake** (primary) - Chat with Claude via `/intake` skill

**Deliverables - Form-Based Intake:**
- [ ] `inputs/intake_template.md` - Intake form template
- [ ] `runner/intake.py` - Intake parser and quality scoring
- [ ] `skills/intake_quality.py` - Quality score calculation
- [ ] `charters/intake.md` - Legacy Intake Agent charter
- [ ] Quality score display and warnings
- [ ] `--check-intake-only` for validation without pipeline

**Deliverables - Conversational Intake (Primary):**
- [ ] `charters/intake_conversation.md` - Conversational intake charter ✓ (created)
- [ ] `schemas/intake_session.py` - Session, document, and task schemas ✓ (created)
- [ ] `runner/intake_conversation.py` - Conversation session manager
- [ ] `skills/document_processing.py` - PDF, URL, Excel, image extraction
- [ ] Session storage in `data/intakes/<intake_id>/`
- [ ] Multi-session support (pause/resume)
- [ ] Reference materials manifest generation
- [ ] Claude Code CLI integration via `/intake` skill
- [ ] Notebook: `05_phase1_intake_system.ipynb`

**Conversational Intake Flow:**
```
claude → /intake
   │
   ▼
Phase 1: Open Exploration (2-5 turns)
"What's on your mind? Tell me about what you're trying to figure out..."
   │
   ▼
Phase 2: Thesis Sharpening (2-4 turns)
"So the core bet is [X]. What's the biggest unknown?"
   │
   ▼
Phase 3: Constraints & Criteria (2-3 turns)
"What would make you walk away entirely?"
   │
   ▼
Phase 4: Document Processing (as needed)
User uploads PDFs, URLs, Excel files → processed and summarized
   │
   ▼
Phase 5: Synthesis & Confirmation
"Here's what I'm proposing to send to the analysis team... Does this capture it?"
   │
   ▼
OUTPUT: data/intakes/<intake_id>/
├── task.md              # Structured task file
├── transcript.jsonl     # Full conversation
├── session_meta.json    # Session state
├── intake_summary.md    # Key highlights
└── reference_materials/ # Processed documents
    ├── originals/
    ├── processed/
    └── manifest.json
```

**Validation Checkpoint:**
```bash
# Test form-based intake parsing
python -m runner.run --task inputs/example_intakes/minimal.md --check-intake-only
# Expected: Quality score and field warnings

# Test conversational intake via Claude Code
claude
> /intake
# Expected: Multi-turn conversation, document upload support

# Resume previous session
> /intake --resume intake_20260205_001

# Run pipeline from intake
python -m runner.run --intake intake_20260205_001
# Verify: task.md loaded, reference_materials available to agents
```

#### Phase 1G: Financial Data Layer (09_financial_data)
**Dependencies:** Phase 1E (Pipeline must be functional)

The 09_financial_data agent provides live market data to other agents via delegation. Inspired by the Dexter project's agentic tool routing pattern.

**Deliverables:**
- [ ] `charters/agents/09_financial_data.md` - Agent charter ✓ (created)
- [ ] `runner/financial_data.py` - Data retrieval implementation
- [ ] `skills/market_data.py` - API client abstraction
  - [ ] Financial Modeling Prep (FMP) integration
  - [ ] Polygon.io integration (fallback)
  - [ ] Rate limiting and caching
- [ ] Agentic tool routing (natural language → specific API calls)
- [ ] Response normalization with source attribution
- [ ] Integration with 06, 07, 08 agents (delegation pattern)
- [ ] DuckDB logging for data request audit trail
- [ ] Notebook: `06_phase1_financial_data.ipynb`

**Capabilities:**
| Capability | Data Points | API Source |
|------------|-------------|------------|
| Price Snapshot | Current price, volume, market cap | FMP/Polygon |
| Historical Prices | OHLCV daily/weekly/monthly | FMP/Polygon |
| Financial Statements | Income, balance sheet, cash flow (5yr) | FMP |
| Key Metrics | P/E, EV/EBITDA, ROE, margins | FMP |
| Analyst Estimates | EPS estimates, price targets | FMP |
| SEC Filings | 10-K, 10-Q, 8-K retrieval | SEC EDGAR |
| Insider Trading | Transactions, amounts, dates | FMP |

**Delegation Pattern:**
```
07_fundamental needs data
        │
        ▼
"Get NVDA income statement, ratios, analyst estimates (5 years)"
        │
        ▼
09_financial_data routes to appropriate APIs
        │
        ▼
Returns structured data with:
- data: The financial information
- source: "Financial Modeling Prep"
- as_of: "2026-02-05T15:30:00Z"
- confidence: "high"
```

**Validation Checkpoint:**
```bash
# Test data retrieval
python -c "from runner.financial_data import get_price_snapshot; print(get_price_snapshot('AAPL'))"
# Expected: Current price with source and timestamp

# Test agent delegation
python -m runner.run --task inputs/example_tasks/ai_gpu_optics.md --max-agents 1 --agent 07_fundamental
# Verify: 07_fundamental output includes data sourced from 09_financial_data
# Verify: Data requests logged in DuckDB
```

---

### Phase 2: Enhancement & Hardening

#### Phase 2A: Skills Layer & Plotting
**Dependencies:** Phase 1G

**Deliverables:**
- [ ] Structured extractors (assumptions, questions, conflicts)
- [ ] Automatic state enrichment after each agent
- [ ] Conflict detection and tracking
- [ ] `skills/plotting.py` - Publication-quality chart generation
  - [ ] Valuation comparison charts (horizontal bar)
  - [ ] Price charts with technical levels (candlestick)
  - [ ] Financial trend charts (multi-line)
  - [ ] Scenario waterfall charts
  - [ ] Risk matrix visualizations
  - [ ] Style guide implementation (colors, fonts, layout)
- [ ] Chart export (HTML + PNG) to run artifacts
- [ ] `schemas/agent_outputs.py` - Agent output schemas
  - [ ] Per-agent Pydantic models (SystemsOutput, InversionOutput, etc.)
  - [ ] Required sections validation
- [ ] `skills/output_validation.py` - Output validation
  - [ ] `validate_agent_output()` function
  - [ ] Missing section detection
  - [ ] Re-prompt logic for invalid outputs
- [ ] `skills/summarization.py` - Output summarization
  - [ ] `summarize_for_reporting()` function
  - [ ] Key findings extraction
  - [ ] Context limit management
- [ ] `skills/document_ingestion.py` - Reference material parsing
  - [ ] PDF text extraction
  - [ ] Markdown/text file parsing
  - [ ] Chunking for context limits
- [ ] `runner/checkpoint.py` - Checkpoint and resume
  - [ ] `save_checkpoint()` function
  - [ ] `resume_from_checkpoint()` function
  - [ ] `--resume` CLI flag
- [ ] Notebook: `06_phase2_skills_and_report.ipynb`

**Validation Checkpoint:**
```bash
# Test plotting skills
python -c "from skills.plotting import ReportPlotter; p = ReportPlotter(); print('Plotting ready')"
# Verify chart output exists after test run
ls data/runs/<test_run_id>/charts/
# Expected: valuation_comparison.html, valuation_comparison.png, etc.

# Test output validation
python -c "from skills.output_validation import validate_agent_output; print(validate_agent_output('01_systems', '# Test'))"

# Test checkpoint/resume
python -m runner.run --task inputs/example_tasks/ai_gpu_optics.md --max-agents 2
# Note the run_id, then:
python -m runner.run --resume <run_id>
# Verify: Pipeline resumes from last checkpoint
```

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

#### Phase 2C: Chain-of-Verification (CoVe) Module
**Dependencies:** Phase 2B

**Deliverables:**
- [ ] `runner/cove.py` - CoVe orchestration logic
- [ ] CoVe Generator agent (claim extraction)
- [ ] CoVe Skeptic agent (verification question generation)
- [ ] CoVe Verifier agent (independent verification)
- [ ] CoVe Editor agent (revision and finalization)
- [ ] CoVe trigger logic in Orchestrator
- [ ] CoVe database schema (cove_runs, cove_claims tables)
- [ ] Integration with web search and market data skills
- [ ] Notebook: `08_phase2_cove_module.ipynb`

**Validation Checkpoint:**
```bash
python -m runner.run --task inputs/example_tasks/rare_earth_diligence.md --enable-cove
# Verify: CoVe runs on 07_fundamental output
# Verify: Atomic claims extracted
# Verify: Verification questions generated
# Verify: Independent verification with sources
# Verify: Final output has caveats for unverified claims
# Verify: cove_runs and cove_claims tables populated
```

**CoVe Charter Files:**
```
charters/
└── cove/
    ├── generator.md      # Claim extraction prompt
    ├── skeptic.md        # VQ generation prompt
    ├── verifier.md       # Independent verification prompt
    └── editor.md         # Revision prompt
```

#### Phase 2D: Testing & Quality Gates
**Dependencies:** Phase 2C

**Deliverables:**
- [ ] `test_state_schema.py`
- [ ] `test_prompt_hashing.py`
- [ ] `test_duckdb_schema.py`
- [ ] `test_pipeline_smoke.py`
- [ ] `test_equity_workflow.py`
- [ ] `--dry-run` validation mode
- [ ] Notebook: `08_phase2_regression_tests.ipynb`

#### Phase 2E: Report Quality System
**Dependencies:** Phase 2A (plotting), Phase 2C (CoVe)

**Deliverables:**
- [ ] `skills/report_quality.py` - Automated quality checks
- [ ] Required section validation
- [ ] Bull/bear balance enforcement
- [ ] Numerical claim source verification
- [ ] Chart reference validation
- [ ] CoVe integration check
- [ ] Report template enforcement
- [ ] Quality gate CLI: `--check-quality` flag
- [ ] Notebook: `09_phase2_report_quality.ipynb`

**Validation Checkpoint:**
```bash
# Test report quality checks
python -m runner.run --task inputs/example_tasks/rare_earth_diligence.md --check-quality
# Expected output:
# Quality Check Results:
# ✓ required_sections: All sections present
# ✓ bull_bear_balance: Both bull and bear cases present
# ✓ recommendation_present: Clear recommendation found
# ✓ charts_exist: 3 charts generated
# ✓ cove_verification: No core claims contradicted
#
# RESULT: Report is SHIPPABLE (0 blockers, 0 warnings)
```

**Quality Report Schema:**
```python
# skills/report_quality.py
class QualityReport(BaseModel):
    run_id: str
    report_path: str
    total_checks: int
    passed_checks: int
    blockers: List[QualityCheckResult]
    warnings: List[QualityCheckResult]
    infos: List[QualityCheckResult]
    is_shippable: bool
    quality_score: float  # 0.0 - 1.0
    generated_at: datetime
```

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

-- Pipeline checkpoints for resume capability
CREATE TABLE IF NOT EXISTS checkpoints (
    checkpoint_id TEXT PRIMARY KEY,
    run_id TEXT NOT NULL,
    stage TEXT NOT NULL,  -- intake_complete, parallel_complete, etc.
    iteration INTEGER DEFAULT 0,
    state_snapshot TEXT,  -- JSON serialized PipelineState
    agent_outputs TEXT,   -- JSON map of agent -> output path
    pending_agents TEXT,  -- JSON list of agents not yet run
    recoverable BOOLEAN DEFAULT TRUE,
    error_context TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Agent output validation results
CREATE TABLE IF NOT EXISTS output_validations (
    validation_id TEXT PRIMARY KEY,
    run_id TEXT NOT NULL,
    agent_name TEXT NOT NULL,
    valid BOOLEAN,
    missing_sections TEXT,  -- JSON list
    warnings TEXT,          -- JSON list
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Conflict tracking
CREATE TABLE IF NOT EXISTS conflicts (
    conflict_id TEXT PRIMARY KEY,
    run_id TEXT NOT NULL,
    conflict_type TEXT,     -- factual, interpretive, valuation, timing, risk
    topic TEXT,
    agents_involved TEXT,   -- JSON list
    positions TEXT,         -- JSON map agent -> position
    severity TEXT,          -- critical, moderate, minor
    resolution TEXT,
    resolved BOOLEAN DEFAULT FALSE,
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
├── intake.md                  # Intake Agent (Phase 1F)
├── agents/
│   ├── 01_systems.md
│   ├── 02_inversion.md
│   ├── 03_allocator.md
│   ├── 04_incentives_timing.md
│   ├── 05_epistemic.md
│   ├── 06_screener.md         # Equity: ticker identification
│   ├── 07_fundamental.md      # Equity: valuation & financials
│   └── 08_technical.md        # Equity: chart & momentum analysis
│
└── cove/                      # Chain-of-Verification (Phase 2C)
    ├── generator.md           # Claim extraction
    ├── skeptic.md             # Verification question generation
    ├── verifier.md            # Independent verification
    └── editor.md              # Revision and finalization

runner/
├── __init__.py
├── run.py             # CLI entrypoint
├── pipeline.py        # Pipeline orchestration
├── orchestrator.py    # Orchestrator logic (Phase 1D)
├── state.py           # State schema (Pydantic)
├── artifacts.py       # Artifact management
├── db.py              # DuckDB operations
├── llm.py             # Provider abstraction
├── utils.py           # Utilities, hashing
├── intake.py          # Intake parser and agent (Phase 1F)
├── checkpoint.py      # Checkpoint and resume (Phase 2A)
└── cove.py            # CoVe module orchestration (Phase 2C)

schemas/
├── __init__.py
├── agent_input.py     # Universal agent input context
└── agent_outputs.py   # Per-agent output schemas

skills/
├── __init__.py
├── extractors.py        # Output parsing
├── scoring.py           # Confidence scoring
├── memo_builder.py      # Report assembly
├── conflicts.py         # Conflict detection and resolution
├── financials.py        # Financial data parsing
│
├── # Intake System (Phase 1F)
├── intake_quality.py    # Intake quality scoring
│
├── # Output Validation & Summarization (Phase 2A)
├── output_validation.py # Agent output schema validation
├── summarization.py     # Output summarization for Reporting
├── document_ingestion.py # Reference material parsing (PDF, text)
│
├── # Reporting & Visualization (Phase 2A/2E)
├── plotting.py          # Publication-quality chart generation
├── report_quality.py    # Automated quality checks
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
├── 05_phase1_intake_system.ipynb
├── 06_phase2_skills_and_report.ipynb
├── 07_phase2_regression_tests.ipynb
├── 08_phase2_equity_research.ipynb
├── 09_phase2_cove_module.ipynb
└── 10_phase2_report_quality.ipynb

data/
├── runs/.gitkeep
└── ledger.duckdb      # Created at runtime

inputs/
├── task_template.md           # Legacy task format (still supported)
├── intake_template.md         # Intake form template (Phase 1F)
├── example_tasks/
│   └── ai_gpu_optics.md
└── example_intakes/           # Example intake forms (Phase 1F)
    ├── minimal.md             # Minimal input for testing
    ├── partial.md             # Partial input for Intake Agent test
    └── complete.md            # Complete intake example
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
| 2.1 | 2026-02-05 | **09_financial_data Agent & Conversational Intake System** — Added 09_financial_data agent (Section 1.3): Dexter-inspired data layer with agentic tool routing, live market data retrieval, source attribution for CoVe integration. Added Conversational Intake System (Section 1.3, Phase 1F): Chat-based task definition via Claude Code CLI (`/intake`), multi-session support, document processing (PDF, URL, Excel, images), reference materials flow to all agents. Updated architecture diagram to show dual entry points and data layer delegation pattern. Added Phase 1G for financial data implementation. Created `charters/intake_conversation.md` and `schemas/intake_session.py`. System now has 9 agents (8 reasoning + 1 data layer) plus intake system. |
| 2.0 | 2026-02-03 | **Major Architecture Analysis & Gap Resolution** — Added Section 1.9: Orchestrator Charter with agent selection logic, synthesis protocol, iteration control, CoVe trigger rules, and stop conditions. Added Section 1.10: Agent Data Contracts with universal input schema and per-agent output schemas (SystemsOutput, InversionOutput, etc.) with required sections validation. Added Section 1.11: Agent Selection Matrix mapping objectives to required/conditional/skip agents. Added Section 1.12: Conflict Resolution Protocol with detection, classification, and resolution strategies. Added Section 1.13: Checkpoint & Resume Protocol for pipeline recovery. Added Section 1.14: Output Summarization Protocol for context management. Updated Phase 1D with Orchestrator implementation deliverables. Updated Phase 2A with output validation, summarization, document ingestion, and checkpoint skills. Added database tables: checkpoints, output_validations, conflicts. Added schemas/ directory for agent contracts. Updated Key Design Principles with chain of custody, fail-safe defaults, and resumability. |
| 1.9 | 2026-02-03 | **Intake System** (Section 1.7): Added comprehensive Intake Form template with 7 sections and 20+ guided fields. Intake Agent charter for interactive context gathering. Intake Quality Score system with objective-specific field weighting. Objective-specific question sets (invest/build/explore/decide/invent). Pipeline integration with CLI flags (--intake, --intake-agent, --check-intake-only). Flexible approach: all fields optional with quality warnings. Phase 1F for intake implementation. |
| 1.8 | 2026-02-03 | **Reporting Agent & Report Quality Standards** (Section 1.6): Added comprehensive Reporting Agent Charter with Amazon memo philosophy. Sell-side quality standards and enforcement. Full report template with required sections. Plotting skills specification (plotly/matplotlib, chart types, style guide). Report quality gate system with automated checks. Phase 2E for report quality implementation. Shippable report definition and criteria. |
| 1.7 | 2026-02-03 | Added Equity Agent Charter Prompts: Stock Screener criteria, Fundamental Analyst framework, Technical Chart breakdown, Risk Manager enhancement, News Impact Analyzer skill, Daily Market Routine for orchestrator. Professional prompt patterns for each agent role. |
| 1.6 | 2026-02-03 | Added Chain-of-Verification (CoVe) module (Section 1.5): Generator/Skeptic/Verifier/Editor agents for claim verification. CoVe trigger conditions, stop conditions, and integration with existing pipeline. Phase 2C for CoVe implementation. Database schema for verification tracking. Model config for CoVe agents. |
| 1.5 | 2026-02-03 | Added Serper.dev as secondary search provider (fast, cost-effective Google Search). Updated provider priority: Brave → Serper → SerpAPI. Added SerperClient implementation. |
| 1.4 | 2026-02-03 | Added Phase 3C Web Research Skills: Brave Search (primary), SerpAPI (fallback) integrations. Web/news search for all agents. Use cases per agent type. Updated file structure and environment variables. |
| 1.3 | 2026-02-03 | Enhanced Phase 3 Market Data: Added Polygon.io (primary), Schwab API (secondary), yfinance (fallback) integrations. Detailed provider config, data models, and client implementations. Added environment variables section. |
| 1.2 | 2026-02-03 | Added Equity Research Agents (06-08): Sector Screener, Fundamental Analyst, Technical Analyst. New equity research workflow with per-ticker deep-dive. Phase 2B for equity agents, Phase 3 for market data integration. Updated architecture diagram, model tiering, and file structure. |
| 1.1 | 2026-02-03 | Added LLM Provider & Model Strategy (Section 2.6): Claude-first approach, per-agent model tiering, extended thinking configuration, environment overrides, cost optimization path |
| 1.0 | 2026-02-03 | Initial final plan with improvements and recommendations |

---

*Document Version: 2.1*
*Updated: 2026-02-05*
*Status: Final Draft for Review*
