import pandas as pd

def parse_uploaded_file(uploaded_file):
    filename = uploaded_file.name.lower()

    try:
        # Try reading as Excel
        df = pd.read_excel(uploaded_file)

        # Identify useful columns
        col_map = {
            "Loss Ratio": ["loss ratio", "loss %"],
            "Growth": ["growth", "premium growth"],
            "Retention": ["retention"]
        }

        def find_column(possibilities):
            for col in df.columns:
                for possible in possibilities:
                    if possible in str(col).lower():
                        return col
            return None

        loss_col = find_column(col_map["Loss Ratio"])
        growth_col = find_column(col_map["Growth"])
        retention_col = find_column(col_map["Retention"])

        loss_val = df[loss_col].mean() if loss_col else None
        growth_val = df[growth_col].mean() if growth_col else None
        retention_val = df[retention_col].mean() if retention_col else None

        return {
            "Carrier Name": infer_carrier_from_filename(filename),
            "Line of Business": "Commercial" if "cl" in filename else "Personal",
            "Loss Ratio (%)": round(loss_val, 1) if loss_val else "N/A",
            "Growth (%)": round(growth_val, 1) if growth_val else "N/A",
            "Retention (%)": round(retention_val, 1) if retention_val else "N/A",
            "Report": extract_report_date_from_filename(filename)
        }

    except Exception:
        return {
            "Carrier Name": infer_carrier_from_filename(filename),
            "Line of Business": "Unknown",
            "Loss Ratio (%)": "Error",
            "Growth (%)": "Error",
            "Retention (%)": "Error",
            "Report": "Unknown"
        }

def infer_carrier_from_filename(filename):
    name = filename.replace(".xlsx", "").replace(".xls", "").replace(".pdf", "")
    return name.replace("_", " ").replace("-", " ").title()

def extract_report_date_from_filename(filename):
    for part in filename.split("_"):
        if part.startswith("20") and len(part) == 6:  # e.g., 202405
            return f"{part[:4]}-{part[4:]}"
    return "Unknown"
