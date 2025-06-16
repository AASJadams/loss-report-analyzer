import streamlit as st
import pandas as pd
from parser import parse_uploaded_file
from utils import classify_and_export_csv

KNOWN_CARRIERS = sorted([
    "Berkshire Hathaway GUARD Ins Co CL", "EMC Underwriters", "FCCI Insurance Company",
    "Foremost/Bristol West (7# all numbers) PL/CL", "Liberty Mutual Insurance",
    "Markel Insurance Co CL", "Mercury CL", "Nationwide CL", "The Hartford", "Travelers CL",
    "Utica National Insurance Group", "Accident Fund", "Acuity Insurance CL",
    "AmTrust North America, Inc.", "Chubb CL", "Mountain States Insurance Group (Donegal)",
    "SECURA Insurance Companies", "Texas Mutual Insurance Company", "Branch Insurance Exchange",
    "Chubb PL", "Clearcover", "Germania", "Homeowners of America Insurance Company (HOAIC)",
    "Lemonade Insurance Company", "Mercury PL", "National General", "Nationwide PL", "Openly",
    "Progressive PL", "Safeco", "Stillwater Insurance Group PL", "Travelers PL",
    "Foremost Star/Choice PL (9# all numbers)"
])

st.set_page_config(page_title="Carrier Loss Report Analyzer", layout="centered")

st.markdown(
    '''
    <style>
        html, body, [data-testid="stAppViewContainer"] {
            background-color: #07385e;
            color: #fec52d;
        }
        header[data-testid="stHeader"] {
            background-color: #87212e;
        }
        h1, h2, h3, h4, h5, h6, p, label, span, div {
            color: #fec52d !important;
        }
        input, textarea, .stTextInput, .stTextArea, .stFileUploader label {
            color: #07385e !important;
            font-weight: bold;
        }
        section[data-testid="stFileUploader"] label {
            color: #07385e !important;
            font-weight: bold;
        }
        button[kind="primary"] {
            background-color: #07385e !important;
            color: #fec52d !important;
            border: 1px solid #fec52d !important;
        }
        button[kind="primary"]:hover {
            background-color: #052742 !important;
            color: #ffffff !important;
        }
    </style>
    ''',
    unsafe_allow_html=True
)

st.title("Carrier Loss Report Analyzer")

st.markdown("""
Upload your monthly loss ratio reports from carriers below.

Supports PDF, XLS, and XLSX formats.  
After uploading, unrecognized carrier names will prompt you to select from your list.
""")

uploaded_files = st.file_uploader("Upload Carrier Reports", accept_multiple_files=True, type=["pdf", "xls", "xlsx"])

manual_overrides = {}
file_carrier_guess = {}

if uploaded_files:
    st.markdown("### Review Detected Carriers")

    for i, file in enumerate(uploaded_files):
        result = parse_uploaded_file(file)
        guess = result["Carrier Name"]
        file_id = file.name

        if guess not in KNOWN_CARRIERS:
            selection = st.selectbox(
                f"Unknown carrier for '{file.name}' (guessed: '{guess}')",
                KNOWN_CARRIERS,
                key=f"select_{file_id}_{i}"
            )
            manual_overrides[file_id] = selection
        else:
            manual_overrides[file_id] = guess

        file_carrier_guess[file_id] = result

    if st.button("Analyze Reports"):
        all_data = []
        for file in uploaded_files:
            file_id = file.name
            result = file_carrier_guess[file_id]
            result["Carrier Name"] = manual_overrides[file_id]
            all_data.append(result)

        if all_data:
            df = pd.DataFrame(all_data)
            st.success("Parsing complete!")
            st.dataframe(df)

            csv = classify_and_export_csv(df)
            st.download_button("Download CSV", data=csv, file_name="Carrier_Loss_Report_Summary.csv", mime="text/csv")
