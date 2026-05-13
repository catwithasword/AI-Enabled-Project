# Part C1: UI Design — ReqTracer Intelligence Interface

**Document:** C1_UI_Design.md  
**Project:** ReqTracer — Requirements Intelligence System  
**Deliverable:** Part C1 — UI Design & Intelligence Experience  

---

## 1. Overview

The ReqTracer UI provides a guided, intelligent experience for extracting, validating, and resolving ambiguities from Software Requirements Specification (SRS) documents. The interface uses a sidebar navigation layout with five primary screens:

| Screen | File | Purpose |
|--------|------|---------|
| Dashboard | `mockup_dashboard.html` | Upload SRS PDF, monitor extraction progress |
| Extraction Results | `mockup_results.html` | Browse extracted requirements with field-level details |
| Confidence Assessment | `mockup_confidence.html` | Review AI confidence scores and severity flags |
| Clarification Q&A | `mockup_clarification.html` | Answer AI questions to resolve ambiguities |

---

## 2. Intelligence Experience

The core design differentiator is how ReqTracer surfaces AI confidence and uncertainty to the user — not as a black box, but as a transparent, actionable dialogue.

### 2.1 Confidence Bands

Each extracted requirement is assigned confidence scores at two levels:

1. **Overall requirement confidence** — a single score summarizing AI certainty.
2. **Field-level confidence** — individual scores for each extracted attribute (Title, Description, Type, Acceptance Criteria, Source Verse).

Confidence is communicated through three bands:

| Band | Range | Visual | Meaning |
|------|-------|--------|---------|
| **HIGH** | > 90% | 🟢 Green badge | AI is very confident. Requirement is clear, complete, and testable. Minimal review needed. |
| **MEDIUM** | 70–90% | 🟡 Amber badge | Some uncertainty detected. Ambiguous language, vague thresholds, or incomplete acceptance criteria. Human review recommended. |
| **LOW** | < 70% | 🔴 Red badge | Significant uncertainty. Critical information missing or highly ambiguous. Requires clarification before the requirement can be trusted. |

### 2.2 How Confidence Scores Are Shown

- **Color-coded badges** appear next to each requirement in the Extraction Results table and within the Confidence Assessment view.
- **Field-level bars** in the Confidence view show per-attribute scores (e.g., Title: 92% HIGH, Description: 45% LOW).
- **Distribution histogram** on the Confidence page provides an at-a-glance overview of the project's overall extraction quality.
- **Severity classification** (HIGH/MEDIUM/LOW flags) combines field-level scores to prioritize which requirements need attention first. HIGH-severity items should be addressed before MEDIUM, which should be addressed before LOW.

### 2.3 How Users Provide Feedback

Users interact with the extraction in three ways:

#### Thumbs Up / Thumbs Down
- Every requirement in the Extraction Results table has 👍 and 👎 buttons.
- **Thumbs up** confirms the extraction is accurate — reinforces the model's approach for similar future extractions.
- **Thumbs down** flags the extraction as incorrect — prompts the system to reconsider and invites the user to provide corrections.

#### "Fix Suggestion" Button
- Appears on flagged (MEDIUM/LOW confidence) requirements.
- When clicked, generates an AI-proposed correction. For example:
  - *Original:* "All data must use latest industry-standard encryption."
  - *Suggested fix:* "All data in transit must use TLS 1.3; all data at rest must use AES-256 encryption (per NIST SP 800-52r2)."
- The user reviews the suggestion and clicks **Apply** to accept it, or dismisses it to proceed to manual clarification.

#### Clarification Q&A
- Low-confidence items are funneled into the Clarification flow, where the AI generates targeted questions.
- Questions appear as multiple-choice options with rationales, or as open-text inputs.
- A **Tree-of-Thought** panel shows the AI's reasoning: it evaluates multiple interpretations of the ambiguous text, weighs pros/cons, and recommends the strongest resolution.
- User answers feed back into the extraction, updating confidence scores and regenerating the affected requirements.

---

## 3. Screen Designs

### 3.1 Dashboard (`mockup_dashboard.html`)

**Purpose:** Entry point for SRS document upload and extraction monitoring.

**Key Elements:**
- **Upload zone** with drag-and-drop area and file browser button
- **File info card** showing document name, size, page count, and processing status
- **Progress tracker** with 5 steps:
  1. Parse PDF document
  2. Classify requirement types
  3. Extract functional requirements
  4. Extract non-functional requirements
  5. Generate traceability matrix
- **Live stats** showing requirement counts by type and flagged items

**Design Rationale:** The progress tracker uses animated dots (green = done, purple pulsing = active, grey = pending) so users understand exactly where the extraction pipeline is. The stats preview gives immediate value even before extraction completes.

