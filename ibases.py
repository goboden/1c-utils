import os
from pathlib import WindowsPath
import re
from pprint import pprint
from typing import Dict, List, Union, Optional, Generator


class IBFolder:
    def __init__(self, name: str, child=None):
        path = name.split('/')
        self.name = path[-1]
        self.parent = None if len(path) < 2 else IBFolder('/'.join(path[:-1]))
        self.children: List[IBFolder] = []

    def __repr__(self):
        return self.name or '/'

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return isinstance(other, IBFolder) and self.name == other.name

    @property
    def parents(self):
        parents = []
        parent = self.parent
        while parent is not None:
            parents.append(parent)
            parent = parent.parent
        return parents

    def add_child(self, child):
        if child not in self.children:
            self.children.append(child)


class IBFolderTree:
    def __init__(self):
        self._folders = []

    def __repr__(self):
        tree_repr = '\n'.join([str(folder) for folder in self._folders])
        return tree_repr

    def __getitem__(self, item) -> IBFolder:
        return self._folders[item]

    def find(self, folder: IBFolder):
        pass

    def add(self, folder: IBFolder):
        if folder not in self._folders:
            self._folders.append(folder)
            if folder.parent is not None and folder.parent in self._folders:
                parent_index = self._folders.index(folder.parent)
                parent = self._folders[parent_index]
                parent.add_child(folder)


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
    DEFAULT_PATH = WindowsPath(os.environ['USERPROFILE']).joinpath('AppData/Roaming/1C/1CEStart/ibases.v8i')

    def _read_file(self):
        with open(self._path, 'r', encoding='utf-8-sig') as f:
            sections = re.findall(r'\[[^\[]*', f.read())
            for section in sections:
                name, data = re.findall(r'\[(.*)]([\w\W]*)', section)[0]
                result = re.findall(r'(\w*)=(.*)', data)
                ib = IBase(name, {key: value for key, value in result})
                self._info[name] = ib
                self.list.append(ib)
                self.folders.add(ib.folder)

    def __init__(self, path=None):
        self._path = WindowsPath(path) if path else IBases.DEFAULT_PATH
        if not self._path.exists():
            raise FileNotFoundError(f'ibases path: {self._path}')

        self.list = []
        self.folders = IBFolderTree()
        self._info = {}
        self._read_file()

    def __getitem__(self, item) -> Optional[IBase]:
        if item in self._info:
            return self._info[item]
        return None

    def __iter__(self) -> Generator:
        for ibase_name in self._info:
            yield self._info[ibase_name]

    def __len__(self):
        return len(self._info)

    @property
    def path(self):
        return self._path


if __name__ == '__main__':
    # ibases = IBases('./ibases.v8i')
    ibases = IBases()
    # print(ibases.path)

    # pprint(ibases.list)
    # pprint(ibases['УПП (вход по паролю)'])
    # pprint(ibases['СЛУЖЕБНЫЕ'])

    # pprint(ibases.folders)

    # for ibase in ibases:
    #     pprint((ibase.folder, ibase.name))

    # ibase = ibases['local_terentev_upp_helix']
    # print(ibase.folder.parent, ibase)

    # print(ibases.folders)

    print([parent for parent in ibases.folders[7].parents])
