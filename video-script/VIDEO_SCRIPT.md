# ReqTracer Video Presentation Script

**Title:** Requirement Traceability Helper Using LLM  
**Target Duration:** 5-8 minutes  
**Format:** Screen recording with voice-over narration  
**Tip:** Read at a natural pace. Pause on transitions between sections. Each timestamp is approximate.

---

## Section 1 — Title & Introduction [0:00 – 0:30]

**On Screen:** Title slide — project name, your name, institution. Clean background with the ReqTracer logo or title text centered.

**Script:**

> "Hi, I'm [Your Name], and this is ReqTracer — a Requirement Traceability Helper powered by large language models.
>
> In software engineering, the Software Requirements Specification — or SRS — is the foundation of every project. It defines what needs to be built, the constraints, and the acceptance criteria. But extracting actionable requirements from a lengthy SRS document is a manual, tedious, and error-prone process.
>
> ReqTracer automates this extraction, producing structured, traceable requirement records from raw SRS documents — and it flags areas that need human attention."

---

## Section 2 — Problem Statement [0:30 – 1:15]

**On Screen:** Transition to a slide or screen showing a dense page of a real SRS document (PDF) with text highlighted everywhere. Then overlay bullets:
- Manual extraction is time-consuming
- Prone to human error and inconsistency
- Cross-references between requirements are easily missed

**Script:**

> "Let's talk about the problem. A typical SRS document can be dozens — sometimes hundreds — of pages long. Engineers have to read through it line by line, identify individual requirements, classify them by type — like functional, non-functional, performance — assign unique IDs, and link them to stakeholders, goals, and acceptance criteria.
>
> This is incredibly time-consuming. And because it's manual, it's also error-prone — requirements get missed, misclassified, or duplicated. Worse, cross-references between requirements are easily overlooked, which breaks traceability downstream when you're doing impact analysis or testing.
>
> Existing tools often rely on simple keyword matching or rules-based extraction, which struggles with the natural ambiguity of technical writing."

---

## Section 3 — Why LLMs? [1:15 – 2:00]

**On Screen:** Side-by-side comparison:
- Left: "Traditional Rule-Based" — show pseudo-regex or keyword matching with a red X
- Right: "LLM-Based Extraction" — show a clean structured requirement card with a green checkmark
- Bullet points: Semantic understanding, Context awareness, Cross-reference reasoning

**Script:**

> "So why use a large language model instead of traditional rule-based approaches?
>
> Rule-based systems — things like regex patterns or keyword lookups — fail when requirements are expressed in natural language. They can't handle semantic ambiguity. For example, the word 'shall' is the standard requirement indicator — but not every 'shall' sentence is a requirement, and some valid requirements don't use 'shall' at all.
>
> LLMs understand context. They can distinguish a requirement from a design constraint, a rationale, or a descriptive note. They can resolve cross-references like 'as described in Section 3.2' and link requirements together meaningfully.
>
> This semantic understanding is what makes LLM-based extraction fundamentally more capable — but it also introduces new challenges around consistency and hallucination, which we address in ReqTracer."

---

## Section 4 — System Architecture [2:00 – 3:00]

**On Screen:** Architecture diagram flowing left to right:

```
  PDF Document
       │
       ▼
  ┌───────────────┐
  │  PDF Parser   │  → Text extraction, page splits
  └───────┬───────┘
          ▼
  ┌───────────────┐
  │ Text Chunking  │  → Section-aware splits, ~3K tokens each
  └───────┬───────┘
          ▼
  ┌─────────────────────────────────────┐
  │ LLM: Gemma-4-26b (Nous API)         │
  │  + Constrained Decoding (JSON)      │
  │  + Chain of Thought reasoning       │
  └───────────────┬─────────────────────┘
                  ▼
  ┌───────────────┐
  │ Merge &       │  → Deduplication, ID assignment,
  │ Post-process   │     confidence scoring
  └───────┬───────┘
          ▼
  ┌───────────────┐
  │ Results        │  → Requirements CSV/JSON,
  │                │     flagged items, clarification Qs
  └───────────────┘
```

