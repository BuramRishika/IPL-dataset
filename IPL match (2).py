import streamlit as st
import pandas as pd
import json
import io
import contextlib

st.set_page_config(page_title="🏏 IPL Q&A Dashboard", page_icon="🏆", layout="wide")
st.title("🏏 IPL Data Analysis Dashboard")
data = pd.read_csv("matches(1).csv")
uploaded_file = st.file_uploader("Upload your IPL CSV file", type="csv")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)  # optional
    st.success("✅ File uploaded successfully!")
else:
    st.info("Please upload your IPL dataset (.csv) file.")
# Show dataset preview
st.subheader("Dataset Preview")
st.dataframe(data.head())


# --- Load Notebook ---
NOTEBOOK_FILE = "IPL match (3).ipynb"
try:
    with open(NOTEBOOK_FILE, "r", encoding="utf-8") as f:
        nb = json.load(f)
except FileNotFoundError:
    st.error("❌ Notebook file 'IPL match (3).ipynb' not found!")
    st.stop()

# --- Extract Questions and Code ---
qa_pairs = []
current_question = None

for cell in nb.get("cells", []):
    if cell["cell_type"] == "markdown":
        text = "".join(cell["source"]).strip()
        if "?" in text:
            current_question = text
    elif cell["cell_type"] == "code":
        lines = cell.get("source", [])
        for line in lines:
            if line.strip().startswith("#") and "?" in line:
                current_question = line.strip("# ").strip()
        if current_question:
            code = "".join(lines).strip()
            qa_pairs.append((current_question, code))
            current_question = None

# --- Display Questions and Direct Answers ---
for i, (question, code) in enumerate(qa_pairs, start=1):
    st.markdown(f"### ❓ Q{i}: {question}")

    local_env = {"data": data, "pd": pd}
    output_buffer = io.StringIO()

    try:
        # Capture printed and final outputs
        with contextlib.redirect_stdout(output_buffer):
            exec(code, local_env)
        output_text = output_buffer.getvalue().strip()

        # Find the last meaningful variable (answer)
        results = {
            k: v for k, v in local_env.items()
            if k not in ["pd", "data", "__builtins__"] and not k.startswith("_")
        }

        # Display only the clean answer
        if output_text:
            st.write(f"🟩 **Answer:** {output_text}")
        elif results:
            for val in results.values():
                # Convert all answers to readable strings
                if isinstance(val, (pd.DataFrame, pd.Series, list, tuple, set)):
                    answer = ", ".join(map(str, list(val)[:5])) + ("..." if len(val) > 5 else "")
                    st.write(f"🟩 **Answer:** {answer}")
                else:
                    st.write(f"🟩 **Answer:** {val}")
        else:
            st.info("ℹ️ No visible output for this question.")
    except Exception as e:
        st.error(f"⚠️ Error executing code: {e}")

    st.divider()

                     