---

### 3.2 Extraction Results (`mockup_results.html`)

**Purpose:** Full table of extracted requirements with filtering, search, and per-row feedback.

**Key Elements:**
- **Summary bar** showing totals: Total, Functional, Non-Functional, Flagged, Average Confidence
- **Filter chips** to toggle between requirement types and view only flagged items
- **Search box** for quick requirement lookup
- **Requirements table** with columns:
  - ID (FR-001, NFR-003, etc.)
  - Title + Description
  - Type badge (Functional / Non-Func. / Constraint / Interface)
  - Acceptance Criteria (Gherkin-style)
  - Source verse (SRS section reference)
  - Confidence score with color-coded dot
  - Action buttons (thumbs up/down, Fix Suggestion)
- **Pagination** for large SRS documents

**Design Rationale:** Row-level feedback lets users validate extractions quickly. The "Fix Suggestion" button appears inline on flagged rows, enabling one-click improvement without navigating away.

---

### 3.3 Confidence Assessment (`mockup_confidence.html`)

**Purpose:** Deep dive into AI confidence for each field of flagged requirements.

**Key Elements:**
- **Confidence legend** showing the three bands with a distribution histogram
- **Flag cards** ordered by severity (HIGH first, then MEDIUM, then LOW)
- Each flag card contains:
  - Severity badge (red HIGH, orange MEDIUM, yellow LOW)
  - Requirement ID, title, and overall confidence percentage
  - **Field-level confidence bars** for each attribute (Title, Description, Type, Acceptance Criteria, Source Verse)
  - **Flag notes** explaining why a field scored low (e.g., "latest industry-standard is ambiguous")
  - **AI Improvement Suggestion** box with a specific, actionable correction and an "Apply Suggestion" button

**Design Rationale:** By showing field-level granularity, users understand exactly *which part* of a requirement is uncertain. The AI suggestions provide concrete fixes rather than just flagging problems.

---

### 3.4 Clarification Q&A (`mockup_clarification.html`)

**Purpose:** Interactive dialogue to resolve ambiguities and improve extraction quality.

**Key Elements:**
- **Progress stepper** showing which flagged requirements still need clarification
- **Multiple-choice questions** for each ambiguity, with:
  - Context (requirement ID, confidence, severity)
  - The specific question being asked
  - Options A, B, C ... each with a rationale explaining pros/cons
  - Option for custom free-text input
- **Tree-of-Thought analysis** panel showing:
  - Branch A, B, C reasoning with pros and cons
  - AI's recommendation with justification
  - Reference to relevant standards (e.g., IEEE 29148, SRE practices)
- **Right sidebar** with question progress and projected confidence improvement
- **Navigation** between questions (Previous / Next / Skip)

**Design Rationale:** Presenting AI reasoning transparently builds trust. Multiple-choice with rationales educates the user while gathering their domain knowledge. The projected impact metric ("answer these 5 questions to raise confidence from 84% to 96%") motivates completion.

---

## 4. Interaction Flow

```
Upload SRS PDF
    │
    ▼
Extraction Runs (dashboard progress)
    │
    ▼
View Extraction Results ──── thumbs up/down per requirement
    │                              │
    ▼                              ▼
Flagged items shown       AI learns from feedback
    │
    ▼
Confidence Assessment ─── Fix Suggestion button → auto-apply correction
    │
    ▼
Clarification Q&A ────── User answers questions → AI updates requirements
    │
    ▼
Review updated results with improved confidence
```

---

## 5. Design Decisions

| Decision | Rationale |
|----------|-----------|
| Sidebar navigation | Standard pattern for multi-step workflows; keeps context visible |
| Color-coded confidence | Green/amber/red is universally understood; maps to traffic-light mental model |
| Field-level granularity | Users can trust what's confident and focus efforts on what's uncertain |
| Multiple-choice over free-text | Faster for users; guides toward actionable resolutions; easier to process |
| Tree-of-Thought transparency | Builds trust by showing AI reasoning; helps non-technical stakeholders understand |
| Inline Fix Suggestion | Low-friction improvement; no context switching required |
| Projected impact metric | Motivates users to complete clarification flow |

---

## 6. Files Delivered

| File | Description |
|------|-------------|
| `C1_UI_Design.md` | This document — UI design specification and Intelligence Experience description |
| `mockup_dashboard.html` | Dashboard screen: upload, progress tracking, preview stats |
| `mockup_results.html` | Extraction results table with filtering, feedback, and fix suggestions |
| `mockup_confidence.html` | Confidence assessment with field-level scores and AI suggestions |
| `mockup_clarification.html` | Clarification Q&A with multiple-choice, Tree-of-Thought, and progress tracking |
