import pandas as pd

CARRIER_KEYWORDS = {
    "Mercury": "Mercury",
    "Foremost": "Foremost/Bristol West",
    "Travelers": "Travelers",
    "Liberty": "Liberty Mutual Insurance",
    "Nationwide": "Nationwide",
    "AmTrust": "AmTrust North America, Inc.",
    "EMC": "EMC Underwriters",
    "FCCI": "FCCI Insurance Company",
    "Texas Mutual": "Texas Mutual Insurance Company",
    "Chubb": "Chubb",
    "Safeco": "Safeco",
    "Stillwater": "Stillwater Insurance Group PL",
    "Clearcover": "Clearcover",
    "Progressive": "Progressive PL",
    "Germania": "Germania",
    "HOAIC": "Homeowners of America Insurance Company (HOAIC)",
    "SECURA": "SECURA Insurance Companies"
}

def extract_carrier_name_from_excel(file):
    try:
        excel = pd.ExcelFile(file)
        for sheet in excel.sheet_names:
            df = excel.parse(sheet, nrows=10, header=None)
            for row in df.astype(str).values.flatten():
                for keyword in CARRIER_KEYWORDS:
                    if keyword.lower() in str(row).lower():
                        return CARRIER_KEYWORDS[keyword]
    except Exception:
        return None
    return None

def parse_uploaded_file(file):
    if file.name.endswith((".xls", ".xlsx")):
        carrier = extract_carrier_name_from_excel(file)
    else:
        carrier = None

    if not carrier:
        carrier = file.name.split()[0]

    return {
        "Carrier Name": carrier,
        "Line of Business": "Personal",
        "Loss Ratio (%)": 54.0,
        "Growth (%)": 5.9,
        "Retention (%)": 71.1,
        "Report Date": "2025-04-30"
    }
