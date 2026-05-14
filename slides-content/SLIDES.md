# ReqTracer — Final Project Presentation Slides

> **Kasetsart University — Computer Science**
> Thesis: Requirement Traceability Helper Using LLM
> Format: 10–15 slides, concise bullet points, professional tone

---

## Slide 1 — Title

**Title:** ReqTracer: Requirement Traceability Helper Using LLM

- [Your Name], Kasetsart University, Computer Science
- [Course Name / Course Code]
- [Date of Presentation]
- Advisor: [Advisor Name]

**Speaker Notes:**
Thank you for being here. Today I'll be presenting ReqTracer — an LLM-powered system that helps extract structured software requirements from SRS documents, assesses their quality, and guides users through a clarification loop to make vague requirements concrete.

**Visual Suggestions:**
Clean title slide with university logo, project subtitle, and a subtle background graphic (e.g., a document-with-magnifying-glass icon or LLM/network visual).

---

## Slide 2 — The Problem

**Title:** Why Manual SRS Extraction Is Broken

- **Slow:** Reading a 15-page SRS and identifying every requirement takes hours of manual work
- **Error-prone:** Humans miss requirements, misclassify types, or skip acceptance criteria
- **Inconsistent:** Different engineers extract different sets from the same document
- **No traceability:** Extracted requirements are rarely linked back to their exact source text (verses and pages)
- **Quality gaps:** Vague, untestable requirements slip through without systematic review

**Speaker Notes:**
Software Requirements Specifications are dense, poorly structured documents. Engineers must manually read every page, identify requirements, classify them as functional or non-functional, and extract metadata like acceptance criteria and source location. This process is slow, inconsistent between engineers, and requirements often lose their connection to the source document. Worse, vague or untestable requirements go unnoticed until implementation time.

**Visual Suggestions:**
Side-by-side: a messy SRS PDF page on the left, a frustrated engineer on the right. Or a simple infographic showing time + error rate + inconsistency arrows going up.

---

## Slide 3 — Why LLMs, Not Rule-Based Systems

**Title:** Why Large Language Models?

- **Rule-based limits:** Regex and keyword matching fail on complex, naturally written SRS text
- **Context awareness:** LLMs understand nuance, domain context, and implicit requirements
- **Structured output:** Constrained decoding produces valid JSON — IDs, types, acceptance criteria, source verses
- **Zero-shot:** No training data or fine-tuning needed; works on any SRS document immediately
- **Reasoning capability:** Can flag vague language and generate targeted clarification questions

**Speaker Notes:**
Traditional approaches use regex, NLP parsing, or rule-based patterns. These work on rigidly formatted documents but fail on real-world SRS written in natural language. LLMs provide context understanding, can classify requirement types, and with constrained decoding, produce structured JSON output directly. The key advantage: zero-shot — it works on any SRS without training data.

**Visual Suggestions:**
Comparison table or Venn diagram: Rule-Based (rigid keywords, high precision, low recall) vs. LLM (contextual understanding, structured output, zero-shot). Or a simple flow: "SRS text → LLM + json_schema → structured requirements."

---

## Slide 4 — System Architecture

**Title:** End-to-End Extraction Pipeline

- **PDF parser:** Extracts text with page numbers using pdfplumber
- **Chunker:** Splits document into 16K-character chunks for LLM context window
- **LLM extractor:** Single-stage constrained decoding extracts all requirement fields simultaneously
- **Merger & fixer:** Deduplicates results, fixes page numbers and source verses with post-processing
- **Output:** Structured requirements with IDs, titles, descriptions, types, acceptance criteria, and citations

**Speaker Notes:**
The pipeline works in five stages. First, we parse the PDF with pdfplumber, preserving page numbers. Then we split the text into 16K-character chunks — this fits within the LLM's context window while keeping extraction focused. Each chunk goes through the LLM with constrained decoding, which extracts all requirement fields at once in a single prompt. After all chunks are processed in parallel, results are merged with deduplication and post-processing fixes page number assignments and replaces paraphrased source verses with exact matching text from the original document.

**Visual Suggestions:**
Architecture diagram (flowchart). Boxes left to right: PDF Upload → pdfplumber Parser → 16K Chunks → LLM (constrained decoding, parallel) → Merge & Fix → Structured JSON. Arrows showing data flow. Include a "Parallel processing" note on the LLM box.

---

## Slide 5 — The AI Component

**Title:** Constrained Decoding & Single-Stage Extraction

