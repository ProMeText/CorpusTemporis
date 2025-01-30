

import os
from pathlib import Path


def find_last_version(version_paths):
    return  max(version_paths, key=lambda x: os.path.getctime(x))

   
def get_version_name(version_path):
    filename = version_path.name
    #print(filename.replace('.csv', '').split('-')[1].split('.'))
    return filename.replace('.csv', '').split('-')[1].split('.')

def get_last_version(version_folder_path):
    version_paths = [vp for vp in version_folder_path.iterdir() if not vp.name.endswith('#')]
    if len(version_paths) == 0:
        return 0, 0, 0
    else:
        last_version_path = find_last_version(version_paths)
        major_str, minor_str, patch_str = get_version_name(last_version_path)
        return int(major_str), int(minor_str), int(patch_str)

import pandas as pd

def save(data_path:Path, versions_folder:Path, new_minor:bool=False):
    df = pd.read_csv(data_path)
    last_major, last_minor, last_patch = get_last_version(versions_folder)
    major = last_major
    minor = last_minor
    patch = last_patch + 1
    if new_minor:
        minor += 1
        patch = 0
    df.to_csv(versions_folder / f'data-{major}.{minor}.{patch}.csv', index=False)
