import pytest
import shutil
from pathlib import WindowsPath
from ibases import IBases

# @pytest.fixture(scope=)


def test_open_file_right_path():
    test_path = WindowsPath('./ibases.v8i')
    if not test_path.exists():
        shutil.copy(IBases.DEFAULT_PATH, test_path)

    ibases = IBases(test_path)
    assert ibases.list
