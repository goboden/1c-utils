import os
from pathlib import WindowsPath
import re
from pprint import pprint
from typing import Dict


class IBFolder:
    def __init__(self, name: str):
        path = name.split('/')
        self.name = path[-1]
        if len(path) > 2:
            self.parent = IBFolder(path[-2])
        else:
            self.parent = None

    def __repr__(self):
        return self.name or '/'

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return isinstance(other, IBFolder) and self.name == other.name


class IBFolderTree:
    def __init__(self):
        self._folders = []
        self._tree = {}

    def __repr__(self):
        tree_repr = '\n'.join([str(folder) for folder in self._folders])
        return tree_repr

    def find(self, folder: IBFolder):
        pass

    def add(self, folder: IBFolder):
        if folder not in self._folders:
            self._folders.append(folder)
            if folder.parent:
                pass
            else:
                self._tree[folder] = {}


class IBase:
    def __init__(self, name: str, info: Dict):
        self.name = name
        self._all = info
        self.folder = IBFolder(info['Folder'])
        self.id = info['ID']
        self.is_folder = 'Connect' not in info

    def __repr__(self):
        return self.name


class IBases:
    def _get_from_file(self):
        with open(self._path, 'r', encoding='utf-8-sig') as f:
            sections = re.findall(r'\[[^\[]*', f.read())
            for section in sections:
                name, data = re.findall(r'\[(.*)]([\w\W]*)', section)[0]
                result = re.findall(r'(\w*)=(.*)', data)
                ib = IBase(name, {key: value for key, value in result})
                self._info[name] = ib
                self.folders.add(ib.folder)

    def __init__(self, path=None):
        super(IBases, self).__init__()

        if path is None:
            self._path = WindowsPath(os.environ['USERPROFILE']).joinpath('AppData/Roaming/1C/1CEStart/ibases.v8i')
        else:
            self._path = WindowsPath(path)
        if not self._path.exists():
            raise FileNotFoundError(f'ibases path: {self._path}')

        self.folders = IBFolderTree()
        self._info = {}
        self._get_from_file()

    def __getitem__(self, item) -> [IBase, IBFolder, None]:
        if item in self._info:
            return self._info[item]

    def __iter__(self) -> [IBase, IBFolder]:
        for ibase_name in self._info:
            yield self._info[ibase_name]

    def __len__(self):
        return len(self._info)

    @property
    def path(self):
        return self._path

    @property
    def list(self):
        return sorted([key for key in self._info if not self._info[key].is_folder])


if __name__ == '__main__':
    ibases = IBases('./ibases.v8i')
    # ibases = IBases()
    # print(ibases.path)

    # print(ibases._path)
    # pprint(ibases.list)
    # pprint(ibases['УПП (вход по паролю)']._all)
    # pprint(ibases['СЛУЖЕБНЫЕ'])

    # pprint(ibases.folders)

    # for ibase in ibases:
    #     pprint((ibase.folder, ibase.name))

    # ibase = ibases['local_terentev_upp_helix']
    # print(ibase.folder.parent, ibase)

    print(ibases.folders)
