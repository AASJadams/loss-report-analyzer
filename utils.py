import io

def classify_and_export_csv(df):
    output = io.StringIO()
    df.to_csv(output, index=False)
    return output.getvalue()
