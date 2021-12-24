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

    @property
    def all_children(self) -> List[int]:
        all_children: List[IBFolder] = []

        return all_children

    def add_child(self, child):
        if child not in self.children:
            self.children.append(child)


class IBFolderTree:
    def __init__(self):
        self._folders: List[IBFolder] = []

    def __repr__(self):
        tree_repr = '\n'.join([str(folder) for folder in self._folders])
        return tree_repr

    def __getitem__(self, item) -> IBFolder:
        return self._folders[item]

    def by_name(self, name: str) -> Optional[IBFolder]:
        for folder in self._folders:
            if folder.name == name:
                return folder
        return None

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
                if not ib.is_folder:
                    self._items.append(ib)
                self.folders.add(ib.folder)

    def __init__(self, path=None):
        self._path = WindowsPath(path) if path else IBases.DEFAULT_PATH
        if not self._path.exists():
            raise FileNotFoundError(f'ibases path: {self._path}')

        self._items = []
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

    def in_folder(self, folder: Optional[IBFolder], recursive=False) -> List[IBase]:
        folders = folder.all_children if recursive else [folder]
        return [ibase for ibase in self._items if ibase.folder in folders]


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

    # print([parent for parent in ibases.folders[7].parents])

    test_folder = ibases.folders.by_name('')
    if test_folder:
        for ib in ibases.in_folder(test_folder, recursive=True):
            print(ib)
