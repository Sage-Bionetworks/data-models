import argparse
import csv
import os


def find_csv_files(directory: str) -> list:
    """Find all CSV files in a directory recursively"""
    csv_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".csv"):
                csv_files.append(os.path.join(root, file))
    return csv_files


def combine_csv_files(csv_files: list) -> list:
    """combine CSV files into one list of rows"""
    combined_rows = []
    header_written = False
    
    for file in csv_files:
        with open(file, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)
            # Only process if file has content
            if rows:
                if not header_written:
                    # Include header for first file
                    combined_rows.extend(rows)
                    header_written = True
                else:
                    # Skip header for subsequent files
                    combined_rows.extend(rows[1:])
    
    return combined_rows


def main(input_directory: str, output_file: str):
    """Assemble CSV data model"""
    csv_files = find_csv_files(input_directory)
    if not csv_files:
        print(f"No CSV files found in the directory: {input_directory}")
        return

    combined_rows = combine_csv_files(csv_files)

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(combined_rows)
    print(f"Combined CSV files saved to {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Combine CSV files in a directory.")
    parser.add_argument("input_directory", help="Input directory containing CSV files")
    parser.add_argument("output_file", help="Output CSV file name")

    args = parser.parse_args()
    main(input_directory=args.input_directory, output_file=args.output_file)
