# C3 — Interface Testing: Test Documentation

## Overview

This document describes the interface testing materials for the MuSEE + Constrained Decoding Requirement Extraction Service (FastAPI, port 8100). The testing is performed via a Postman Collection v2.1 that validates all API endpoints using realistic SRS text excerpts from the PURE dataset.

---

## Test Scenarios

### Scenario 1: Get Real 0.2 SRS — Full Extraction + Confidence + Clarification

**Domain:** Get Real 0.2 — A college CS career website SRS document. The text excerpt contains functional requirements (search systems, Q&A feedback, usage analytics, content display) and non-functional requirements (browser compatibility, server response time, security conventions).

#### Step 1a: POST /extract/text

**Input:**
```json
{
  "document_name": "get-real-0.2",
  "text": "<SRS excerpt with ~10 paragraphs covering browser testing, search features, Q&A system, analytics, and video content>"
}
```

**Expected Output:**
- HTTP 200
- Response body with fields: `document`, `requirements` (array), `total_requirements` (int), `functional` (int), `non_functional` (int)
- Each requirement has: `requirement_id` (REQ-NNN), `title`, `description`, `type` (functional/non-functional), `acceptance_criteria` (array), `source_location.document`, `source_location.verse` (array)
- `total_requirements == len(requirements)`
- `functional + non_functional == total_requirements`

**Assertions (pm.test):**
- Status code is 200
- Response has all required top-level fields
- Requirements array is non-empty
- Each requirement has valid REQ-NNN ID format, non-empty title/description, valid type enum, and source_location with non-empty document and verse
- Counters are internally consistent

#### Step 1b: POST /assess/confidence

**Input:** The `requirements` array from step 1a (sent as raw JSON array of ExtractedRequirement objects).

**Expected Output:**
- HTTP 200
- `documents` array where each entry has `document` name and `flags` (object mapping requirement_id → array of ConfidenceFlag)
- Each ConfidenceFlag has: `field` (enum), `issue` (string), `severity` (low/medium/high), `suggestion` (optional string)

**Assertions:**
- Status code is 200
- `documents` is a non-empty array
- Each flag has valid structure with proper enum values

#### Step 1c: POST /assess/clarify

**Input:** Flagged requirements with their confidence flags, plus document name.
```json
{
  "flagged_requirements": [<array of requirements that have high/medium severity flags>],
  "document_name": "get-real-0.2"
}
```

**Expected Output:**
- HTTP 200
- `document`, `questions` (array), `total_questions` (int)
- Each question has: `requirement_id`, `question`, `reasoning_path`, `choices` (array)

**Assertions:**
- Status code is 200
- All required fields present
- Questions array is non-empty (given flagged input)
- Each question has valid structure
- `total_questions == len(questions)`

---

### Scenario 2: Mashboot SRS — Extraction + Confidence Assessment

**Domain:** Mashboot — A social media campaign management tool SRS. The excerpt contains role-based access control (Contributor, Approver, Publisher), user account management, password reset, campaign components, scheduling, and security (TLS encryption, data backup).

#### Step 2a: POST /extract/text

**Input:**
```json
{
  "document_name": "mashboot",
  "text": "<SRS excerpt with numbered requirements about roles, account creation, password reset, campaign components, encryption, backup>"
}
```

**Expected Output:** Same structure as Scenario 1 step 1a, but with function-heavy content (Mashboot has ~88% functional requirements).

**Assertions:**
- All standard structure checks
- Additional assertion: `functional > non_functional` (Mashboot is function-heavy)
- Each requirement has source_location with non-empty verse array

#### Step 2b: POST /assess/confidence

**Input:** A 3-element subset of extracted requirements, representing diverse types (encrypted data, role-based access, scheduling).

**Expected Output:** Same structure as Scenario 1 step 1b.

**Assertions:**
- Status code is 200
- All documents have valid structure
- All flag fields match the RequirementField enum: `title`, `description`, `type`, `acceptance_criteria`, `source_location`
- All severity values are valid: `low`, `medium`, `high`

---

### Scenario 3: Integration Flow — Extract → Assess → Integrate

**Domain:** Get Real 0.2 — A second, shorter excerpt focusing on site benefits, target audience, and OUS domain integration.

#### Step 3a: POST /extract/text

**Input:** SRS text about site benefits, target audiences, and hosting.

**Expected Output:** Standard extraction result.

**Assertions:** Standard structure checks on all extracted requirements.

#### Step 3b: POST /assess/confidence

**Input:** Requirements from step 3a.