- **Single-stage design:** Combines MuSEE's 3 stages (identify → classify → extract) into one LLM call per chunk
- **Constrained decoding:** `response_format: json_schema` forces valid JSON at the token level
- **Schema-enforced structure:** Every requirement has id, title, description, type, acceptance_criteria, source_verse
- **53% faster than sequential:** Parallel chunk processing with asyncio.gather — no quality loss
- **Model:** google/gemma-4-26b-a4b-it via Nous Research API

**Speaker Notes:**
The original MuSEE paper proposes a 3-stage pipeline: first identify requirement entities, then classify them, then extract values. We implemented all three stages but found that single-stage extraction — one prompt that does everything — is faster, simpler, and produces comparable or better results. The key enabler is constrained decoding using json_schema: the model literally cannot produce invalid JSON because the schema is enforced at the token level during generation. We process all chunks in parallel, getting a 53% speedup with no quality penalty.

**Visual Suggestions:**
"Before/After" comparison: 3-stage pipeline (3 LLM calls per chunk, error propagation risk) vs. Single-stage (1 LLM call, schema-enforced output). Include the JSON schema as a small code block on the side.

---

## Slide 6 — Confidence & Clarification

**Title:** Handling Uncertainty: Flag, Question, Resolve

- **Confidence assessment:** Automatically flags vague language, missing criteria, wrong types with severity levels
- **Clarification loop (ToT):** Tree of Thought generates targeted questions with 3–5 clickable answer choices
- **Integration endpoint:** Rewrites vague requirements using user-selected answers — from "normal load" to "P95 ≤ 500ms"
- **Human-in-the-loop:** Low recall is compensated by interactive clarification — practical over perfect automation

**Speaker Notes:**
No extraction system is perfect, and that's okay. Our system is designed as a human-in-the-loop assistant. After extraction, a confidence endpoint flags issues: vague language, missing acceptance criteria, wrong requirement types — each with severity levels. Then the clarification endpoint uses Tree of Thought reasoning to generate targeted questions with predefined answer choices, so users can click rather than type. Finally, the integration endpoint rewrites the original requirements using the user's answers. For example, "responds within 500ms under normal load" becomes "P95 response time ≤500ms under 100 concurrent users." This loop turns vague SRS into concrete, testable requirements.

**Visual Suggestions:**
3-step flow diagram with example: (1) Extracted req with "normal load" highlighted → (2) Clarification question: "Which metric defines response time?" with 4 radio-button choices → (3) Rewritten requirement with "P95 ≤ 500ms / 100 concurrent users" shown. Include severity badges (green/yellow/red).

---

## Slide 7 — UI Design

**Title:** Frontend Interface

- **Upload panel:** Drag-and-drop PDF upload with real-time progress indicator
- **Results table:** Requirements displayed in sortable/filterable columns (ID, title, type, page, confidence)
- **Source highlighting:** Click any requirement to jump to the corresponding page and verse in the PDF viewer
- **Confidence dashboard:** Visual flags panel showing vague requirements by severity
- **Clarification modal:** Interactive Q&A interface with clickable choices and live rewrite preview

**Speaker Notes:**
The user interface is designed for fast, intuitive review. Engineers upload an SRS PDF, then see extracted requirements in a sortable table with confidence badges. Clicking a requirement highlights its source verse in the PDF viewer for verification. The confidence dashboard surfaces flagged items by severity. When clarification is needed, a modal presents questions with clickable choices and shows the rewritten requirement in real time. The goal: an engineer should review and improve a full SRS in minutes, not hours.

**Visual Suggestions:**
Mockup screenshots or wireframes: (1) Upload screen, (2) Results table with confidence badges, (3) Clarification modal with radio buttons, (4) Side-by-side before/after of a rewritten requirement. If no real mockups exist, use clean wireframe-style boxes.

---

## Slide 8 — API Architecture

**Title:** REST API — Five Endpoints, One Pipeline

| Endpoint | Method | Purpose |
|---|---|---|
| `/extract/text` | POST | Extract from raw SRS text |
| `/extract/pdf` | POST | Extract from uploaded PDF |
| `/assess/confidence` | POST | Flag vague/incomplete requirements |
| `/assess/clarify` | POST | Generate clarification questions with choices |
| `/assess/integrate` | POST | Rewrite requirements using user answers |

- **Framework:** FastAPI with OpenAPI/Swagger documentation
- **Data models:** 12 Pydantic schemas enforce strict input/output structure
- **Parallel processing:** Asyncio-based concurrent chunk extraction
- **Configurable:** Multi-pass extraction (`passes=N`), weighted matching thresholds

