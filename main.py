
import argparse
from pathlib import Path

from fit_fix import FitFixer
from strava import Strava

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
    try:
        args = parse_args()
        fit_file = str(Path(__file__).parent / args.fit_file)
        fitFixer = FitFixer(fit_file)
        clean_fit_file = fitFixer.run_fixer()
        del fitFixer

        strava = Strava()
        strava.upload_activity(clean_fit_file)
        del strava
    except Exception as e:
        print(e)
