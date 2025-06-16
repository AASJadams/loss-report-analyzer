import streamlit as st
import pandas as pd

# Try importing the parser with safety
try:
    from parser import parse_file
except Exception as e:
    st.error(f"Parser failed to load: {e}")
    st.stop()

st.title("Loss Report Analyzer")

uploaded_files = st.file_uploader("Upload carrier reports", accept_multiple_files=True, type=["pdf", "xlsx"])

results = []

if uploaded_files:
    for file in uploaded_files:
        try:
            parsed = parse_file(file, file.name)
            parsed["Filename"] = file.name
            results.append(parsed)
        except Exception as e:
            results.append({
                "Carrier Name": "Unknown",
                "Loss Ratio (%)": f"Error: {e}",
                "Growth (%)": "Error",
                "Retention (%)": "Error",
                "Report": "Unknown",
                "Filename": file.name
            })

    df = pd.DataFrame(results)
    st.dataframe(df)
    st.download_button("Download CSV", df.to_csv(index=False), "results.csv", "text/csv")
