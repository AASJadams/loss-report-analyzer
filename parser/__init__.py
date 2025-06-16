import pandas as pd
import pdfplumber
import re
from PyPDF2 import PdfReader

def parse_file(file, carrier_name):
    try:
        carrier = carrier_name.lower()

        if "fcci" in carrier:
            return parse_fcci_pdf(file)
        elif "texas mutual" in carrier:
            return parse_texas_mutual_pdf(file)
        elif "amtrust" in carrier:
            return parse_amtrust_excel(file)
        else:
            return {
                "Carrier Name": carrier_name,
                "Loss Ratio (%)": "Not supported",
                "Growth (%)": "Not supported",
                "Retention (%)": "Not supported",
                "Report": "Unknown"
            }
    except Exception as e:
        return {
            "Carrier Name": carrier_name,
            "Loss Ratio (%)": f"Error: {str(e)}",
            "Growth (%)": "Error",
            "Retention (%)": "Error",
            "Report": "Unknown"
        }

def parse_fcci_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"

    lr_match = re.search(r"Total\s+\$[\d,]+\s+\$[\d,]+\s+(\d+\.\d+)%", text)
    loss_ratio = float(lr_match.group(1)) if lr_match else "N/A"

    wp_match = re.search(r"Total \(\$?\d+\)?\s+100.0%\s+\$([\d,]+)\s+0.0%\s+\$([\d,]+)\s+\$([\d,]+)", text)
    if wp_match:
        curr = int(wp_match.group(1).replace(",", ""))
        prev = int(wp_match.group(2).replace(",", ""))
        growth = round(((curr - prev) / prev) * 100, 2) if prev else "N/A"
    else:
        growth = "N/A"

    ret_match = re.search(r"TOTAL.*?\$[\d,]+\s+\d+\s+\$\d+\s+(\d+\.\d+)%", text)
    retention = float(ret_match.group(1)) if ret_match else "N/A"

    return {
        "Carrier Name": "FCCI Insurance Company",
        "Loss Ratio (%)": loss_ratio,
        "Growth (%)": growth,
        "Retention (%)": retention,
        "Report": "2025-03-31"
    }

def parse_texas_mutual_pdf(file):
    text = ""
    reader = PdfReader(file)
    for page in reader.pages:
        text += page.extract_text() + "\n"

    lr_match = re.search(r"Total\s+\$[\d,]+\s+\$[\d,]+\s+(\d+\.\d+)%", text)
    loss_ratio = float(lr_match.group(1)) if lr_match else "N/A"

    growth_match = re.search(r"Growth.*?(-?\d+\.\d+)%", text)
    growth = float(growth_match.group(1)) if growth_match else "N/A"

    retention_match = re.search(r"Retention.*?(\d+\.\d+)%", text)
    retention = float(retention_match.group(1)) if retention_match else "N/A"

    return {
        "Carrier Name": "Texas Mutual Insurance Company",
        "Loss Ratio (%)": loss_ratio,
        "Growth (%)": growth,
        "Retention (%)": retention,
        "Report": "2025-05-31"
    }

def parse_amtrust_excel(file):
    df = pd.read_excel(file, sheet_name=0)
    row = df.iloc[0]

    return {
        "Carrier Name": "AmTrust North America, Inc.",
        "Loss Ratio (%)": float(row.get("Loss Ratio", "N/A")),
        "Growth (%)": float(row.get("Growth %", "N/A")),
        "Retention (%)": float(row.get("Retention %", "N/A")),
        "Report": "2025-05"
    }
