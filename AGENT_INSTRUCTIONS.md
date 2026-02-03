# Agent Instructions for This Repository
> This file serves as the project-specific CLAUDE.md equivalent. See also: AGENT_CONTEXT.md, AGENT_PROJECT_CONVENTION.md

## Mission and Starting Point
- Always read `AGENT_CONTEXT.md` before coding.

## How to Assist Effectively
- Understand which piece of the notebook you are porting before writing code. Keep `main.py` thin; delegate API, persistence, analytics, and plotting to their dedicated modules.
- When modifying code, state **what changed**, **why**, and **what follow-up work** remains. Reference notebook cells or data contracts when it helps reviewers.
- Prefer incremental lifts of notebook helpers. If you refactor aggressively, preserve CSV/plot outputs and add assertions so regressions surface quickly.

## Code Style, Layout, and Dependencies
- Target Python 3.11+. Use explicit imports and place modules inside `PATH` so imports stay consistent with the package layout.
- Keep `requirements.txt` aligned with actual imports (`requests`, `duckdb`, `matplotlib`, `pytz`, `yfinance`, `python-dotenv`, etc.).

## Database Rules


## Analytics, Plotting, and Alerts


## Testing, Validation, and Logging
- Keep console logging informative (`print` or `logging`) so Windows Task Scheduler logs are useful during failures.

## Documentation and Runbooks
- Keep `README.md` synchronized with the actual module layout, CLI usage (`python main.py`), configuration requirements, and deployment steps (Task Scheduler cadence, potential AWS migration).
- Document new env vars or config toggles in both `README.md`

## AGENT_CHANGELOG Expectations
- After each work session, append a dated section to `AGENT_CHANGELOG.md`. Use checkboxes for completed tasks and prefix in-progress bullets with `ƒ-`. Keep entries concise and archive/summarize older blocks instead of letting the file grow forever.

## Output Rules: Snippets vs. Full Files
- Default to returning only the modified snippet when the change is localized to a single block or function.
- Return the entire file only when edits touch multiple sections, adjust imports/class definitions, or when global context is critical for correctness. Keep full-file outputs to a few hundred lines.
- When uncertain, provide the snippet and ask if the user needs the full file.

## Environment and Safety
- Assume `python -m pip install -r requirements.txt` prepares the environment.
- Mention hidden assumptions, or scheduling edge cases in your responses so the next agent can continue seamlessly.

## PATH and directories
- Alway use relative path whenever possible
