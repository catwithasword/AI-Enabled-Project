"""Fix broken notebooks by rewriting them with proper JSON encoding."""
import json
import os

base = "/Users/xd/Final_Project/final-project-deliverables/part-b-notebooks"

broken = {
    # filename -> number of cells to verify
    "B1_Data_Exploration.ipynb": None,
    "B2_Model_Training.ipynb": None,
    "B4_Model_Versioning.ipynb": None,
    "B5_Model_Explainability.ipynb": None,
    "B7_Model_Deployment.ipynb": None,
}

for fname in broken:
    fp = os.path.join(base, fname)
    with open(fp, 'r', encoding='utf-8') as fh:
        lines = fh.readlines()
    
    # Find all lines that look like JSON values but aren't quoted
    # The pattern is lines that start with "   - " inside a "source" array
    # instead of "   "- " (properly quoted)
    fixed_lines = []
    in_source = False
    for i, line in enumerate(lines):
        stripped = line.lstrip()
        if '"source":' in line:
            in_source = True
        if in_source and stripped.startswith(']') and stripped.strip() == '],':
            in_source = False
        if in_source and (stripped.startswith('- ') or stripped.startswith('"- ')):
            # This line is a bare markdown list item or improperly quoted
            # Wrap it in quotes
            if stripped.startswith('- ') and not stripped.startswith('"- '):
                indent = len(line) - len(stripped)
                fixed_lines.append(' ' * indent + '"- \\n",\n')
                continue
    
    content = ''.join(fixed_lines)
    
    try:
        json.loads(content)
        print(f"  {fname}: FIXED by line replacement")
    except json.JSONDecodeError as e:
        print(f"  {fname}: Still broken at pos {e.pos}, line {e.lineno}")
        # Need a different approach - rewrite from scratch
