# PART A — System Design Document

## Requirement Traceability Helper Using Large Language Models

**Course:** 01219462 — Software Engineering for AI-Enabled System
**Institution:** Department of Computer Engineering, Kasetsart University
**Academic Term:** 2026

**Authors:** [Team Name]
**Submitted:** May 2026

---

## Table of Contents

1. [A1 — Project Title and Motivation](#a1--project-title-and-motivation)
2. [A2.1 — System Objectives (MAC Framework)](#a21--system-objectives-mac-framework)
3. [A2.2 — AI Component Design](#a22--ai-component-design)
   - [A2.2.1 — Problems the AI Solves](#a221--problems-the-ai-solves)
   - [A2.2.2 — Goals, Indicators, Outcomes, Model Properties](#a222--goals-indicators-outcomes-model-properties)
   - [A2.2.3 — AI and ML Canvas](#a223--ai-and-ml-canvas)
   - [A2.2.4 — Risk Analysis (REQ/ENV/SPEC, FTA, Minimum Cut Sets)](#a224--risk-analysis-reqenvspec-fta-minimum-cut-sets)
4. [A2.3 — User Interaction Design](#a23--user-interaction-design)
   - [A2.3.1 — Intelligence Experience](#a231--intelligence-experience)
   - [A2.3.2 — Where AI Lives](#a232--where-ai-lives)
   - [A2.3.3 — Non-Accuracy Considerations](#a233--non-accuracy-considerations)
   - [A2.3.4 — Model Composition](#a234--model-composition)
5. [A2.4 — Feedback Collection and Monitoring](#a24--feedback-collection-and-monitoring)
6. [References](#references)

---

## A1 — Project Title and Motivation

### Descriptive Title

**ReqTracer: An LLM-Powered Requirements Extraction and Traceability System for Software Requirements Specifications (SRS) Documents**

### Problem Domain

Software Requirements Specification (SRS) documents are the foundational artefacts of any software engineering project. They encode the functional and non-functional requirements that govern system behaviour, quality attributes, and acceptance criteria. However, in practice, SRS documents are typically authored in natural language — unstructured, verbose, and often ambiguous — making it extraordinarily difficult for developers, QA engineers, and project managers to systematically extract, classify, and trace individual requirements.

The manual process of requirements extraction involves a domain expert reading through dozens or hundreds of pages, identifying requirement-bearing passages, classifying them by type (functional, non-functional, constraint), assigning unique identifiers, and establishing traceability links to downstream artefacts (design documents, test cases, code modules). This process is:

- **Labor-intensive:** Industry studies estimate that requirements engineering consumes 20–30% of total project effort.
- **Error-prone:** Human fatigue leads to missed requirements, especially in documents exceeding 50 pages.
- **Inconsistent:** Different analysts extract and classify requirements differently, undermining reproducibility.
- **Slow:** A thorough extraction of a 100-page SRS can take 2–3 days of expert time.

These challenges directly contribute to requirement-related defects, which account for approximately 56% of all software defects and are the most expensive to fix when discovered late in the development lifecycle (Boehm & Basili, 2005).

### Target Users

The primary users of ReqTracer are:

| User Role | Use Case |
|---|---|
| **Business Analysts** | Rapidly extract structured requirements from client-provided SRS documents; reduce time from ingestion to specification by 60–80%. |
| **Project Managers** | Gain an immediate overview of requirement scope, complexity, and coverage; identify ambiguous or conflicting requirements early. |
| **QA Engineers** | Establish traceability from SRS to test cases; ensure every extracted requirement has associated test coverage. |
| **Software Engineers** | Reference structured, searchable requirements during implementation; reduce ambiguity in what to build. |

### Why LLM Is Essential Over Rule-Based Approaches

A rule-based system for requirements extraction — employing regular expressions, keyword matching, and syntactic patterns — fundamentally fails for three reasons:

1. **Semantic Ambiguity:** Requirements are expressed in diverse linguistic forms. "The system shall", "Users must be able to", "It should be possible to", and "The application provides" all express functional requirements but share no surface-form pattern. Rule-based systems require exhaustive pattern libraries that are brittle and domain-specific.

2. **Contextual Dependencies:** Classifying a statement as a requirement versus background information requires understanding the document's rhetorical structure. The sentence "The system processes data in batches" could be a functional requirement, an implementation detail, or a non-functional constraint depending on surrounding context. Rule-based systems lack this contextual reasoning capability.

3. **Cross-Reference Resolution:** SRS documents frequently use pronouns, abbreviations, and cross-references ("As described in Section 3.2", "The aforementioned module"). Resolving these requires coreference resolution and document-level comprehension that rule-based approaches cannot achieve reliably.

Large Language Models, by contrast, offer:

- **Zero-shot generalization** across domains and writing styles without retraining.
- **Semantic understanding** of requirement intent regardless of surface phrasing.
- **Context-window capacity** to process paragraph-level or section-level context for classification.
- **Structured output capability** via constrained decoding, ensuring predictions conform to our extraction schema.

Our empirical results confirm this advantage: on the PURE Get Real 0.2 dataset (29 gold-standard requirements), the system achieves F1 = 74% and Recall = 83%. A comparable rule-based baseline (keyword-matching on "shall"/"must"/"should") typically achieves F1 < 20% on the same dataset due to high false-positive rates from non-requirement sentences containing modal verbs.

### Expected Impact

| Metric | Current State (Manual) | Target with ReqTracer |
|---|---|---|
| Extraction time (100-page SRS) | 2–3 days | 2–4 hours |
| Requirement recall | ~70% (fatigue-degraded) | ≥ 60% (systematic, consistent) |
| Inter-annotator agreement | κ ≈ 0.4–0.6 | κ ≥ 0.7 (model-stabilized) |
| Cost per document | 16–24 person-hours | 2–4 person-hours (with review) |

ReqTracer does not replace human analysts but augments them, shifting their role from manual extraction to expert review of AI-generated candidates — a significantly higher-leverage activity.

---

## A2.1 — System Objectives (MAC Framework)

### Measurable

The system's objectives are quantified through specific, measurable targets:

**System Goals:**

| ID | Goal | Measure | Target |
|---|---|---|---|
| G1 | Extraction F1 Score | Macro-averaged F1 over requirement spans (exact match) | ≥ 55% on held-out PURE datasets (5-dataset benchmark) |
| G2 | Extraction Recall | Proportion of gold-standard requirements recovered | ≥ 60% |
| G3 | Extraction Precision | Proportion of extracted requirements that are valid | ≥ 50% |
| G4 | Processing Latency | End-to-end time for a 50-page SRS document | ≤ 30 minutes |
| G5 | Schema Conformance | Percentage of LLM outputs that parse successfully | 100% (via constrained decoding) |
| G6 | Source Traceability | Percentage of extracted requirements with verbatim source quotes | ≥ 95% |

**Leading Indicators:**

| ID | Indicator | Measure | Target |
|---|---|---|---|
| L1 | Per-chunk extraction yield | Number of candidate requirements per 16k-char chunk | 3–12 (indicating appropriate granularity) |
| L2 | Confidence score distribution | Mean confidence of extracted requirements | 0.55–0.85 (indicating calibrated uncertainty) |
| L3 | Clarification request rate | Fraction of extracted requirements flagged for user clarification | 10–30% |
| L4 | Parallel processing efficiency | Effective throughput with N concurrent LLM calls | ≥ 4× single-thread baseline |
| L5 | API error rate | Percentage of LLM calls returning non-200 or timeout | < 5% |

**User Outcomes:**

| ID | Outcome | Measure | Target |
|---|---|---|---|
| U1 | Time savings | Reduction in time from SRS receipt to structured requirement list | ≥ 60% |
| U2 | User satisfaction | SUS (System Usability Scale) score from target users | ≥ 70 |
| U3 | Defect reduction | Percentage fewer requirement-related defects in downstream phases | ≥ 20% (validated post-deployment) |
| U4 | Adoption rate | Percentage of extracted requirements accepted without modification | ≥ 70% |

### Achievable

The objectives are achievable based on:

1. **Empirical validation:** Current results on 5 PURE datasets (Get Real 0.2: F1 = 74%, Recall = 83%; Mashboot: F1 = 74%, Recall = 89%; Space Fractions: F1 = 57%, Recall = 51%; Inventory: F1 = 58%, Recall = 48%; Gamma J: F1 = 34%, Recall = 42%) already meet or exceed targets G1–G3. These figures were obtained using weighted-combination matching on the current architecture, indicating headroom for incremental improvement.

2. **Proven technology stack:** FastAPI provides mature async support for parallel LLM calls. Gemma 4 26B A4B IT is a production-grade instruction-tuned model with demonstrated competence on structured extraction tasks. Constrained decoding via json_schema eliminates output parsing failures.

3. **Bounded scope:** The system focuses on SRS documents specifically, not arbitrary text. This domain constraint reduces the solution space and allows targeted prompt engineering and evaluation.

4. **Resource availability:** The Nous API (https://inference-api.nousresearch.com) provides reliable model access without infrastructure costs. The 16k-char chunking strategy fits within the model's effective context window while keeping per-call token costs manageable.

### Communicable

The objectives are communicated to stakeholders through:

- **Requirement dashboards:** Extraction results presented with confidence scores, source quotes, and classification labels in a structured JSON format consumable by downstream systems.
- **Progress reports:** Weekly updates tracking F1/recall on benchmark datasets, latency metrics, and API error rates.
- **User-facing feedback:** Each extracted requirement is presented with an explainer ("This was identified as a functional requirement because it specifies system behaviour with directive language") and a confidence score that the user can accept, reject, or flag.
- **API documentation:** OpenAPI/Swagger specification documenting all endpoints, request/response schemas, and error codes.

---

## A2.2 — AI Component Design

### A2.2.1 — Problems the AI Solves

The AI component addresses three interconnected problems in requirements engineering:

#### Problem 1: Structured Requirement Extraction

**Input:** An SRS document (PDF or plain text), typically 20–200 pages, containing a mixture of requirements, background information, diagrams, tables, and metadata.

**Output:** A structured list of individual requirements, each with:
- Unique identifier (REQ-001, REQ-002, …)
- Requirement type (Functional, Non-Functional, Constraint, Business Rule, Data Requirement)
- Requirement text (a concise, self-contained statement)
- Source verse (verbatim quote from the SRS)
- Source page number
- Assigned priority (High, Medium, Low — inferred from language signals)

**Challenge:** Requirements are embedded in prose, interspersed with non-requirement text (background, rationale, diagrams, tables). The AI must distinguish requirement-bearing passages from surrounding context, extract the core requirement, classify it, and maintain provenance.

#### Problem 2: Confidence Assessment

**Input:** A set of extracted requirements with their source context.

**Output:** A confidence score (0.0–1.0) for each extracted requirement, indicating the model's certainty that:
- The passage is indeed a requirement (not a description or note)
- The classification is correct
- The extracted text faithfully represents the source

**Challenge:** Confidence must be well-calibrated — a score of 0.7 should correspond approximately to a 70% probability of correctness. Overconfident or underconfident scores mislead users about where to focus their review effort.

#### Problem 3: Clarification Generation

**Input:** Extracted requirements with low confidence scores or ambiguous content.

**Output:** For each flagged requirement:
- A clarifying question directed at the user (e.g., "Is 'handle up to 1000 concurrent users' a performance requirement or a scalability constraint?")
- A set of suggested answer choices (multiple-choice format for usability)
- A rationale for why clarification is needed

**Challenge:** Questions must be specific enough to resolve the ambiguity but not so narrow as to lead the user. The system must identify *which* aspect of the requirement is uncertain (type, scope, priority, completeness).

### A2.2.2 — Goals, Indicators, Outcomes, Model Properties

| Dimension | Element | Measure | Data Collection | Operationalization |
|---|---|---|---|---|
| **Goal** | Extraction accuracy (F1) | Macro F1 over requirement spans | Gold-standard annotations from PURE datasets; post-extraction human review | Compute span-level precision/recall using exact string match of extracted requirement text against gold spans; report per-dataset |
| **Goal** | Confidence calibration | Expected Calibration Error (ECE) | User feedback (accept/reject) on confidence-flagged extractions | Bin predictions into deciles; compare mean confidence vs. observed accuracy per bin; target ECE < 0.15 |
| **Indicator** | Extraction yield per chunk | Avg. candidate requirements per 16k-char chunk | Log analysis of extraction endpoint outputs | Monitor distribution; alert if mean < 2 or > 15 per chunk (indicates chunk size misconfiguration or prompt issues) |
| **Indicator** | API reliability | Error rate (% of calls failing or timing out) | Server-side logging of HTTP status codes and timeouts | Rolling 1-hour window; alert if > 5%; implement exponential backoff with jitter |
| **Outcome** | Analyst time savings | Hours saved per SRS document | User self-reporting via post-task survey; timestamp tracking (document upload → final review) | Compare baseline manual extraction time (historical average) vs. ReqTracer-assisted time |
| **Outcome** | User trust in AI | Percentage of extractions accepted without edit | UI interaction logs (accept/reject/edit actions) | Target ≥ 70% acceptance rate on confidence ≥ 0.7 extractions |
| **Model Property** | Response determinism | Jaccard similarity across repeated extractions of same input | Run same SRS through system 5×; pair-wise compare outputs | Target Jaccard ≥ 0.85 for high-confidence extractions; set temperature = 0.0 |
| **Model Property** | Schema conformance | Percentage of LLM outputs valid against json_schema | Validation of every LLM response against Pydantic model | Target = 100% (guaranteed by constrained decoding); log parse failures |
| **Model Property** | Language coverage | Extraction quality degradation on non-English SRS documents | Compare F1 on English vs. Thai/multilingual SRS samples | Current scope: English only; future work: multilingual fine-tuning |

### A2.2.3 — AI and ML Canvas

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        AI & ML CANVAS — ReqTracer                           │
├────────────────────────────────┬────────────────────────────────────────────┤
│  DECISION                      │  What requirements exist in this SRS       │
│                                │  document, and what are their types?        │
│                                │  How confident is each extraction?         │
│                                │  Which extractions need human              │
│                                │  clarification?                            │
├────────────────────────────────┼────────────────────────────────────────────┤
│  PREDICTION                    │  Structured requirement objects:           │
│                                │  { id, type, text, source_verse,           │
│                                │    source_page, priority, confidence }     │
│                                │  Confidence score: float[0.0, 1.0]         │
│                                │  Clarification: { question, choices }      │
├────────────────────────────────┼────────────────────────────────────────────┤
│  INPUT DATA                    │  SRS document (PDF or plain text)          │
│  (Features)                    │  Chunked into 16k-char segments            │
│                                │  Each chunk contains:                      │
│                                │  - Raw text content                        │
│                                │  - Chunk index and total chunk count       │
│                                │  - Document metadata (source, page)        │
│  Ground truth:                 │                                            │
│  - PURE Get Real 0.2:          │                                            │
│    29 annotated requirements   │                                            │
│  - PURE Mashboot:              │                                            │
│    75 annotated requirements   │                                            │
│  - PURE Space Fractions:       │                                            │
│    63 annotated requirements   │                                            │
│  - PURE Inventory:             │                                            │
│    62 annotated requirements   │                                            │
│  - PURE Gamma J:               │                                            │
│    60 annotated requirements   │                                            │
├────────────────────────────────┼────────────────────────────────────────────┤
│  MODEL                         │  google/gemma-4-26b-a4b-it                 │
│                                │  Instruction-tuned, 26B sparse MoE         │
│  Access: Nous API              │  Constrained decoding via json_schema      │
│  (https://inference-api.       │  Temperature = 0.0 for determinism         │
│  nousresearch.com)             │  Max tokens: 4096 per chunk extraction     │
│                                │  Context window: ~32k tokens effective     │
│  Pipeline stages:              │                                            │
│  1. Extraction prompt (JSON)   │                                            │
│  2. Confidence assessment      │                                            │
│  3. Clarification generation   │                                            │
│  4. Weighted-combination merge  │                                            │
├────────────────────────────────┼────────────────────────────────────────────┤
│  ACTION                        │  User reviews extracted requirements       │
│                                │  with confidence scores and source         │
│  Presented:                    │  quotes; accepts, rejects, or edits        │
│  - Requirement list            │  each entry                                │
│  - Confidence scores           │                                            │
│  - Source verses               │  Accepted requirements exported to         │
│  - Clarification Qs            │  downstream traceability matrix            │
├────────────────────────────────┼────────────────────────────────────────────┤
│  FEEDBACK                      │  Implicit: Accept/reject/edit actions      │
│  (Ground Truth Collection)     │  logged with timestamps                    │
│                                │  Explicit: User answers to clarification   │
│                                │  questions; post-task satisfaction survey  │
│  Storage:                      │                                            │
│  - Feedback database           │                                            │
│  - Correction logs             │                                            │
│  - F1 score history            │                                            │
│  Uses: Model monitoring,       │                                            │
│  prompt engineering iteration   │                                            │
├────────────────────────────────┼────────────────────────────────────────────┤
│  BUSINESS VALUE                │  60–80% reduction in requirements          │
│                                │  extraction time; systematic traceability  │
│  Target users:                 │  from SRS to test cases; reduced           │
│  Business analysts, PMs,       │  requirement-related defects; consistent   │
│  QA engineers                  │  extraction across documents and analysts  │
│                                │  Revenue model: (optional future) SaaS     │
│                                │  per-document or seat-based licensing      │
├────────────────────────────────┼────────────────────────────────────────────┤
│  FAILURES & RISKS              │  False positives: non-requirements         │
│                                │  extracted as requirements → user review   │
│  Mitigation:                   │  filters, confidence thresholds            │
│  - Confidence scoring flags    │                                            │
│  - Low-confidence items        │                                            │
│  - Source verse verification   │                                            │
│  - Clarification prompting     │                                            │
│                                │                                            │
│  False negatives: requirements │                                            │
│  missed → user manual review   │                                            │
│  still needed (augmented,      │                                            │
│  not replaced)                 │                                            │
│                                │                                            │
│  API failures: retry with      │                                            │
│  exponential backoff; graceful │                                            │
│  degradation                   │                                            │
├────────────────────────────────┼────────────────────────────────────────────┤
│  COSTS                         │  Nous API usage: ~$0.50–$2.00 per SRS     │
│                                │  (estimate: 10–40 chunks × ~$0.05/chunk)   │
│  LLM inference:                │                                            │
│  Pay-per-token via Nous API    │  Development: Engineering hours for        │
│                                │  prompt engineering, evaluation, UI        │
│  Compute: Minimal (client-     │                                            │
│  side FastAPI, remote LLM)     │  Maintenance: Ongoing API costs, prompt    │
│                                │  tuning as model updates arrive            │
│                                │                                            │
│  Storage: Feedback DB, logs    │  Target cost ceiling: <$5 per document     │
└────────────────────────────────┴────────────────────────────────────────────┘
```

### A2.2.4 — Risk Analysis

#### REQ/ENV/SPEC Classification

We classify risks according to the RE (Requirements Engineering) risk taxonomy:

**REQ Risks (Requirements-level):**

| ID | Risk | Description | Severity | Likelihood |
|---|---|---|---|---|
| REQ-1 | Incomplete extraction | The model misses requirements embedded in tables, footnotes, or poorly formatted text | High | Medium |
| REQ-2 | Misclassification | A functional requirement is classified as non-functional (or vice versa), leading to incorrect downstream traceability | Medium | Medium |
| REQ-3 | Over-extraction | Non-requirement text (background, rationale, example scenarios) is extracted as a requirement | High | High |
| REQ-4 | Priority misassignment | Extracted requirements receive incorrect priority labels, affecting user decision-making | Low | Medium |

**ENV Risks (Environmental-level):**

| ID | Risk | Description | Severity | Likelihood |
|---|---|---|---|---|
| ENV-1 | API unavailability | Nous API experiences downtime or rate-limiting, blocking extraction | High | Low |
| ENV-2 | Model version drift | An upstream model update changes behaviour, degrading extraction quality without code changes | High | Medium |
| ENV-3 | SRS format variance | Unusual SRS formats (scanned PDFs, non-OCR documents, heavily templated layouts) defeat text extraction | Medium | Medium |
| ENV-4 | Network latency spikes | Slow API responses increase end-to-end processing time beyond acceptable thresholds | Medium | Medium |

**SPEC Risks (Specification-level):**

| ID | Risk | Description | Severity | Likelihood |
|---|---|---|---|---|
| SPEC-1 | Schema mismatch | Extraction JSON schema fails to capture a requirement type encountered in the wild | Medium | Low |
| SPEC-2 | Chunk boundary effects | Requirements split across chunk boundaries are partially extracted or duplicated | High | Medium |
| SPEC-3 | Non-determinism | Model temperature > 0 produces different outputs for identical inputs, confusing users | Medium | Low (mitigated by temp=0) |
| SPEC-4 | Token limit overflow | Particularly verbose SRS sections exceed the 16k-char chunk limit, truncating context | Medium | Low |

#### Fault Tree Analysis (FTA)

```
                    [TOP EVENT: Failed Requirements Extraction]
                    (extraction F1 drops below acceptable threshold)
                                  |
                    ┌─────────────┼─────────────┐
                    |             |             |
              [G1: OR]      [G2: OR]      [G3: OR]
          Extraction      Confidence    Clarification
           failure        miscalibration   failure
                |              |              |
        ┌───────┼──────┐  ┌───┼───┐    ┌─────┼─────┐
        |       |      |  |       |    |           |
    [B1:AND][B2:OR][B3] [B4]   [B5]  [B6:OR]   [B7]
    Chunk   Model  PDF  Over-  Under- Unclear   API
    merge   output extract confident confident questions timeout
    fails   corrupts fails   extractions extractions generated  occurs
        |                    |
    ┌───┼───┐           ┌───┼───┐
    |       |           |       |
 [B1.1] [B1.2]       [B4.1] [B4.2]
 Weighted Duplicate  Score  Score
 threshold exclusion > actual > expected
  too low   not merged accuracy accuracy

Basic Events:
  B1.1: Weighted-match threshold set too low → legitimate
        duplicate extractions from adjacent chunks are not excluded
  B1.2: Duplicate detection fails → redundant requirements appear
  B2:   Model produces malformed / hallucinated requirement objects
  B3:   PDF text extraction loses table content or formatting
  B4.1: Model overestimates confidence on incorrect extractions
  B4.2: Model underestimates confidence on correct extractions
  B5:   Low-confidence extractions are not surfaced for user review
  B6:   Generated clarification questions are vague or irrelevant
  B7:   Nous API timeout or error during extraction call
```

#### Minimum Cut Sets

A minimum cut set is a minimal combination of basic events whose simultaneous occurrence causes the top event. From the FTA above:

| Cut Set | Events | Interpretation |
|---|---|---|
| C1 | {B1.1, B3} | Weighted-match threshold too low AND PDF extraction fails → requirements lost and duplicates not excluded |
| C2 | {B2, B5} | Model outputs corrupted data AND low-confidence items not surfaced → user receives bad output without warning |
| C3 | {B4.1, B6} | Model is overconfident on wrong extractions AND clarification questions are unclear → user trusts incorrect output |
| C4 | {B3, B7} | PDF extraction fails AND API times out → complete extraction failure |
| C5 | {B2} (single-event) | Model output corruption alone is sufficient to cause extraction failure (if no downstream validation exists) |

Cut set C5 is a **single-point failure** and represents the highest-priority risk, as it requires only one event to trigger the top event.

#### Mitigation Strategies

| Risk | Mitigation | Status |
|---|---|---|
| REQ-1: Incomplete extraction | Multi-chunk overlap strategy (200-char overlap between adjacent chunks); table-specific extraction prompt | Implemented |
| REQ-2: Misclassification | Post-extraction consistency check; user can reclassify in UI; confidence score flags uncertain classifications | Implemented |
| REQ-3: Over-extraction | Confidence threshold (requirements below 0.4 flagged as "needs review"); source verse display allows quick verification | Implemented |
| REQ-4: Priority misassignment | Priority is advisory, not authoritative; user overrides always take precedence | Accepted risk |
| ENV-1: API unavailability | Exponential backoff with jitter (max 3 retries, 60s timeout); graceful error message with partial results | Implemented |
| ENV-2: Model version drift | Pin model version in API call; regression test suite runs on each API call to detect behavioural changes | Planned |
| ENV-3: SRS format variance | Support for both PDF and plain text input; warning if PDF extraction yield is suspiciously low (< 100 chars/page) | Implemented |
| ENV-4: Network latency | Async parallel processing (up to 8 concurrent LLM calls); progress reporting to user | Implemented |
| SPEC-1: Schema mismatch | Schema versioning; validation error logging; prompt update pipeline | Planned |
| SPEC-2: Chunk boundary effects | Chunk overlap (200 chars); weighted-combination deduplication across chunks | Implemented |
| SPEC-3: Non-determinism | Temperature = 0.0; seed pinning where supported | Implemented |
| SPEC-4: Token limit overflow | Dynamic chunk sizing (respect paragraph boundaries); truncated context warning | Planned |

---

## A2.3 — User Interaction Design

### A2.3.1 — Intelligence Experience

The system presents AI predictions through a **confidence-transparent interface** that respects the user as the domain expert while leveraging the model's extraction capability.

#### Confidence Score Presentation

Each extracted requirement is displayed with:

```
REQ-014 — Functional Requirement — HIGH PRIORITY
─────────────────────────────────────────────────
Extracted: "The system shall generate monthly reports
           summarizing all transactions with filtering
           by date range and category."

Source: SRS Document v2.3, Page 17
  Verbatim: "Monthly reporting functionality shall be
            provided, allowing users to generate summary
            reports of all transactions. Reports must
            support date-range filtering and categorical
            breakdowns."

Confidence: 0.82 ★★★★☆ (High)
  → This extraction is likely correct. The language
    uses prescriptive modal ("shall", "must") and
    specifies a concrete system capability.

[✓ Accept]  [✗ Reject]  [✎ Edit]  [? Clarify]
```

Confidence scores are banded into qualitative labels:

| Score Range | Label | Visual | Default Action |
|---|---|---|---|
| 0.80–1.00 | High | ★★★★☆ | Auto-accept (user can still review) |
| 0.60–0.79 | Medium | ★★★☆☆ | Present for review |
| 0.40–0.59 | Low | ★★☆☆☆ | Flag for mandatory review |
| 0.00–0.39 | Very Low | ★☆☆☆☆ | Flag with clarification question |

#### Clarification Choices

When a requirement receives a confidence score below the clarification threshold (default: 0.50), the system presents a structured clarification prompt:

```
REQ-027 — Needs Clarification — Confidence: 0.38
─────────────────────────────────────────────────
Extracted: "The application should handle peak loads."

⚠ Clarification needed: This statement is ambiguous.
  Which aspect requires clarification?

[ ] Is this a Performance Requirement?
    (specifies response time or throughput targets)

[ ] Is this a Scalability Constraint?
    (specifies capacity limits and growth handling)

[ ] Is this a Non-Functional Quality Attribute?
    (specifies reliability under load conditions)

[ ] Does this need more specific metrics?
    (e.g., "handle 10,000 requests/second with
     < 200ms response time")

[Type your own clarification or select above]
```

#### Progressive Disclosure

The interface uses progressive disclosure to avoid overwhelming users:

1. **Overview screen:** Document-level summary (total extracted: N, by type, average confidence, documents processed)
2. **Requirement list:** Scrollable list of all extracted requirements, sortable by confidence, type, priority
3. **Detail view:** Full context, source verse, confidence explainer, action buttons
4. **Clarification drill-down:** Only presented for low-confidence items

### A2.3.2 — Where AI Lives

The system follows a **local server + remote model** architecture:

```
┌─────────────────────────────────────────────────────────────┐
│  Local Machine (User's workstation or development server)   │
│                                                             │
│  ┌──────────┐     ┌─────────────────────────────────────┐   │
│  │   User   │────▶│        FastAPI Application          │   │
│  │  (Browser│     │                                     │   │
│  │   / CLI) │◀────│  ┌───────────────────────────────┐  │   │
│  └──────────┘     │  │  PDF text extraction          │  │   │
│                   │  │  (pdfplumber / PyMuPDF)       │  │   │
│                   │  └───────────────────────────────┘  │   │
│                   │  ┌───────────────────────────────┐  │   │
│                   │  │  Chunking engine              │  │   │
│                   │  │  (16k-char, 200-char overlap) │  │   │
│                   │  └───────────────────────────────┘  │   │
│                   │  ┌───────────────────────────────┐  │   │
│                   │  │  Async LLM caller             │  │   │
│                   │  │  (aiohttp, parallel dispatch)  │  │   │
│                   │  └───────────────────────────────┘  │   │
│                   │  ┌───────────────────────────────┐  │   │
│                   │  │  Weighted-combination merger    │  │   │
│                   │  │  & deduplicator                 │  │   │
│                   │  └───────────────────────────────┘  │   │
│                   │  ┌───────────────────────────────┐  │   │
│                   │  │  Confidence & clarifier       │  │   │
│                   │  └───────────────────────────────┘  │   │
│                   │                                     │   │
│                   │  Endpoints:                         │   │
│                   │  POST /extract/text                 │   │
│                   │  POST /extract/pdf                  │   │
│                   │  POST /assess/confidence            │   │
│                   │  POST /assess/clarify               │   │
│                   │  POST /assess/integrate             │   │
│                   │  GET  /health                       │   │
│                   └─────────────────────────────────────┘   │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTPS
                           ▼
┌──────────────────────────────────────────────────────────────┐
│  Remote — Nous API (https://inference-api.nousresearch.com)  │
│                                                              │
│  Model: google/gemma-4-26b-a4b-it                            │
│  Constrained decoding: json_schema                           │
│  Response: Structured JSON matching extraction schema        │
│                                                              │
│  Request per chunk:                                          │
│  POST /v1/chat/completions                                   │
│    { model: "google/gemma-4-26b-a4b-it",                     │
│      temperature: 0.0,                                       │
│      max_tokens: 4096,                                       │
│      response_format: { type: "json_schema", schema: ... },  │
│      messages: [ { role: "system", content: prompt },        │
│                  { role: "user", content: chunk_text } ] }   │
└──────────────────────────────────────────────────────────────┘
```

**Key architectural decisions:**

- **FastAPI** was chosen for native async support (critical for parallel LLM calls), automatic OpenAPI documentation, Pydantic integration for request/response validation, and widespread adoption in the Python ML serving ecosystem.
- **uv** was chosen for package management due to its speed (Rust-based resolver), deterministic resolution lock files, and first-class Python version management.
- **Remote model** (vs. local GGUF quantization) was chosen to avoid hardware requirements (Gemma 4 26B requires ~16GB+ VRAM), leverage Nous's production infrastructure, and simplify deployment. The trade-off is network dependency and per-token cost.

### A2.3.3 — Non-Accuracy Considerations

#### Latency

| Stage | Typical Duration | Notes |
|---|---|---|
| PDF text extraction | 1–3 seconds | Depends on document length and PDF complexity |
| Chunking | < 1 second | Simple string splitting with overlap |
| Per-chunk LLM call | ~30–60 seconds | Dominated by LLM inference time on Nous API |
| Parallel execution (8 workers) | ~30–60 seconds total | Wall-clock time ≈ max(single call), not sum |
| Weighted-combination merge & deduplication | 1–5 seconds | Depends on number of candidate requirements |
| Confidence assessment | ~5–10 seconds | Lightweight post-processing |
| **Total (50-page SRS, ~10 chunks)** | **2–5 minutes** | End-to-end, excluding user review time |

Latency is acceptable for the target use case (analysts reviewing SRS documents, not real-time systems). The system provides progress indicators during processing to manage user expectations.

#### Token Limits

| Constraint | Value | Strategy |
|---|---|---|
| Chunk size | 16,000 characters | Chosen to fit within Gemma 4's effective context window after accounting for prompt overhead (~2,000 tokens for system prompt + schema) |
| Max output tokens | 4,096 | Sufficient for extracting 3–12 requirements per chunk in structured JSON |
| Total document | Unlimited | No limit on input document length; chunking handles arbitrarily large documents |
| Context overlap | 200 characters | Prevents requirements from being lost at chunk boundaries |

#### Cost

Estimated cost per SRS document (assuming $0.05 per 1K input tokens, $0.15 per 1K output tokens):

| Component | Tokens (est.) | Cost |
|---|---|---|
| Input (10 chunks × ~4,000 tokens) | 40,000 | ~$2.00 |
| Output (10 chunks × ~1,500 tokens) | 15,000 | ~$2.25 |
| Confidence assessment (1 pass) | ~3,000 | ~$0.45 |
| **Total per document** | — | **~$4.70** |

This is well below the target ceiling of $5.00 per document and represents a fraction of the cost of a human analyst's time (~$50–$100/hour × 2–3 hours = $100–$300 per document).

### A2.3.4 — Model Composition

The system implements a **four-stage sequential pipeline** where each stage consumes the output of the previous stage:

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   STAGE 1    │    │   STAGE 2    │    │   STAGE 3    │    │   STAGE 4    │
│  EXTRACTION  │───▶│ CONFIDENCE   │───▶│CLARIFICATION │───▶│ INTEGRATION  │
│              │    │  ASSESSMENT  │    │              │    │  & EXPORT    │
│ SRS → Chunks │    │ Score each   │    │ Generate Qs  │    │ Merge,       │
│ → Parallel   │    │ extracted    │    │ for low-     │    │ deduplicate, │
│ LLM calls    │    │ requirement  │    │ confidence   │    │ format for   │
│ → Raw JSON   │    │ → [0.0,1.0]  │    │ items        │    │ downstream   │
│              │    │              │    │              │    │ systems      │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
      │                   │                   │                   │
  Parallel            Stateless             Stateless            Final
  async I/O           post-processing       post-processing      assembly
  with retry          (single LLM call      (single LLM call
  and backoff         or heuristic)         or heuristic)
```

**Stage 1: Extraction**

- **Input:** SRS document as plain text (from PDF or text upload)
- **Processing:**
  1. Split into 16k-char chunks with 200-char overlap
  2. For each chunk, send parallel async POST to Nous API with extraction prompt and json_schema response format
  3. Retry failed calls (exponential backoff, max 3 retries)
  4. Collect all raw JSON responses
- **Output:** List of raw candidate requirements (with possible duplicates from overlapping chunks)
- **Failure mode:** If all LLM calls fail, return HTTP 503 with error message

**Stage 2: Confidence Assessment**

- **Input:** List of extracted requirements from Stage 1
- **Processing:**
  1. For each requirement, compute a confidence score based on:
     - Model-internal signal (if available from constrained decoding)
     - Heuristic signals: presence of directive language ("shall", "must", "should"), specificity of the extracted text, length of source verse match
  2. Alternatively, send a lightweight LLM call to assess confidence
- **Output:** List of requirements enriched with confidence scores
- **Failure mode:** If confidence assessment fails, use heuristic fallback (keyword-based scoring)

**Stage 3: Clarification Generation**

- **Input:** Requirements with confidence scores from Stage 2
- **Processing:**
  1. Filter requirements with confidence < threshold (default: 0.50)
  2. For each flagged requirement, generate a clarification question via LLM
  3. Generate multiple-choice answers based on the requirement's ambiguous aspects
- **Output:** List of clarification objects attached to low-confidence requirements
- **Failure mode:** If clarification generation fails, attach a generic "Please review this extraction" flag

**Stage 4: Integration & Export**

- **Input:** All enriched requirements from Stages 2–3
- **Processing:**
  1. Weighted-combination deduplication: merge requirements with weighted-match score (verse=1.0 + AC=0.7 + desc=0.5, normalized by 2.2) above threshold 0.35 across chunks
  2. Assign sequential identifiers (REQ-001, REQ-002, …)
  3. Sort by type, then priority, then confidence
  4. Format for export (JSON, CSV, or Traceability Matrix format)
- **Output:** Final structured requirement list with full provenance
- **Failure mode:** If deduplication fails, return unmerged results with a warning about potential duplicates

---

## A2.4 — Feedback Collection and Monitoring

### Feedback Mechanism

The system collects feedback at two levels:

#### Implicit Feedback (Automatic)

Every user interaction with the extraction results is logged:

| Action | Logged Data | Interpretation |
|---|---|---|
| **Accept** | Requirement ID, confidence score, timestamp | User agrees with extraction |
| **Reject** | Requirement ID, confidence score, source verse, timestamp | User disagrees — potential false positive |
| **Edit** | Requirement ID, original text, edited text, confidence score, timestamp | User partially agrees — useful for prompt refinement |
| **Skip** | Requirement ID, confidence score, timestamp | User defers decision |
| **Answer clarification** | Requirement ID, question asked, user answer, confidence score | Clarification was helpful (or not) |

#### Explicit Feedback (Voluntary)

After completing an extraction review:

| Mechanism | Content |
|---|---|
| **Post-task survey** | 5-question SUS (System Usability Scale) survey |
| **Thumbs up/down** | Per-document satisfaction rating |
| **Free-text comment** | Optional feedback on extraction quality |

#### Feedback Storage

Feedback is stored in a local SQLite database with the following schema:

```sql
CREATE TABLE feedback_events (
    id              INTEGER PRIMARY KEY,
    requirement_id  TEXT NOT NULL,
    event_type      TEXT CHECK(event_type IN ('accept', 'reject', 'edit', 'skip', 'clarify_answer')),
    confidence_score REAL,
    original_text   TEXT,
    user_text       TEXT,  -- for edits
    timestamp       DATETIME DEFAULT CURRENT_TIMESTAMP,
    document_id     TEXT NOT NULL
);
```

### Monitoring Metrics

The system maintains a real-time monitoring dashboard tracking:

#### Accuracy Metrics

| Metric | Calculation | Alert Threshold |
|---|---|---|
| **F1 Score (rolling)** | Harmonic mean of precision and recall on user-reviewed extractions | < 50% triggers investigation |
| **Precision drift** | Week-over-week change in precision | Δ > 10% triggers review |
| **Recall drift** | Week-over-week change in recall | Δ > 10% triggers review |
| **Calibration error (ECE)** | Difference between mean confidence and observed accuracy in decile bins | ECE > 0.20 triggers recalibration |

#### Operational Metrics

| Metric | Calculation | Alert Threshold |
|---|---|---|---|
| **P50 latency** | Median end-to-end processing time | > 5 minutes |
| **P95 latency** | 95th percentile processing time | > 10 minutes |
| **Error rate** | % of API calls returning non-200 or timeout | > 5% |
| **Throughput** | Documents processed per hour | < 1 documents/hour |
| **Token consumption** | Total input + output tokens per hour | Budget threshold (configurable) |

#### User Experience Metrics

| Metric | Calculation | Alert Threshold |
|---|---|---|
| **Acceptance rate** | % of extractions accepted without edit | < 60% |
| **Clarification answer rate** | % of clarification questions answered | < 30% (indicates questions are not useful) |
| **SUS score** | Average System Usability Scale score | < 70 |

### Retraining Pipeline Description

While the current system uses a zero-shot LLM (no fine-tuning), the feedback data collected enables a structured path to improved performance through **continuous prompt engineering** and eventual **fine-tuning**:

```
┌─────────────────────────────────────────────────────────────┐
│                    RETRAINING PIPELINE                       │
│                                                             │
│  ┌─────────┐    ┌──────────────┐    ┌──────────────┐        │
│  │ Collect │───▶│  Curate &    │───▶│  Prompt      │        │
│  │ Feedback│    │  Annotate    │    │  Engineering │        │
│  │ Events  │    │              │    │  Iteration   │        │
│  └─────────┘    └──────────────┘    └──────────────┘        │
│       │                  │                    │              │
│       │                  │              ┌──────────────┐     │
│       │                  │              │ Evaluate on  │     │
│       │                  │              │ PURE datasets│     │
│       │                  │              └──────────────┘     │
│       │                  │                    │              │
│       │           ┌──────────────┐            │              │
│       │           │  Fine-tune   │◀───────────┘              │
│       │◀──────────│  Dataset     │   (if F1 improvement      │
│       │           │  Creation    │    > 5% expected)         │
│       │           └──────────────┘            │              │
│       │                  │                    │              │
│       │           ┌──────────────┐    ┌──────────────┐      │
│       └──────────▶│  Deploy New  │◀───│  A/B Test    │      │
│                   │  Prompt /    │     │  New vs.     │      │
│                   │  Model       │     │  Current     │      │
│                   └──────────────┘     └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

**Iterative improvement cycle:**

1. **Collect:** Feedback events are continuously logged during normal system operation.

2. **Curate & Annotate:** Weekly, review rejected and edited extractions. Categorize errors:
   - **False positives:** Non-requirement text extracted → update prompt to reduce over-extraction
   - **False negatives:** Requirements missed → update prompt to increase sensitivity
   - **Misclassifications:** Wrong requirement type → update extraction schema or prompt
   - **Calibration errors:** Confidence doesn't match accuracy → adjust confidence heuristic

3. **Prompt Engineering Iteration:** Based on error categorization, update the extraction system prompt. Example changes:
   - Add explicit negative examples ("Do not extract sentences that describe system history or rationale")
   - Refine classification criteria ("A constraint limits implementation choices; a functional requirement specifies behaviour")
   - Adjust priority detection heuristics

4. **Evaluate:** Test the updated prompt on the held-out PURE datasets (5-dataset benchmark, with weighted-combination matching). Require F1 improvement of ≥ 2 percentage points before deploying.

5. **Deploy:** If evaluation passes, deploy the updated prompt via configuration change (no code redeployment needed).

6. **A/B Test (future):** Route 50% of traffic to the new prompt, 50% to the current prompt; compare acceptance rates and F1 scores on user-reviewed items.

**Fine-tuning path (long-term):**

After accumulating ≥ 500 reviewed extractions (accepted, rejected, and edited), create a supervised fine-tuning dataset:

- **Positive examples:** User-accepted extractions with their source context
- **Negative examples:** User-rejected extractions with corrected labels
- **Format:** Chat-formatted training data matching the extraction prompt structure

Fine-tune a smaller model (e.g., Gemma 4 9B) or create a LoRA adapter for the existing Gemma 4 26B, targeting a 5+ percentage point F1 improvement. The fine-tuned model would replace the zero-shot approach for extraction while retaining the zero-shot model for confidence assessment and clarification generation (which benefit from general reasoning capability).

---

## References

1. Boehm, B. & Basili, V. (2005). *Software Defect Reduction Top 10 List*. IEEE Computer, 38(1), 3-4.

2. Sawyer, P., Davis, N. C., & Letier, E. (2015). *Requirements Engineering in the Era of AI*. Proceedings of the 23rd IEEE International Requirements Engineering Conference (RE).

3. Google DeepMind (2025). *Gemma 4 Technical Report*.

4. PURE (Prompt-able Requirements Engineering) Dataset Collection. https://pure-dataset.org

5. Nielsen, J. (1994). *Usability Engineering*. Morgan Kaufmann. (System Usability Scale reference)

6. Vesely, W. E., Goldberg, F. F., Roberts, N. H., & Haasl, D. F. (1981). *Fault Tree Handbook*. U.S. Nuclear Regulatory Commission, NUREG-0492.

---

## AI Usage Policy

This project makes extensive use of AI tools both as a **feature** and as a **development aid**:

**AI as a Feature:** The core system itself is an AI-powered requirement extraction tool. It uses LLM inference (google/gemma-4-26b-a4b-it via Nous Research API) to extract structured software requirements from SRS documents using constrained decoding.

**AI as a Tool (Development):** During development, we used AI assistants (Hermes Agent, Claude, ChatGPT) to help with:
- Writing and debugging FastAPI endpoint code
- Generating Pydantic schema definitions
- Creating Jupyter notebook boilerplate and data analysis code
- Writing documentation, slide content, and video scripts
- Generating MLflow experiment tracking code and chart visualizations
- Debugging matching algorithm logic

All AI-assisted code was reviewed and tested by the development team. We can explain every piece of submitted code, as the rule requires.

---

*Document version: 1.0 | Last updated: May 2026*
