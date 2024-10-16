import camelot
import pandas as pd

def extract_data_from_pdf(pdf_path, output_csv):
    """Extracts tables from PDF and saves them as CSV."""

    tables = camelot.read_pdf(pdf_path, pages='50-56') 

    for i, table in enumerate(tables):
        df = table.df
        df.to_csv(f"{output_csv}_{i}.csv", index=False)

if __name__ == "__main__":
    pdf_path = r"C:\Users\kiun\pod_lca\src\buildings\240P.pdf"
    output_csv = "output_data.csv"
    extract_data_from_pdf(pdf_path, output_csv)