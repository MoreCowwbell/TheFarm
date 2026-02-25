# Agent Changelog

This file tracks completed tasks and in-progress work across sessions.  
Each entry should be short, bullet-based, and written immediately after a task is completed.

Format:
- Use checkboxes for completed tasks.
- Use a "⧗" prefix for tasks that are in progress (not yet finished).
- Keep each bullet to one line.
- Keep total log size manageable (older items can be summarized or archived periodically).

---

## Example of logs:
## 2025-01-XX — Session Summary (Agent Name)
- [x] Short description of completed task.
- [x] Another completed task.
- ⧗ In-progress task that should be resumed next session.

## 2025-01-XX — Session Summary (Agent Name)
- [x] Completed adjustment to function X.
- ⧗ Started refactor of Y but not finished.

## 2025-01-14 — Session Summary (Claude Code)
- [x] Added timeout support to Polygon request helper.
- [x] Fixed missing import in historical.py.
- ⧗ Started rewriting intraday_stream.py state machine (continue next session).

---
## Start of Changelog below:

## 2026-02-25 — Financial Analysis Agent Frameworks (Claude Code)
- [x] Created `charters/agents/10_equity_intel.md` — Equity Intelligence Brief agent (Framework 1)
  - Rapid single-company institutional intelligence briefs
  - 5 sections: Business Foundation, Core Metrics, Performance Profile, Analyst Sentiment, Institutional Positioning
  - All data delegated to 09_financial_data; no independent retrieval
  - Model: Sonnet 4, Standard mode
- [x] Created `charters/agents/11_earnings_intel.md` — Earnings Intelligence Decoder agent (Framework 3)
  - Post-earnings analysis with transcript parsing and management commentary extraction
  - 6 sections: Reported Results, Forward Outlook, Segment Performance, Management Commentary, Market Reaction, Investment Verdict
  - Graceful degradation when transcripts unavailable (falls back to 8-K)
  - Critical guardrail: never fabricate management quotes
  - Model: Opus 4.5, Extended thinking
- [x] Enhanced `charters/agents/07_fundamental.md` — Added Forensic Audit Mode (Framework 2)
  - Income Statement Diagnostics (4-quarter table with margin trajectory)
  - Balance Sheet Deep-Dive (quick ratio, goodwill flag >30%, debt maturity timeline)
  - Cash Flow Validation (FCF margin, capital allocation breakdown)
  - 6 Risk Indicators scored PASS/WATCH/FAIL
  - 4 Strength Indicators scored STRONG/MODERATE/WEAK
  - Competitive Benchmarking table vs top 3 competitors
  - Forensic Verdict: plain-language operational assessment
- [x] Enhanced `charters/agents/06_screener.md` — Added Competitive Sector Matrix Mode (Framework 4)
  - Quantitative Comparison Table (18+ metrics across all companies)
  - Competitive Positioning (moat type, width, market share, share trend)
  - Risk Assessment Matrix (12-month risk, leverage risk, disruption risk)
  - Strategic Ranking (best valuation, growth, balance sheet, overall pick)
- [x] Expanded `charters/agents/09_financial_data.md` — ~15 new data capabilities
  - Tier 2: analyst ratings, price targets, institutional holdings QoQ, relative performance, quarterly financials (8Q), debt maturity, goodwill, AR/inventory detail, earnings estimates/surprises/release/revisions, sector KPIs
  - Tier 3: earnings call transcripts with speaker attribution
  - New API endpoints and agentic routing patterns for all new data types
  - Updated roadmap with Phase 2.5 for financial frameworks data layer
- [x] Updated `charters/orchestrator.md` — 4 new objective types
  - EQUITY_BRIEF, EARNINGS_ANALYSIS, SECTOR_COMPARISON, FORENSIC_AUDIT
  - Enhanced INVEST objective with conditional 10/11 inclusion
  - Updated delegation table and CoVe trigger rules
- [x] Updated `charters/reporting.md` — 4 alternative report templates
  - EQUITY_BRIEF: data-dense single-page brief
  - EARNINGS_ANALYSIS: verdict-first with results table
  - SECTOR_COMPARISON: strategic ranking with comparison tables
  - FORENSIC_AUDIT: risk/strength scorecard with quarterly diagnostics
  - Template-specific quality checklists
- [x] Updated `charters/cove/generator.md` — Financial framework claim extraction patterns
  - Framework-specific extraction rules for 10, 11, 07(forensic), 06(matrix)
  - New claim type: MANAGEMENT_QUOTE (highest verification priority)
- [x] Updated `charters/cove/verifier.md` — Management quote verification protocol
  - SUPPORTED/PARTIALLY_SUPPORTED/CONTRADICTED/UNVERIFIED verdicts for quotes
  - Transcript-based verification with speaker attribution check
  - Contradicted management quotes flagged as critical contradictions