**Expected Output:** Confidence assessment with field-level flags.

**Assertions:** Standard structure checks. Confidence results stored for integration step.

#### Step 3c: POST /assess/integrate

**Input:**
```json
{
  "document_name": "get-real-0.2",
  "requirements": [<original ExtractedRequirement objects>],
  "answers": [
    {
      "requirement_id": "REQ-001",
      "question": "<clarification question about career info types>",
      "answer": "<user's specific answer with concrete details>",
      "reasoning_path": "scope"
    },
    {
      "requirement_id": "REQ-001",
      "question": "<clarification question about update frequency>",
      "answer": "<user's answer with specific timeframes>",
      "reasoning_path": "scope"
    },
    {
      "requirement_id": "REQ-002",
      "question": "<clarification question about audience differentiation>",
      "answer": "<user's answer about landing page design>",
      "reasoning_path": "scope"
    }
  ]
}
```

**Expected Output:**
- HTTP 200
- `document`, `requirements` (updated array), `total_requirements`, `functional`, `non_functional`
- Requirements should show LLM-refined descriptions that incorporate the user's clarifying answers (more concrete, testable language)

**Assertions:**
- Status code is 200
- All required fields present
- Each updated requirement maintains valid structure (REQ-NNN ID, non-empty title/description, valid type, source_location)
- Counters are consistent

---

### Health Check

#### GET /health

**Expected Output:**
```json
{
  "status": "ok",
  "service": "requirement-extraction"
}
```

**Assertions:**
- Status code is 200
- Response has `status` field with value `"ok"`
- Response has `service` identifier field

---

## Expected Inputs and Outputs Summary

| Endpoint | Method | Input | Output |
|----------|--------|-------|--------|
| `/health` | GET | None | `{"status": "ok", "service": "..."}` |
| `/extract/text` | POST | `{"document_name": str, "text": str}` | `{"document": str, "requirements": [ExtractedRequirement], "total_requirements": int, "functional": int, "non_functional": int}` |
| `/assess/confidence` | POST | `[ExtractedRequirement, ...]` (raw array) | `{"documents": [{"document": str, "flags": {req_id: [ConfidenceFlag]}}]}` |
| `/assess/clarify` | POST | `{"flagged_requirements": [FlaggedRequirement], "document_name": str}` | `{"document": str, "questions": [ClarificationQuestion], "total_questions": int}` |
| `/assess/integrate` | POST | `{"requirements": [ExtractedRequirement], "answers": [ClarificationAnswer], "document_name": str}` | `{"document": str, "requirements": [ExtractedRequirement], "total_requirements": int, "functional": int, "non_functional": int}` |

---

## Challenges Encountered and Resolutions

### 1. Confidence endpoint expects raw JSON array (not wrapped in object)

**Challenge:** Unlike all other endpoints, `POST /assess/confidence` takes a raw JSON array of `ExtractedRequirement` objects as the request body, not an object like `{"requirements": [...]}`. This is because the FastAPI route parameter is `requirements: list[ExtractedRequirement]` without a Pydantic wrapper model.

**Resolution:** The Postman collection sends the requirements array directly as raw JSON body for this endpoint. The pre-request script copies the saved requirements from the extraction step's environment variable into the request body.

### 2. Inter-request data passing in Postman

**Challenge:** The confidence assessment requires the exact requirements from the extraction response. Postman tests run after the request, so we need a way to pass data between sequential requests.

**Resolution:** Each extraction request's test script saves the requirements JSON to a Postman environment variable (`scenario1_requirements_json`). The subsequent confidence request's pre-request script reads this variable and sets the request body. This creates a data pipeline: extract → save env var → pre-request reads → confidence assess.

### 3. Clarify endpoint needs flagged requirements with embedded flags

**Challenge:** The `/assess/clarify` endpoint expects `FlaggedRequirement` objects, which have a `flags` field containing the `ConfidenceFlag` objects from the confidence assessment — not just the raw extracted requirements.

**Resolution:** The confidence test's test script identifies requirements with medium/high severity flags, pairs them with their flag data from the confidence response, and stores the combined `FlaggedRequirement` objects in an environment variable. The clarify pre-request script reads this and constructs the proper request body.

### 4. LLM endpoint timeouts

**Challenge:** When the underlying LLM is slow (particularly with Nous API backends), extraction requests can take 60+ seconds per chunk. Large documents may cause Postman timeouts.

**Resolution:** The collection uses small SRS excerpts (~500-1500 characters) that fit in a single chunk, minimizing LLM call count. If using the collection against a live server, increase the Postman request timeout to 120 seconds (Settings → General → Request timeout in ms).

