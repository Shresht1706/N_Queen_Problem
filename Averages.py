import csv

def append_averages_by_n(input_csv_path: str, target_n: int, output_csv_path: str = "Averages.csv"):
    """
    Reads data from input_csv_path, filters rows where the first value == target_n,
    computes column-wise averages (excluding the first column),
    and appends the result to output_csv_path.
    """
    filtered_rows = []

    # Read the input CSV and collect rows matching N
    with open(input_csv_path, newline='') as infile:
        reader = csv.reader(infile)
        for row in reader:
            float_row = list(map(float, row))
            if int(float_row[0]) == target_n:
                filtered_rows.append(float_row)

    # Return early if no matching rows
    if not filtered_rows:
        print(f"⚠️ No rows found for N = {target_n} in {input_csv_path}")
        return

    # Compute averages excluding the first column (N)
    num_cols = len(filtered_rows[0])
    averages = [target_n]
    for col in range(1, num_cols):
        avg = sum(row[col] for row in filtered_rows) / len(filtered_rows)
        averages.append(round(avg, 2))

    # Append the averages to the output CSV
    with open(output_csv_path, "a", newline="") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(averages)
        writer.writerow(output_csv_path)

    print(f"✅ Averages for N = {target_n} appended to {output_csv_path}")


append_averages_by_n("HCNQ_Results.csv", 50)