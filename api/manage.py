"""
Applications command line tools
Example:
DATABASE_URL=postgresql://user:password@host:port/dbname muffin api process_csv_from_file /path/to/file.csv
"""

import os
from api import app, filiaweb

@app.manage.command
def process_csv_from_file(filepath):
    if os.path.exists(filepath):
        file_name = os.path.basename(filepath)
        file_text = open(filepath, 'rb').read()

        persisted_id = filiaweb.persist_csv_data(file_name, file_text.decode('utf-8'))
        process_result = filiaweb.process_csv_data(persisted_id, file_text.decode('utf-8'))

        print(process_result)
    else:
        print("File not found")