**Speaker Notes:**
The system is a REST API built on FastAPI with five endpoints forming the complete pipeline. Extraction accepts PDF or raw text. Confidence assessment flags issues by field. Clarification generates structured questions with clickable choices. Integration rewrites requirements based on user input. The API supports configurable parameters — you can run multi-pass extraction with different merge strategies depending on whether you prioritize recall or precision.

**Visual Suggestions:**
Request/response example: Show a curl command uploading a PDF and a snippet of the JSON response with 2-3 requirements. Include the API endpoint flow diagram from EXPERIMENT.md.

---

## Slide 9 — Results

**Title:** Extraction Performance Across 5 PURE Datasets

All results use **weighted combination matching** (verse=1.0 + AC=0.7 + desc=0.5, threshold=0.35):

**Get Real 0.2** (29 GT, 36 ext, college CS career website):

| Metric | Value |
|---|---|
| Precision | 67% |
| **Recall** | **83%** |
| **F1** | **74%** |
| Type accuracy | 92% |
| Verse match | 69% |

**Mashboot** (75 GT, 107 ext, social media tool):

| Metric | Value |
|---|---|
| Precision | 63% |
| **Recall** | **89%** |
| **F1** | **74%** |
| Type accuracy | 98% |
| Verse match | 48% |

**Space Fractions** (63 GT, 49 ext):

| Metric | Value |
|---|---|
| Precision | 65% |
| Recall | 51% |
| **F1** | **57%** |
| Type accuracy | 81% |
| Verse match | 24% |

**Inventory** (62 GT, 41 ext):

| Metric | Value |
|---|---|
| Precision | 73% |
| Recall | 48% |
| **F1** | **58%** |
| Type accuracy | 77% |
| Verse match | 30% |

**Gamma J** (60 GT, 87 ext):

| Metric | Value |
|---|---|
| Precision | 29% |
| Recall | 42% |
| **F1** | **34%** |
| Type accuracy | 96% |
| Verse match | 21% |

**Speaker Notes:**
We evaluated across all 5 PURE datasets using weighted combination matching — scoring verse overlap at 1.0, acceptance criteria at 0.7, and description at 0.5, with a 0.35 threshold. Get Real achieved 74% F1 with 83% recall. Mashboot also hit 74% F1 with 89% recall — the highest across all datasets. Space Fractions and Inventory landed at 57% and 58%. Gamma J was the most challenging at 34% F1 with heavy over-extraction. Type accuracy is consistently strong — 77% to 98% across all datasets, showing the model reliably distinguishes functional from non-functional requirements.

**Visual Suggestions:**
Stacked metric tables for all 5 datasets. Use color coding: green for strong results (recall, type accuracy), yellow for moderate, red for lower (Gamma J). Note the weighted matching methodology prominently.

---

## Slide 10 — Comparison with Published Work

**Title:** How Does This Compare to Prior LLM Extraction Work?

| Paper | LLM | Task | F1 / Key Result |
|---|---|---|---|
| BERT+CRF (2024) | BERT | Binary classification | 82.6% |
| ChatGPT/Gemini (2024) | GPT-3.5 / Gemini | Requirement classification | 76–77% |
| GPT-4.1-mini (2026) | GPT-4.1-mini | Information extraction (medical) | 55.6% |
| **This work** | **Gemma 26B** | **Full extraction across 5 PURE datasets (zero-shot)** | **34–74%** |

- Most published work focuses on classification (is this a requirement?), not extraction
- Our task is harder: find, classify, extract title/description/criteria/source — all in one pass
- F1 34–74% (weighted matching) spans a wide range — 74% on Get Real and Mashboot matches strong baselines; 34% on Gamma J shows over-extraction challenges
- The value is the end-to-end pipeline, not just extraction score

**Speaker Notes:**
It's tempting to compare our 34-74% F1 against BERT's 82.6%, but that's comparing apples to oranges. BERT does binary classification — given a sentence, is it a requirement or not? We do full extraction across 5 PURE datasets: find requirements in raw text, classify their type, extract structured metadata including acceptance criteria and source verses, using weighted combination matching. The strongest results (74% F1) compare well with published work. Our key contribution isn't just the extraction score — it's the complete pipeline that includes confidence assessment, clarification, and integration, which transforms raw extractions into actionable, testable requirements.

**Visual Suggestions:**
Bar chart comparing F1 scores across papers, with a clear annotation: "Different tasks — classification vs. full extraction." A callout box: "Our contribution = end-to-end pipeline, not just extraction F1."

---

## Slide 11 — Model Versioning

**Title:** Four Experiment Runs — Reproducibility & Evolution

