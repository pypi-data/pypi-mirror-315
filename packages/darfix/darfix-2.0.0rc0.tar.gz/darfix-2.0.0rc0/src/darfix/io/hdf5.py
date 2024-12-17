from typing import Union

import os.path
import h5py
from silx.io.url import DataUrl


def is_hdf5(url: Union[DataUrl, str]) -> bool:
    if isinstance(url, DataUrl):
        file_path = url.file_path()
    else:
        try:
            data_url = DataUrl(path=url)
        except Exception:
            file_path = url
        else:
            file_path = data_url.file_path()

    if not file_path or not os.path.exists(file_path):
        raise FileNotFoundError(f"Could not find {file_path}")

    return h5py.is_hdf5(file_path)
