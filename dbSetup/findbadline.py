import os


def find_problematic_line(file_path, encoding="utf-8"):
    chunk_size = 1024
    position = 0

    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break

            try:
                chunk.decode(encoding)  # If this throws an exception, decoding failed
            except UnicodeDecodeError as e:
                print(f"Decoding error at byte position {position + e.start}: {e}")
                # Read the file line by line to find the problematic line
                f.seek(0)
                for line_number, line in enumerate(f, start=1):
                    try:
                        line.decode(encoding)
                    except UnicodeDecodeError:
                        print(f"Problematic line {line_number}: {line}")
                        break
                break

            position += chunk_size


base_dir = os.path.abspath(os.path.dirname(__file__))
csv_file_path = os.path.join(base_dir, "static", "csv", "People.csv")
find_problematic_line(csv_file_path)
