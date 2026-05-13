# Final Project Deliverables

Kasetsart University — 01219462 Software Engineering for AI-Enabled System
Project: Requirement Traceability Helper Using LLM

---

## Directory Structure

```
final-project-deliverables/
├── part-a-system-design/          # Part A — System Design Document
│   └── PART_A_System_Design.md   # Export to PDF for submission
├── part-b-notebooks/              # Part B — Jupyter Notebooks
│   ├── B1_Data_Exploration.ipynb
│   ├── B2_Model_Training.ipynb
│   ├── B3_Model_Fairness.ipynb
│   ├── B4_Model_Versioning.ipynb
│   ├── B5_Model_Explainability.ipynb
│   ├── B6_Prediction_Reasoning.ipynb
│   └── B7_Model_Deployment.ipynb
├── part-c-ui-interface/           # Part C — UI Design + Interface Contract
│   ├── C1_UI_Design.md
│   ├── C2_Interface_Design.md
│   ├── mockup_dashboard.html
│   ├── mockup_results.html
│   ├── mockup_confidence.html
│   └── mockup_clarification.html
├── part-c-api-tests/              # Part C — API Testing
│   ├── C3_API_Tests.postman_collection.json
│   └── C3_Test_Documentation.md
├── mlflow-experiments/            # MLflow Tracking
│   ├── mlruns.db
│   └── screenshots/
│       ├── chart_get_real.png          # Get Real 0.2 - metrics by run
│       ├── chart_mashboot.png          # Mashboot - metrics by run
│       ├── chart_space_fractions.png   # Space Fractions - metrics by run
│       ├── chart_inventory.png          # Inventory - metrics by run
│       ├── chart_gamma_j.png           # Gamma J - metrics by run
│       ├── chart_5dataset_f1.png       # All 5 datasets F1 comparison
│       ├── chart_type_accuracy.png     # Type classification accuracy across runs
│       └── chart_union_recall.png      # Union recall comparison
├── model-artifacts/               # B7 — Model Artifacts
│   ├── MLmodel
│   ├── model.pkl
│   └── model_config.json
├── slides-content/
│   └── SLIDES.md                  # Slide deck content for Google Slides
├── video-script/
│   └── VIDEO_SCRIPT.md            # Video presentation script
└── scripts/                       # Helper scripts
    ├── run_mlflow_experiments.py
    └── generate_mlflow_charts.py
```

## How to Use

### Run Notebooks
Open each `.ipynb` in Jupyter and click "Run All":
```bash
cd ~/Final_Project/Requirement-extraction
uv run jupyter notebook ~/Final_Project/final-project-deliverables/part-b-notebooks/
```

### View MLflow UI
```bash
cd ~/Final_Project/Requirement-extraction
uv run mlflow ui --backend-store-uri sqlite:///../final-project-deliverables/mlflow-experiments/mlruns.db
```
Then open http://localhost:5000 in your browser.

### Run Postman Tests
1. Install Postman Desktop
2. File → Import → `C3_API_Tests.postman_collection.json`
3. Start the API server: `cd ~/Final_Project/Requirement-extraction && uv run uvicorn app.main:app --port 8100`
4. Run the collection against `http://localhost:8100`

### View HTML Mockups
Open any `mockup_*.html` file in a browser.

### Create Slides
Copy content from `SLIDES.md` into Google Slides.

### Create Video
Follow `VIDEO_SCRIPT.md` for screen recording.

### Export Part A to PDF
Open `PART_A_System_Design.md` → Print/Export as PDF.
