from datetime import datetime
import csv
import os 
import subprocess
import pandas as pd
from glob import glob

class CSVHandler:
    def __init__(self, dir_path):
        self.dir_path = dir_path

    def get_metadata(self, file_path):
        file_path = os.path.join(self.dir_path, file_path)

        #read a sample
        with open(file_path, errors='ignore') as f:
            sample = f.read(1024)

        stats = os.stat(file_path)

        sniffer = csv.Sniffer()
        delimiter = sniffer.sniff(sample).delimiter
        has_header = sniffer.has_header(sample)

        wc_result = subprocess.run(['wc', '-l', file_path], capture_output=True, text=True)
        n_rows = int(wc_result.stdout.strip().split()[0]) - int(has_header)
        
        first_line = open(file_path).readline()
        n_cols = first_line.count(delimiter) + 1

        uri = f"csv://file/{file_path}/"

        created_time = datetime.fromtimestamp(stats.st_ctime).isoformat()
        modified_time = datetime.fromtimestamp(stats.st_mtime).isoformat()

        return {
            "filename": os.path.basename(file_path),
            "file_size_bytes": stats.st_size,
            "uri": uri,
            "delimiter": delimiter,
            "has_header": has_header,
            "num_rows": n_rows,
            "num_cols": n_cols,
            "created_time": created_time,
            "modified_time": modified_time
        }
        

    def list_dir(self):
        files = glob(
            os.path.join(self.dir_path, "*.csv")
        )
        return files

    def get_schema(self, file_path):
        file_path = os.path.join(self.dir_path, file_path)
        df_sample = pd.read_csv(file_path, nrows=10)
    
        schema = df_sample.dtypes.apply(lambda x: x.name).to_dict()
        
        return {
            "columns": list(df_sample.columns),
            "dtypes": schema,
            "row_count_sample": len(df_sample)
        }

    def get_preview(self, file_path):
        file_path = os.path.join(self.dir_path, file_path)
        df_sample = pd.read_csv(file_path, nrows=20)
    
        return df_sample.to_dict()