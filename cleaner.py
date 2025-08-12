import io
import csv


def clean_csv(content: str) -> str:
    input_stream = io.StringIO(content)
    reader = csv.reader(input_stream)
    output = io.StringIO()
    writer = csv.writer(output)
    for row in reader:
        # Skip empty rows
        if any(cell.strip() for cell in row):
            writer.writerow([cell.strip() for cell in row])
    return output.getvalue()