### 5. Schema validation for confidence flags

**Challenge:** The LLM-based confidence assessment might produce flags with unexpected field names or severity values that don't match the Pydantic enum.

**Resolution:** The Postman test assertions validate that all flag fields are one of the valid `RequirementField` enum values (`title`, `description`, `type`, `acceptance_criteria`, `source_location`) and all severity values are one of `low`, `medium`, `high`. This catches schema violations early.

### 6. Integrating user answers back into requirements

**Challenge:** The `/assess/integrate` endpoint's output depends on the LLM rewriting requirement descriptions based on user answers — the output is non-deterministic in terms of exact text content, though the schema is deterministic.

**Resolution:** Assertions focus on structural validity (valid ID format, non-empty fields, correct types, consistent counters) rather than exact content. Content quality is verified through the documentation describing expected refinements.

---

## How to Run the Postman Collection

### Prerequisites

1. **Server running:** The FastAPI service must be running at `localhost:8100`.

   ```bash
   cd ~/Final_Project/Requirement-extraction
   uv run uvicorn app.main:app --host 0.0.0.0 --port 8100
   ```

   Verify with: `curl http://localhost:8100/health`
   Expected: `{"status":"ok","service":"requirement-extraction"}`

2. **Postman installed:** Postman desktop app (or use Newman CLI).

3. **Environment configured:** The collection uses `{{base_url}}` variable. It defaults to `http://localhost:8100` in the collection variables. Override by creating a Postman environment with `base_url = http://localhost:8100`.

### Running in Postman Desktop

1. Open Postman.
2. Click **Import** → File → select `C3_API_Tests.postman_collection.json`.
3. The collection "C3 — MuSEE Requirement Extraction API Tests" appears in the sidebar.
4. Create an environment (optional, not required since collection has default variable):
   - Click Environments → Create → Name: `Local`
   - Add variable `base_url` with value `http://localhost:8100`
   - Select the environment in the top-right dropdown.
5. Run requests individually by clicking them, or run the entire collection:
   - Click the collection name → **Run** (Collection Runner).
   - Set iterations to 1.
   - Click **Run C3 — MuSEE Requirement Extraction API Tests**.

**Important:** Run Scenario 1 requests (1a, 1b, 1c) in order. Step 1b depends on data saved by 1a. Step 1c depends on data saved by 1b. Similarly, Scenario 3 (3a, 3b, 3c) must run sequentially. Scenario 2 requests (2a, 2b) also run in order.

### Running with Newman (CLI)

Install Newman:
```bash
npm install -g newman
```

Run the collection:
```bash
newman run /Users/xd/Final_Project/final-project-deliverables/part-c-api-tests/C3_API_Tests.postman_collection.json \
  --env-var "base_url=http://localhost:8100" \
  --timeout 120000
```

The `--timeout 120000` flag sets a 120-second timeout per request to accommodate slow LLM responses.

### Running with JSON output (for CI/CD)

```bash
newman run C3_API_Tests.postman_collection.json \
  --env-var "base_url=http://localhost:8100" \
  --timeout 120000 \
  --reporters cli,json \
  --reporter-json-export test-results.json
```

---

## Collection Structure

```
C3 — MuSEE Requirement Extraction API Tests
├── 0 — Health Check
│   └── GET /health
├── 1 — Scenario 1: Get Real 0.2 SRS Extraction
│   ├── 1a — POST /extract/text (Get Real 0.2)
│   ├── 1b — POST /assess/confidence (Get Real 0.2)
│   └── 1c — POST /assess/clarify (Get Real 0.2)
├── 2 — Scenario 2: Mashboot SRS Extraction
│   ├── 2a — POST /extract/text (Mashboot)
│   └── 2b — POST /assess/confidence (Mashboot)
└── 3 — Scenario 3: Integration Flow
    ├── 3a — POST /extract/text (Get Real 0.2)
    ├── 3b — POST /assess/confidence (Get Real 0.2)
    └── 3c — POST /assess/integrate (User Answers)
```

Total: 1 collection, 3 scenario folders, 8 requests, 30+ test assertions.

---

## Files

| File | Description |
|------|-------------|
| `C3_API_Tests.postman_collection.json` | Postman Collection v2.1 with all test scenarios, requests, and pm.test assertions |
| `C3_Test_Documentation.md` | This documentation file |

Both files are located in: `/Users/xd/Final_Project/final-project-deliverables/part-c-api-tests/`
