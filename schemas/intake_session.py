"""
Intake Session Schemas

Pydantic models for the Conversational Intake System.
These schemas define the structure of intake sessions, documents, and outputs.
"""

from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


# -----------------------------------------------------------------------------
# Enums
# -----------------------------------------------------------------------------

class SessionState(str, Enum):
    """States an intake session can be in."""
    EXPLORING = "exploring"      # Initial conversation, gathering context
    REFINING = "refining"        # Narrowing to specific questions and constraints
    DOCUMENTING = "documenting"  # Processing user-provided materials
    CONFIRMING = "confirming"    # Reviewing draft task file with user
    COMPLETE = "complete"        # Task file generated, ready for pipeline
    PAUSED = "paused"            # User left mid-session, can resume


class ObjectiveType(str, Enum):
    """Task objective types."""
    INVEST = "invest"
    BUILD = "build"
    EXPLORE = "explore"
    DECIDE = "decide"
    INVENT = "invent"


class TimeHorizon(str, Enum):
    """Investment/analysis time horizons."""
    TACTICAL = "tactical"        # < 3 months
    NEAR_TERM = "near-term"      # 3-12 months
    MEDIUM_TERM = "medium-term"  # 1-3 years
    STRATEGIC = "strategic"      # 3+ years


class RiskAppetite(str, Enum):
    """Risk tolerance levels."""
    CONSERVATIVE = "conservative"
    MODERATE = "moderate"
    AGGRESSIVE = "aggressive"


class DocumentFormat(str, Enum):
    """Supported document formats."""
    PDF = "pdf"
    URL = "url"
    EXCEL = "excel"
    CSV = "csv"
    IMAGE = "image"
    WORD = "word"
    MARKDOWN = "markdown"
    TEXT = "text"
    FOLDER = "folder"
    UNKNOWN = "unknown"


# -----------------------------------------------------------------------------
# Document Models
# -----------------------------------------------------------------------------

class DocumentExtract(BaseModel):
    """A specific extract from a document."""
    location: str = Field(..., description="Page number, URL anchor, or section name")
    text: str = Field(..., description="The extracted text")
    relevance: Optional[str] = Field(None, description="Why this extract matters")


class ProcessedDocument(BaseModel):
    """A document that has been processed for the intake session."""
    id: str = Field(..., description="Unique document identifier (doc_001, etc.)")
    original_name: str = Field(..., description="Original filename or URL")
    original_path: str = Field(..., description="Path to original file in session folder")
    processed_path: Optional[str] = Field(None, description="Path to processed/extracted version")
    format: DocumentFormat = Field(..., description="Detected document format")
    size_bytes: Optional[int] = Field(None, description="File size in bytes")
    pages: Optional[int] = Field(None, description="Number of pages (for PDFs)")
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
    fetched_at: Optional[datetime] = Field(None, description="When URL was fetched")

    # Content analysis
    summary: str = Field(..., description="3-5 sentence summary of document")
    key_extracts: List[DocumentExtract] = Field(default_factory=list)
    relevance_to_thesis: Optional[str] = Field(None, description="How this relates to user's thesis")

    # Processing metadata
    processing_success: bool = Field(True, description="Whether processing completed successfully")
    processing_notes: Optional[str] = Field(None, description="Any issues during processing")


class DocumentManifest(BaseModel):
    """Manifest of all documents in an intake session."""
    intake_id: str
    documents: List[ProcessedDocument] = Field(default_factory=list)
    total_documents: int = Field(0)
    last_updated: datetime = Field(default_factory=datetime.utcnow)

    def add_document(self, doc: ProcessedDocument) -> None:
        """Add a document to the manifest."""
        self.documents.append(doc)
        self.total_documents = len(self.documents)
        self.last_updated = datetime.utcnow()


# -----------------------------------------------------------------------------
# Conversation Models
# -----------------------------------------------------------------------------

class ConversationTurn(BaseModel):
    """A single turn in the intake conversation."""
    turn_id: int = Field(..., description="Sequential turn number")
    role: str = Field(..., description="'user' or 'assistant'")
    content: str = Field(..., description="The message content")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    phase: SessionState = Field(..., description="Which phase this turn was in")

    # Optional metadata
    documents_referenced: List[str] = Field(default_factory=list, description="Document IDs mentioned")
    key_insight: Optional[str] = Field(None, description="If this turn surfaced important info")


class ConversationHighlight(BaseModel):
    """A key moment from the conversation worth preserving."""
    turn_id: int
    highlight_type: str = Field(..., description="thesis, kill_criterion, insight, concern, etc.")
    content: str
    extracted_at: datetime = Field(default_factory=datetime.utcnow)


# -----------------------------------------------------------------------------
# Session Models
# -----------------------------------------------------------------------------

class SessionMetadata(BaseModel):
    """Metadata about an intake session."""
    intake_id: str = Field(..., description="Unique session identifier")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    state: SessionState = Field(SessionState.EXPLORING)

    # Progress tracking
    total_turns: int = Field(0)
    documents_processed: int = Field(0)

    # User info (optional)
    user_id: Optional[str] = Field(None)
    session_title: Optional[str] = Field(None, description="User-provided title or auto-generated")

    # Completion info
    task_file_generated: bool = Field(False)
    task_file_path: Optional[str] = Field(None)
    pipeline_run_id: Optional[str] = Field(None, description="If pipeline was run from this intake")