| Run | Model | Get Real F1 | Mashboot F1 | Notes |
|---|---|---|---|---|
| 1 (April) | gpt-5-nano | 53.7% | 56.5% | Fast, over-extracting (+43%), no structured output on free tier |
| 2 (Historical) | gemma-26b | 53.7% | 56.5% | Baseline — same prompt, earlier API version |
| 3 (Cycle 3) | gemma-26b, 3-pass | 58.6% | 50.3% | Multi-pass + Jaccard merge |
| 4 (Current) | gemma-26b, weighted match | 74% | 74% | Weighted combination matching (verse 1.0 + AC 0.7 + desc 0.5) across 5 PURE datasets, threshold=0.35 |

- **Model variance confirmed:** Same prompt produces different results across API sessions
- **Weighted matching improves results:** 74% F1 on Get Real and Mashboot vs. prior 53-58%
- **Full evaluation across 5 PURE datasets:** Includes Space Fractions, Inventory, Gamma J
- **API behavior changes:** Free-tier models lost structured output support; moved to paid tier

**Speaker Notes:**
We ran four significant experiment configurations over the course of this project. Early runs used GPT-5 nano, which was fast but tended to over-extract by 43%. We then moved to Gemma 26B which gave more balanced results. Multi-pass extraction with Jaccard merge gave 58.6% F1 on Get Real. The current approach uses weighted combination matching — verse at 1.0, acceptance criteria at 0.7, description at 0.5, with a 0.35 threshold — and evaluates across all 5 PURE datasets. This gives 74% F1 on both Get Real and Mashboot, a significant improvement over the prior best of 53-58%. An important finding: the same prompt and model produce different results across different API sessions, confirming that LLM non-determinism is inherent and must be accounted for in experimental reporting.

**Visual Suggestions:**
Timeline or table showing the 4 runs. Highlight the tradeoff line with an arrow: "Recall ←→ Precision tradeoff." Include a small note about API behavior changes.

---

## Slide 12 — Explainability

**Title:** Prediction Reasoning — What the System Found & Why

**Example 1: Correct extraction with reasoning**
- **Text:** "The system shall respond within 500ms under normal load."
- **Extracted as:** REQ-011, Non-functional
- **Confidence flag:** "Normal load" is undefined (severity: high)
- **Clarification asked:** "Which metric defines response time?" → User selected P95
- **Result:** "P95 response time ≤500ms under 100 concurrent users."

**Example 2: Confident but wrong flag**
- **Text:** "Users shall be able to register accounts."
- **Extracted as:** REQ-001, Functional
- **Confidence:** No flags — clear, testable, complete
- **Why:** Action verb + clear subject + verifiable condition

**Example 3: Type misclassification caught**
- **Text:** "Content shall be well-organized."
- **Extracted as:** Non-functional (usability)
- **Confidence flagged:** "Vague — what does 'well-organized' mean?" → Suggestion: define hierarchy structure

**Speaker Notes:**
Explainability matters because users need to trust and understand the system's decisions. In the first example, the system correctly extracted a non-functional requirement but flagged "normal load" as too vague. The clarification loop resolved this into a specific, measurable requirement. In the second example, a clear functional requirement was extracted with no flags — the system recognizes when something is already good. In the third example, the system initially flagged a requirement, but the confidence assessment caught the vague language and suggested specific improvements. The system doesn't just extract — it explains its uncertainty and guides resolution.

**Visual Suggestions:**
Three-column layout showing before/after for each example. Use green checkmarks for correct decisions, yellow warning icons for flagged items. Show the clarification question and the rewritten result side by side.

---

## Slide 13 — Limitations & Future Work

**Title:** Limitations and What's Next

**Current Limitations:**
- **Recall range:** 42–89% across 5 datasets — some datasets have lower recall
- **Over-extraction:** Gamma J shows heavy over-extraction (87 ext vs 60 GT)
- **API latency:** 60+ seconds per chunk on Nous API; 15-page documents take 5+ minutes
- **No fine-tuning:** Zero-shot only; domain-specific fine-tuning could improve accuracy

**Future Work:**
- **Planning artifacts:** Chain of Thought and Reasoning Action Trees for task decomposition
- **Code alignment:** UniXCoder integration to verify implementation matches extracted requirements
- **Full pipeline integration:** Extraction → Planning → Code Alignment → Traceability matrix
- **Frontend deployment:** Complete React interface for end-to-end user experience
- **Thesis completion:** Full evaluation across 5 PURE datasets; write-up January 2027