- [x] Updated `charters/intake_conversation.md` — New objective types and field priorities
  - Added 4 new objective types to task file format
  - Field priority table for EQUITY_BRIEF, EARNINGS_ANALYSIS, SECTOR_COMPARISON, FORENSIC_AUDIT
  - Objective detection signals for quick routing
- [x] Updated `AGENT_CONTEXT.md` — Architecture updates for 11-agent system
  - Added Financial Intelligence Agents (10-11) category
  - Updated execution flow diagram with new agents
  - Added Objective Types reference table
  - Updated Known Gaps section
- [x] Updated `AGENT_INSTRUCTIONS.md` — Model config for agents 10-11

## 2026-02-05 — Session Summary (Claude Code) - Part 3
- [x] Updated `Plan_FINAL.md` to version 2.1:
  - Updated Section 1.3 Core Agents: Added 09_financial_data and Intake System categories (now 9 agents)
  - Updated Section 1.2 Architecture diagram: Added dual entry points (direct vs conversational) and data layer
  - Updated Phase 1F: Added conversational intake deliverables alongside form-based approach
  - Added Phase 1G: Financial Data Layer implementation phase
  - Added changelog entry for version 2.1

## 2026-02-05 — Session Summary (Claude Code) - Part 2
- [x] Created Conversational Intake System:
  - `charters/intake_conversation.md` - Full charter for conversational intake via Claude Code CLI
  - Multi-session support (explore → refine → document → confirm → complete)
  - Document processing capabilities (PDF, URL, Excel, images, folders)
  - Reference materials flow to all downstream agents
- [x] Created `schemas/intake_session.py` - Pydantic models for:
  - Session state management (SessionState, SessionMetadata, IntakeSession)
  - Document processing (ProcessedDocument, DocumentManifest)
  - Conversation tracking (ConversationTurn, ConversationHighlight)
  - Task output generation (TaskOutput with to_markdown())
- [x] Updated `AGENT_CONTEXT.md`:
  - Added Intake Conversation Agent to agent table
  - Updated directory layout with intakes/ folder structure
  - Updated execution flow diagram showing dual entry points
  - Added intake CLI options
- [x] Updated `AGENT_INSTRUCTIONS.md`:
  - Added Intake Conversation to model config (Opus 4.5, Extended)
- [x] Updated `orchestrator.md`:
  - Added Reference Materials Integration section
  - Document routing by agent type table
  - Manifest parsing and tracking responsibilities

## 2026-02-05 — Session Summary (Claude Code) - Part 1
- [x] Created `09_financial_data.md` charter - new data layer subagent inspired by Dexter project
  - Agentic tool routing pattern for natural language → API calls
  - Financial statements, price data, ratios, analyst estimates, SEC filings
  - Source attribution and freshness metadata for CoVe integration
  - Planned API integration with FMP or Polygon.io
- [x] Updated `orchestrator.md` with 09_financial_data integration:
  - Added Data Layer Architecture section explaining delegation pattern
  - Updated agent selection matrix to show 09 as data layer for equity objectives
  - Updated CoVe trigger rules table
- [x] Updated equity research agent charters to delegate to 09_financial_data:
  - `06_screener.md` - delegates for market caps, sectors, peer lists
  - `07_fundamental.md` - delegates for statements, ratios, estimates
  - `08_technical.md` - delegates for price history and volume data
- [x] Updated `04_incentives.md` to delegate for insider trading data
- [x] Updated `cove/verifier.md` to use 09_financial_data for verification data retrieval
- [x] Updated `AGENT_CONTEXT.md`:
  - Changed from 8 to 9 agents, added Data Layer category
  - Updated execution flow diagram showing delegation pattern
  - Updated Known Gaps section re: API implementation pending
- [x] Updated `AGENT_INSTRUCTIONS.md`:
  - Added 09_financial_data to model configuration table (Sonnet 4)
  - Added FMP_API_KEY to optional environment variables

## 2026-02-02 — Session Summary (Claude Code)
- [x] Updated `AGENT_CONTEXT.md` with comprehensive project documentation:
  - Project goal summary (deepmind1 multi-agent diligence system)
  - Full 8-agent architecture with capabilities table
  - Directory layout matching Plan_FINAL.md specification
  - Execution flow diagram (parallel → synthesis → sequential → reporting)
  - Data storage details (DuckDB tables, DATA_ROOT convention)
  - External integrations (LLM providers, market data, web search)
  - Deployment/CLI commands and environment variables
  - Known gaps and tips for contributors
- [x] Updated `AGENT_INSTRUCTIONS.md` with project-specific guidance:
  - Database rules (DuckDB audit ledger, SHA256 hashing)
  - Analytics/plotting requirements (Plotly, chart quality checklist)
  - Model configuration table (Opus vs Sonnet per agent)
  - Testing/validation workflow (notebooks, checkpoints)
  - CLI quick reference
- [x] Added this session entry to `AGENT_CHANGELOG.md`
