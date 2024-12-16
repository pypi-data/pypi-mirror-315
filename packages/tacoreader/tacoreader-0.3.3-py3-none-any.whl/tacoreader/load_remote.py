import json
import pathlib
from typing import List, Union

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import requests


def remote_file2dataframe(file: str) -> pd.DataFrame:
    """Read the dataframe of a tortilla file given a URL. The
        server must support HTTP Range requests.

    Args:
        files (str): A URL pointing to the tortilla file.
    Returns:
        pd.DataFrame: The dataframe of the tortilla file.
    """
    # Fetch the first 8 bytes of the file
    headers = {"Range": "bytes=0-17"}
    response: requests.Response = requests.get(file, headers=headers)
    static_bytes: bytes = response.content

    # SPLIT the static bytes
    MB: bytes = static_bytes[:2]
    FO: bytes = static_bytes[2:10]
    FL: bytes = static_bytes[10:18]

    # Check if the file is a tortilla or a taco
    if MB not in {b"#y", b"WX"}:
        raise ValueError(
            "Invalid file type: must be either a Tortilla 🫓 or a TACO 🌮"
        )

    # Interpret the bytes as a little-endian integer
    footer_offset: int = int.from_bytes(FO, "little")
    footer_length: int = int.from_bytes(FL, "little")

    # Fetch the footer
    headers = {"Range": f"bytes={footer_offset}-{footer_offset + footer_length - 1}"}
    with requests.get(file, headers=headers) as response:
        # Interpret the response as a parquet table
        dataframe = pq.read_table(pa.BufferReader(response.content)).to_pandas()

    # Add the file format and mode
    dataframe["internal:mode"] = "online"
    dataframe["internal:subfile"] = dataframe.apply(
        lambda row: f"/vsisubfile/{row['tortilla:offset']}_{row['tortilla:length']},/vsicurl/{file}",
        axis=1,
    )
    return dataframe


def remote_files2dataframe(files: List[str]) -> pd.DataFrame:
    """Read the dataframe of tortillas files given a set of URLs. The
        server must support HTTP Range requests.

    Args:
        files (List[str]): A list of URLs pointing to the
            tortilla files.

    Returns:
        pd.DataFrame: The dataframe of the tortilla file.
    """

    container = []
    for file in files:

        # Fetch the first 8 bytes of the file
        headers = {"Range": "bytes=0-17"}
        response: requests.Response = requests.get(file, headers=headers)
        static_bytes: bytes = response.content

        # SPLIT the static bytes
        MB: bytes = static_bytes[:2]
        FO: bytes = static_bytes[2:10]
        FL: bytes = static_bytes[10:18]

        # Check if the file is a tortilla
        if MB not in {b"#y", b"WX"}:
            raise ValueError(
                "Invalid file type: must be either a Tortilla 🫓 or a TACO 🌮"
            )

        # Interpret the bytes as a little-endian integer
        footer_offset: int = int.from_bytes(FO, "little")
        footer_length: int = int.from_bytes(FL, "little")

        # Fetch the footer
        headers = {"Range": f"bytes={footer_offset}-{footer_offset + footer_length - 1}"}
        with requests.get(file, headers=headers) as response:

            # Interpret the response as a parquet table
            dataframe = pq.read_table(pa.BufferReader(response.content)).to_pandas()

        # Add the file format and mode
        dataframe["internal:mode"] = "online"
        dataframe["internal:subfile"] = dataframe.apply(
            lambda row: f"/vsisubfile/{row['tortilla:offset']}_{row['tortilla:length']},/vsicurl/{file}",
            axis=1,
        )
        container.append(dataframe)

    return pd.concat(container, ignore_index=True)


def remote_lazyfile2dataframe(
    offset: int, file: Union[str, pathlib.Path]
) -> pd.DataFrame:
    """Read the dataframe of tortilla file that is a subfile
    of a larger file.

    Args:
        offset (int): The offset of the subfile.
        file (Union[str, pathlib.Path]): A local path pointing to the
            main tortilla file.

    Returns:
        pd.DataFrame: The dataframe of the tortilla file.
    """

    # Fetch the first 8 bytes of the file
    initb, endb = offset, offset + 18
    headers = {"Range": f"bytes={initb}-{endb - 1}"}
    response: requests.Response = requests.get(file, headers=headers)
    static_bytes: bytes = response.content

    # SPLIT the static bytes
    MB: bytes = static_bytes[:2]
    FO: bytes = static_bytes[2:10]
    FL: bytes = static_bytes[10:18]

    # Check if the file is a tortilla
    if MB not in {b"#y", b"WX"}:
        raise ValueError(
            "Invalid file type: must be either a Tortilla 🫓 or a TACO 🌮"
        )

    # Interpret the bytes as a little-endian integer
    footer_offset: int = int.from_bytes(FO, "little") + offset
    footer_length: int = int.from_bytes(FL, "little")

    # Fetch the footer
    headers = {"Range": f"bytes={footer_offset}-{footer_offset + footer_length - 1}"}
    with requests.get(file, headers=headers) as response:
        # Interpret the response as a parquet table
        dataframe = pq.read_table(pa.BufferReader(response.content)).to_pandas()

    # Fix the offset
    dataframe["tortilla:offset"] = dataframe["tortilla:offset"] + offset

    # Add the file format and mode
    dataframe["internal:mode"] = "online"
    dataframe["internal:subfile"] = dataframe.apply(
        lambda row: f"/vsisubfile/{row['tortilla:offset']}_{row['tortilla:length']},/vsicurl/{file}",
        axis=1,
    )

    return dataframe


def remote_file2metadata(file: str) -> dict:
    """Read the metadata of a taco file given a URL. The
        server must support HTTP Range requests.

    Args:
        file (str): A URL pointing to the taco file.

    Returns:
        dict: The metadata of the taco file.
    """
    # Fetch the first 8 bytes of the file
    headers = {"Range": "bytes=0-41"}
    response: requests.Response = requests.get(file, headers=headers)
    static_bytes: bytes = response.content

    # SPLIT the static bytes
    MB: bytes = static_bytes[:2]
    CO: int = int.from_bytes(static_bytes[26:34], "little")
    CL: int = int.from_bytes(static_bytes[34:42], "little")

    # Check if the file is a tortilla
    if MB not in {b"#y", b"WX"}:
        raise ValueError(
            "Invalid file type: must be either a Tortilla 🫓 or a TACO 🌮"
        )

    # Read the Collection (JSON UTF-8 encoded)
    headers = {"Range": f"bytes={CO}-{CO + CL - 1}"}
    collection: dict = json.loads(requests.get(file, headers=headers).content.decode())

    return collection


def remote_files2metadata(files: List[str]) -> dict:
    """Read the metadata of taco files given a set of URLs. The server
        must support HTTP Range requests.

    Args:
        files (List[str]): A list of URLs pointing to the
            taco files.

    Returns:
        dict: The metadata of the taco file.
    """
    return remote_file2metadata(files[0])