**Script:**

> "Here's how ReqTracer works under the hood.
>
> First, the system takes an SRS document in PDF format and extracts the text, preserving page structure.
>
> The text is then chunked into manageable pieces — roughly 3,000 tokens each — keeping section boundaries intact so context isn't lost mid-requirement.
>
> Each chunk is sent to the LLM — we use Gemma-4-26B through the Nous API. The model is prompted to identify requirements, classify their types, and extract key metadata.
>
> A key part of our pipeline is constrained decoding — the LLM outputs are forced into a strict JSON schema. This prevents hallucinated fields and guarantees a consistent, parseable output format.
>
> Finally, results from all chunks are merged: duplicates are resolved, unique requirement IDs are assigned, confidence scores are calculated, and any ambiguous requirements are flagged for review."

---

## Section 5 — Demo Walkthrough [3:00 – 5:00]

**On Screen:** Screen recording of the actual application. Switch between views as described.

### 5a — Uploading the Document [3:00 – 3:20]

**On Screen:** Show the upload page. Click through file selection, then show the processing indicator.

**Script:**

> "Let me walk you through the actual tool. Starting on the upload page — you simply select your SRS PDF and click 'Extract Requirements.'
>
> The system processes the document in parallel — each chunk is sent to the LLM concurrently to minimize wait time. You'll see a progress indicator."

### 5b — Extraction Results [3:20 – 3:50]

**On Screen:** Switch to the results table. Scroll through a few requirement cards showing ID, type, priority, description, acceptance criteria, source page.

**Script:**

> "Once processing is complete, you see the extraction results. Each requirement has a unique ID, its type — functional, performance, constraint, and so on — priority classification, the requirement text itself, acceptance criteria, and the source page from the original document.
>
> You'll notice the requirement descriptions preserve the original language while being normalized into a consistent format."

### 5c — Confidence Assessment [3:50 – 4:20]

**On Screen:** Zoom in on a requirement card with a red or orange confidence flag. Show the confidence breakdown: confidence score, flagged status, reason for flag, source overlap info.

**Script:**

> "Here's a key feature — confidence assessment. Not every extraction is equally reliable. Requirements with low confidence are flagged in orange or red.
>
> Each flagged item includes an explanation — for example, the LLM may have been uncertain about the requirement type, or the source text was ambiguous. You also get source overlap information, which is especially useful when processing revised documents — it shows you what changed."

### 5d — Clarification Questions [4:20 – 4:40]

**On Screen:** Show the Tree-of-Thought clarification panel. Display a sample question like "The requirement states 'system shall be fast' — what is the acceptable response time threshold?" with answer fields.

**Script:**

> "For ambiguous requirements, the system generates clarification questions using a Tree-of-Thought approach. The LLM identifies what information is missing and formulates specific questions — for example, 'This requirement says the system shall be fast — what is the acceptable response time?'
>
> Engineers can answer these questions, and their input gets fed back into the pipeline."

### 5e — Updated Requirements After Integration [4:40 – 5:00]

**On Screen:** Show the updated requirement card after answers were integrated — compare before and after side by side if possible.

**Script:**

> "Once the clarification answers are integrated, the requirements are updated to include the new information — making them specific, testable, and complete. This creates a feedback loop where the tool guides engineers toward higher-quality requirements."

---

## Section 6 — Results & Evaluation [5:00 – 6:00]

**On Screen:** Results table or bar chart comparing metrics across datasets:

| Dataset | F1 | Recall | Type Accuracy | Verse Match |
|---------|-----|--------|---------------|-------------|
| Get Real 0.2 | 74% | 83% | 92% | 69% |
| Mashboot | 74% | 89% | 98% | 48% |
| Space Fractions | 57% | 51% | 81% | 24% |
| Inventory | 58% | 48% | 77% | 30% |
| Gamma J | 34% | 42% | 96% | 21% |

Results use weighted combination matching (verse=1.0 + AC=0.7 + desc=0.5, threshold=0.35).

Also show a comparison row or chart referencing published LLM extraction baselines if available.