class IntakeSession(BaseModel):
    """Complete intake session state."""
    metadata: SessionMetadata
    conversation: List[ConversationTurn] = Field(default_factory=list)
    highlights: List[ConversationHighlight] = Field(default_factory=list)
    documents: DocumentManifest

    # Extracted information (populated during conversation)
    working_title: Optional[str] = Field(None)
    working_thesis: Optional[str] = Field(None)
    objective: Optional[ObjectiveType] = Field(None)
    time_horizon: Optional[TimeHorizon] = Field(None)
    risk_appetite: Optional[RiskAppetite] = Field(None)
    kill_criteria: List[str] = Field(default_factory=list)
    constraints: List[str] = Field(default_factory=list)
    key_questions: List[str] = Field(default_factory=list)

    def add_turn(self, role: str, content: str, phase: SessionState) -> ConversationTurn:
        """Add a conversation turn."""
        turn = ConversationTurn(
            turn_id=len(self.conversation) + 1,
            role=role,
            content=content,
            phase=phase
        )
        self.conversation.append(turn)
        self.metadata.total_turns = len(self.conversation)
        self.metadata.updated_at = datetime.utcnow()
        return turn

    def add_highlight(self, turn_id: int, highlight_type: str, content: str) -> None:
        """Add a conversation highlight."""
        highlight = ConversationHighlight(
            turn_id=turn_id,
            highlight_type=highlight_type,
            content=content
        )
        self.highlights.append(highlight)

    def transition_to(self, new_state: SessionState) -> None:
        """Transition session to a new state."""
        self.metadata.state = new_state
        self.metadata.updated_at = datetime.utcnow()


# -----------------------------------------------------------------------------
# Task Output Models
# -----------------------------------------------------------------------------

class TaskOutput(BaseModel):
    """The final task file generated from an intake session."""
    # Metadata
    intake_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    session_turns: int
    documents_processed: int

    # Core task definition
    title: str
    objective: ObjectiveType
    one_line_ask: str

    # Context
    background: str = Field(..., description="2-3 paragraphs of context")
    core_thesis: str
    key_questions: List[str]

    # Constraints and criteria
    kill_criteria: List[str]
    constraints: List[str]
    time_horizon: TimeHorizon
    risk_appetite: RiskAppetite
    decision_stakes: str

    # Prior beliefs
    prior_hypotheses: List[str] = Field(default_factory=list)

    # Reference materials
    reference_materials: List[Dict[str, str]] = Field(
        default_factory=list,
        description="List of {name, summary} for each document"
    )

    # Conversation context
    conversation_highlights: List[str] = Field(
        default_factory=list,
        description="Key moments from the intake conversation"
    )

    def to_markdown(self) -> str:
        """Generate the task.md file content."""
        materials_section = "\n".join([
            f"- **{m['name']}**: {m['summary']}"
            for m in self.reference_materials
        ]) if self.reference_materials else "None provided."

        highlights_section = "\n".join([
            f"- {h}" for h in self.conversation_highlights
        ]) if self.conversation_highlights else "See full transcript."

        kill_criteria_section = "\n".join([
            f"- {k}" for k in self.kill_criteria
        ]) if self.kill_criteria else "None specified."

        constraints_section = "\n".join([
            f"- {c}" for c in self.constraints
        ]) if self.constraints else "None specified."

        questions_section = "\n".join([
            f"{i+1}. {q}" for i, q in enumerate(self.key_questions)
        ])

        hypotheses_section = "\n".join([
            f"- {h}" for h in self.prior_hypotheses
        ]) if self.prior_hypotheses else "None stated."

        return f"""# Task: {self.title}

## Metadata
- **Intake ID:** {self.intake_id}
- **Created:** {self.created_at.isoformat()}
- **Session Turns:** {self.session_turns}
- **Documents Processed:** {self.documents_processed}

## Objective
{self.objective.value}

## One-Line Ask
{self.one_line_ask}

## Background & Context
{self.background}

## Core Thesis
{self.core_thesis}

## Key Questions to Answer
{questions_section}

## Kill Criteria
{kill_criteria_section}

## Constraints
{constraints_section}

## Time Horizon
{self.time_horizon.value}

## Risk Appetite
{self.risk_appetite.value}

## Decision Stakes
{self.decision_stakes}

## Prior Hypotheses
{hypotheses_section}

## Reference Materials
{materials_section}

See: reference_materials/manifest.json for full details.

## Conversation Highlights
{highlights_section}

---
Generated by Intake Conversation Agent
Full transcript: data/intakes/{self.intake_id}/transcript.jsonl
"""


# -----------------------------------------------------------------------------
# Helper Functions
# -----------------------------------------------------------------------------

def generate_intake_id() -> str:
    """Generate a unique intake session ID."""
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    import secrets
    suffix = secrets.token_hex(3)
    return f"intake_{timestamp}_{suffix}"


def detect_document_format(filename: str) -> DocumentFormat:
    """Detect document format from filename."""
    filename_lower = filename.lower()

    if filename_lower.startswith(("http://", "https://")):
        return DocumentFormat.URL

    extension_map = {
        ".pdf": DocumentFormat.PDF,
        ".xlsx": DocumentFormat.EXCEL,
        ".xls": DocumentFormat.EXCEL,
        ".csv": DocumentFormat.CSV,
        ".png": DocumentFormat.IMAGE,
        ".jpg": DocumentFormat.IMAGE,
        ".jpeg": DocumentFormat.IMAGE,
        ".gif": DocumentFormat.IMAGE,
        ".webp": DocumentFormat.IMAGE,
        ".doc": DocumentFormat.WORD,
        ".docx": DocumentFormat.WORD,
        ".md": DocumentFormat.MARKDOWN,
        ".txt": DocumentFormat.TEXT,
    }

    for ext, fmt in extension_map.items():
        if filename_lower.endswith(ext):
            return fmt

    return DocumentFormat.UNKNOWN


def get_intake_session_path(intake_id: str, data_root: Path = Path("data")) -> Path:
    """Get the path to an intake session folder."""
    return data_root / "intakes" / intake_id
