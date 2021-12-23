import os
from pathlib import WindowsPath
import argparse
from ibases import IBases


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', type=str, required=True)
    args = parser.parse_args()
    return args


def clear_cache():
    args = parse_args()

    db_name = args.d

    ibases = IBases()
    ibase = ibases[db_name]
    if ibase:
        print(f'ID={ibase.id}')

        profile_path = WindowsPath(os.environ['USERPROFILE'])
        path1 = profile_path.joinpath('AppData/Local/1C/1cv8').joinpath(ibase.id)
        path2 = profile_path.joinpath('Local Settings/Application Data/1C/1cv8').joinpath(ibase.id)

        if path1.exists():
            print(f' .1. {path1}')
        if path2.exists():
            print(f' .2. {path2}')
    else:
        print(f'IB {db_name} not found in {ibases.path}')


if __name__ == '__main__':
    clear_cache()
