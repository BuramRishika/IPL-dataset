import streamlit as st
import json

st.set_page_config(page_title="IPL Data Analysis Questions", page_icon="❓", layout="wide")

st.title("🏏 IPL Data Analysis — Questions")

# Load your IPL notebook file
NOTEBOOK_FILE = "IPL (1).ipynb"

try:
    with open(NOTEBOOK_FILE, "r", encoding="utf-8") as f:
        nb = json.load(f)
except FileNotFoundError:
    st.error("❌ Notebook file not found! Please make sure 'IPL (1).ipynb' is in your repo.")
    st.stop()

# Extract questions (from markdown and code comments)
questions = []

for cell in nb.get("cells", []):
    # Check markdown cells (normal notebook text)
    if cell["cell_type"] == "markdown":
        text = "".join(cell["source"]).strip()
        # Lines containing '?' are treated as questions
        for line in text.splitlines():
            if "?" in line:
                questions.append(line.strip())

    # Check code comments starting with '#' that include a question
    elif cell["cell_type"] == "code":
        for line in cell.get("source", []):
            if line.strip().startswith("#") and "?" in line:
                q = line.strip("# ").strip()
                questions.append(q)

# Display all questions neatly
if questions:
    st.success(f"✅ Found {len(questions)} questions in the notebook.")
    for i, q in enumerate(questions, start=1):
        st.markdown(f"### ❓ Q{i}. {q}")
else:
    st.warning("⚠️ No questions found in the notebook.")
