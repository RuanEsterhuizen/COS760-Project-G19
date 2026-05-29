import csv

file = "../../data/mgts/quen2_5.csv"
expected_columns = 4

bad_rows = []

with open(file, "r", encoding="utf-8") as f:
    reader = csv.reader(f)

    for line_num, row in enumerate(reader, start=1):
        if len(row) != expected_columns:
            bad_rows.append((line_num, len(row), row))

print(f"Found {len(bad_rows)} bad rows")

for line_num, n_cols, row in bad_rows[:20]:
    print(f"Line {line_num}: {n_cols} columns")
    print(row)
    print("-" * 50)