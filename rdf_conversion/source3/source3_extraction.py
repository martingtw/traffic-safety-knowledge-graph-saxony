from pathlib import Path
import pandas as pd
import re
import unicodedata

INPUT_DIR = "csv"
OUTPUT_DIR = "ttl_files"

Path(OUTPUT_DIR).mkdir(exist_ok=True)

def normalize_predicate(text):
    """
    Generate an RDF-compatible property name.
    """
    text = str(text)

    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")

    text = text.lower()

    text = re.sub(r"[^a-z0-9]+", "_", text)
    text = re.sub(r"_+", "_", text)

    return text.strip("_")

def detect_header(lines):
    """
    Finds the last header row before the actual data.
    Data rows start with:
        14511;Chemnitz...
    """
    data_start = None

    for i, line in enumerate(lines):
        if re.match(r"^\d+;", line):
            data_start = i
            break

    if data_start is None:
        return None, None

    header1 = lines[data_start - 2].strip().split(";")
    header2 = lines[data_start - 1].strip().split(";")

    return data_start, (header1, header2)

for csv_file in Path(INPUT_DIR).glob("*.csv"):

    print(f"\nProcessing: {csv_file.name}")

    with open(csv_file, "r", encoding="ISO-8859-1") as f:
        lines = f.readlines()

    data_start, headers = detect_header(lines)

    if data_start is None:
        print("No data found.")
        continue

    header1, header2 = headers

    # Read data
    df = pd.read_csv(
        csv_file,
        sep=";",
        encoding="ISO-8859-1",
        skiprows=data_start,
        header=None,
        dtype=str
    )

    # Generate column names
    columns = ["code", "name"]

    if len(df.columns) > 2:

        for idx in range(2, len(df.columns)):

            h1 = header1[idx] if idx < len(header1) else ""
            h2 = header2[idx] if idx < len(header2) else ""

            header_text = " ".join(
                x.strip()
                for x in [h1, h2]
                if x.strip()
            )

            if not header_text:
                header_text = f"value_{idx}"

            columns.append(
                normalize_predicate(header_text)
            )

    df.columns = columns[:len(df.columns)]

    ttl_path = Path(OUTPUT_DIR) / f"{csv_file.stem}.ttl"

    with open(ttl_path, "w", encoding="utf-8") as ttl:

        ttl.write("@prefix ex: <http://example.org/genesis/> .\n")
        ttl.write("@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n\n")

        dataset_name = normalize_predicate(csv_file.stem)

        for _, row in df.iterrows():

            code = str(row["code"]).strip()

            if code == "nan":
                continue

            name = str(row["name"]).strip()
            name = name.replace('"', '\\"')

            ttl.write(f"ex:{code}\n")
            ttl.write("    a ex:Dataset ;\n")
            ttl.write(f'    ex:name "{name}"')

            for col in df.columns[2:]:

                value = row[col]

                if pd.isna(value):
                    continue

                value = str(value).strip()

                if value in ["", ".", "-"]:
                    continue

                value = value.replace('"', '\\"')

                ttl.write(
                    f' ;\n    ex:{col} "{value}"'
                )

            ttl.write(" .\n\n")

    print(f"Saved RDF to: {ttl_path}")

print("\nDone.")