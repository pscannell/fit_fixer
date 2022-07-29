from subprocess import run as sp_run
import tempfile
from pathlib import Path
import csv
import argparse

fitCSVTool = str(Path(__file__).parent / 'bin/FitCSVTool.jar')
out_path = Path(__file__).parent / 'out/'

class FitFixer:
    def __init__(self, fit_file_path):
        self.fit_file_path = fit_file_path
        self.csv_file_dest = str(out_path / Path(self.fit_file_path).stem) + '_update.csv'
        self.fit_file_dest = str(out_path / Path(self.fit_file_path).stem) + '_update.fit'
        self.temp_csv_path = tempfile.NamedTemporaryFile(suffix='.csv', prefix=str(Path(__file__)))

    def _fit_to_csv(self):
        fit_to_csv_cmd = [
            'java',
            '-jar',
            fitCSVTool,
            '-b',
            self.fit_file_path,
            self.temp_csv_path.name
        ]
    
        status = sp_run(fit_to_csv_cmd)

        return status

    def _csv_to_fit(self):
        fit_to_csv_cmd = [
            'java',
            '-jar',
            fitCSVTool,
            '-c',
            self.csv_file_dest,
            self.fit_file_dest
        ]
        
        status = sp_run(fit_to_csv_cmd)

        return status
    
    def _clean_timestamp(self):
        with open(self.temp_csv_path.name, 'r') as f:
            with open(self.csv_file_dest, 'w')  as w:
                csv_f = csv.reader(f)
                writer = csv.writer(w)
                for i, row in enumerate(csv_f):
                    if i!=7:
                        writer.writerow(row)
    
    def run_fixer(self):
        self._fit_to_csv()
        self._clean_timestamp()
        self._csv_to_fit()

        return self.fit_file_dest

def parse_args():
    parser = argparse.ArgumentParser(description='Fix FIT file for Strava.')
    parser.add_argument(
        '--fit_file', 
        '-f', 
        type=str,
        help='Path to FIT file.',
        required=True)

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    fit_file = str(Path(__file__).parent / args.fit_file)
    fitFixer = FitFixer(fit_file)
    fitFixer.run_fixer()
    del fitFixer
