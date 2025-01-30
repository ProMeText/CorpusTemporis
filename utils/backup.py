from pathlib import Path
import time

import pandas as pd


def backup(data_path:Path, backup_folder:Path, message:str = 'None'):
    timestamp = time.time()
    df = pd.read_csv(data_path)
    df.to_csv(backup_folder / "data" / f'{timestamp}.csv', index=False)
    Path(backup_folder / "metadata" / f'{timestamp}.txt').write_text(message)