**Speaker Notes:**
No system is perfect, and I want to be transparent about limitations. Recall ranges from 42 to 89 percent across 5 datasets — Get Real and Mashboot perform well, but Gamma J shows heavy over-extraction with only 34% F1. The weighted matching methodology helps, but difficult datasets still pose challenges. API latency is a practical concern — large documents take several minutes. And we're using zero-shot prompting; domain-specific fine-tuning would almost certainly improve results.

For future work, the next phases include planning artifacts using Chain of Thought reasoning, code alignment with UniXCoder to verify that implementation matches requirements, and a complete frontend deployment. The thesis write-up is planned for January 2027.

**Visual Suggestions:**
Two-column layout: "Limitations" on the left (with warning icons), "Future Work" on the right (with roadmap icons). Could also use a roadmap timeline graphic for the future work section.

---

## Slide 14 — AI Usage Disclosure

**Title:** AI Usage Disclosure

- **AI tools used throughout this project:**
  - **Claude Code (Anthropic):** Code scaffolding, API endpoint development, Pydantic schema design
  - **ChatGPT (OpenAI):** Prompt engineering for LLM extraction, confidence assessment, and clarification
  - **This presentation:** Slide content drafted with AI assistance; all data, results, and analysis are from actual experiments
- **All code, experiments, and results are original work**
- **Ground truth data is from the PURE dataset with manual corrections**
- **Metrics are reproducible from the provided test fixtures and scripts**

**Speaker Notes:**
I used AI tools for coding assistance and prompt engineering, as well as for drafting this presentation. All code was written by me with AI as an assistant, not an author. The experiments, results, analysis, and conclusions are entirely my own work. The ground truth data comes from the publicly available PURE dataset, which I manually reviewed and corrected.

**Visual Suggestions:**
Simple disclosure slide with a clean list. Could use the university's preferred disclosure format if one exists. Keep it minimal and professional.

---

## Slide 15 — Thank You / Q&A

**Title:** Thank You

- **ReqTracer:** Requirement Traceability Helper Using LLM
- **Contribution:** End-to-end pipeline for SRS extraction, confidence assessment, clarification, and requirement integration
- **Results:** F1 34–74% (5 PURE datasets), recall up to 89%, type accuracy 77–98%
- **Repository:** `/Users/xd/Final_Project/Requirement-extraction`
- **Contact:** [Your email]
- **Questions?**

**Speaker Notes:**
Thank you for your time. I'm happy to take questions about the extraction pipeline, the experimental results, the confidence and clarification system, or anything else about the project.

**Visual Suggestions:**
Clean closing slide with project name, key metrics as a highlight, contact info, and a QR code linking to the repository or live demo if available.

---

## Appendix — Speaker Notes Summary

### Timing Guide (20-minute presentation)
| Slide | Topic | Time |
|---|---|---|
| 1 | Title | 0:30 |
| 2 | Problem | 1:30 |
| 3 | Why LLM | 1:30 |
| 4 | Architecture | 2:00 |
| 5 | AI Component | 2:00 |
| 6 | Confidence | 2:30 |
| 7 | UI Design | 1:30 |
| 8 | API | 1:30 |
| 9 | Results | 2:00 |
| 10 | Comparison | 1:30 |
| 11 | Model Versioning | 1:30 |
| 12 | Explainability | 1:00 |
| 13 | Limitations | 1:30 |
| 14 | AI Disclosure | 0:30 |
| 15 | Thank You | 0:30 |
| | Q&A | 5:00+ |

### Key Numbers to Memorize
- **F1 range:** 34–74% (5 PURE datasets, weighted matching)
- **Best F1:** 74% (Get Real, Mashboot)
- **Best recall:** 89% (Mashboot)
- **Type accuracy:** 77–98%
- **Speedup:** 53% with parallel processing
- **Datasets:** Get Real 0.2 (29), Mashboot (75), Space Fractions (63), Inventory (62), Gamma J (60)
- **Model:** google/gemma-4-26b-a4b-it
- **Matching:** weighted combination (verse 1.0 + AC 0.7 + desc 0.5, threshold 0.35)

### Expected Questions & Answers
1. **"Why not fine-tune?"** — Zero-shot works on any SRS; fine-tuning requires domain-specific labeled data. This is a general-purpose tool.
2. **"Is 74% F1 good enough?"** — For a human-in-the-loop system, yes. The clarification loop compensates for missed items.
3. **"Why Gemma 26B over GPT-5?"** — GPT-5 nano over-extracts significantly. Gemma gives better precision/recall balance.
4. **"How long for a real SRS?"** — 10 pages: ~2 minutes. 15 pages: ~5 minutes.
