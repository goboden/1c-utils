import pytest
import shutil
from pathlib import WindowsPath
from ibases import IBases

# @pytest.fixture(scope=)

test_path = WindowsPath('./ibases.v8i')
# if not test_path.exists():
#     shutil.copy(IBases.DEFAULT_PATH, test_path)


def test_open_file_right_path():
    IBases(test_path)
    assert True


def test_open_file_wrong_path():
    with pytest.raises(FileNotFoundError):
        IBases(WindowsPath('./f'))


def test_find_folder_by_right_name():
    ibases = IBases(test_path)
    folder = ibases.folders.by_name('')
    assert folder is not None


def test_find_folder_by_wrong_name():
    ibases = IBases(test_path)
    folder = ibases.folders.by_name('folder')
    assert folder is None


def test_find_ibases_in_folder():
    ibases = IBases(test_path)
    test_folder = ibases.folders.by_name('')
    ibases_in_folder = ibases.in_folder(test_folder)
    assert len(ibases_in_folder) != 0


def test_find_ibases_in_folder_recursive():
    ibases = IBases(test_path)
    test_folder = ibases.folders.by_name('')
    ibases_in_folder = ibases.in_folder(test_folder, recursive=True)
    assert len(ibases_in_folder) == len(ibases)