**Script:**

> "Now let's look at the results.
>
> We evaluated across all 5 PURE datasets using weighted combination matching — verse overlap at 1.0, acceptance criteria at 0.7, description at 0.5, with a 0.35 threshold.
>
> On Get Real 0.2, ReqTracer achieved an F1 score of 74%, recall of 83%, and requirement type accuracy of 92%.
>
> On Mashboot, F1 was also 74%, with recall notably higher at 89% and type accuracy of 98%.
>
> The other datasets — Space Fractions at 57%, Inventory at 58%, and Gamma J at 34% — show the range of performance across different document types.
>
> Type accuracy is consistently strong, ranging from 77% to 98% — the constrained decoding effectively guides the model toward correct classification."

---

## Section 7 — Key Innovations [6:00 – 6:40]

**On Screen:** Three-column or icon-based slide:

1. **Constrained Decoding** — JSON schema enforcement, consistent output
2. **Confidence Assessment** — Flagging ambiguous items for human review
3. **Tree-of-Thought Clarification** — LLM-generated questions to resolve ambiguity

**Script:**

> "I want to highlight three key innovations in our approach.
>
> First, constrained decoding. By forcing the LLM output into a strict JSON schema, we eliminate hallucinated fields and guarantee that every extraction follows the same structure. This is critical for downstream processing.
>
> Second, our confidence assessment system. Rather than presenting all results as equally reliable, the tool identifies which extractions the model was uncertain about and flags them for human review. This is a much more honest and useful approach than pretending every output is equally trustworthy.
>
> Third, Tree-of-Thought clarification. Instead of leaving ambiguous requirements unaddressed, the system actively generates clarifying questions — engaging the engineer in a structured dialogue to improve requirement quality."

---

## Section 8 — Limitations & Future Work [6:40 – 7:20]

**On Screen:** Bullet list:
- Over-extraction: some non-requirement text captured
- API latency: parallelism helps but cloud LLM calls add delay
- Future: fine-tuning on domain-specific SRS data, local model deployment, batch processing enhancements

**Script:**

> "Of course, there are limitations.
>
> The most common issue is over-extraction — the system occasionally captures sentences that look like requirements but are actually design decisions or rationale. This is the trade-off for high recall, and our confidence scoring helps engineers identify these cases.
>
> API latency is another factor. Processing large documents requires multiple LLM calls, and even with parallelism, there's inherent network latency. For production use, fine-tuning a smaller model on SRS-specific data could eliminate the API dependency and significantly speed up extraction.
>
> Other areas for future work include local model deployment with quantized models, batch processing for multiple documents, and integrating with issue tracking systems for end-to-end traceability."

---

## Section 9 — AI Usage Disclosure [7:20 – 7:40]

**On Screen:** Simple disclosure text on a clean slide:

> "AI Usage Disclosure: Large language models (Gemma-4-26B via Nous API) were used for requirement extraction and analysis as the core function of this tool. AI assistance was also used for code development, documentation drafting, and script preparation. All outputs were verified and validated against ground truth datasets."

**Script:**

> "For transparency — AI is both the subject and a tool in this project. The LLM-based extraction is the core functionality of ReqTracer. Additionally, AI coding assistants were used during development for boilerplate generation and debugging, and AI tools assisted with documentation and presentation preparation. All outputs were independently verified against ground truth datasets.
>
> Thank you for watching."

---

## Recording Tips

- **Pacing:** Each section's timestamp is approximate. If you run long, trim from Section 5 (demo) by showing fewer requirement examples rather than cutting any section entirely.
- **Transition pauses:** Leave 1-2 seconds of silence between sections — this makes editing easier.
- **Screen recording:** Use a tool like OBS or QuickTime. Record at 1080p minimum. Keep your mouse movements minimal and deliberate.
- **Audio:** Use an external microphone if possible. Record in a quiet room. Do a 30-second test recording to check levels before the full take.
- **Backup:** If the live demo is unreliable, pre-record the demo portion separately and insert it during editing.

---

*Script prepared for ReqTracer final project presentation.*
