#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: libra.py
Author: AleNriG
Email: agorokhov94@gmail.com
Github: https://github.com/alenrig
Description: Program for editing epub format books.
"""
import re
import sys
import zipfile

from bs4 import BeautifulSoup

METADATA = ["title", "creator"]


def _check_arguments_number():
    if len(sys.argv) != 2:
        print("You should specify one and only one file.")
        sys.exit(1)


def _unzip_archive():
    """TODO: Docstring for _unzip_file.
    :returns: TODO

    """
    try:
        archive = zipfile.ZipFile(sys.argv[1])
        return archive
    except Exception as ex:
        print(f"Error while uncompressing {sys.argv[1]}: {ex}")
        sys.exit(1)


def _find_content_file(archive) -> bytes:
    """TODO: Docstring for _find_metafile.

    :archive: class: TODO
    :returns: TODO

    """
    try:
        meta_container = archive.read("META-INF/container.xml")
    except KeyError as ex:
        print(f"Bad EPUB: {ex}")
        sys.exit(1)
    soup = BeautifulSoup(meta_container, features="lxml")
    content_file_path = soup.find("rootfile").get("full-path")
    content_file = archive.read(content_file_path)
    return content_file


def _get_metadata(epub_content: bytes) -> dict:
    """TODO: Docstring for archive.

    :epub_content: TODO
    :returns: TODO

    """
    soup = BeautifulSoup(epub_content, features="lxml")
    metadata = {meta: soup.find(re.compile(meta + "$")).getText() for meta in METADATA}
    sequence = soup.find("meta", attrs={"name": re.compile("sequence$")})
    if sequence:
        sequence, number = _sequence_parser(sequence.get("content"))
        metadata["sequence"] = sequence
        metadata["number in sequence"] = number
    return metadata


def _sequence_parser(sequence: str) -> str:
    """TODO: Docstring for _sequence_parser.

    :sequence: str: with this template - 'sequence_name; number=...'
    :returns: TODO

    """
    number = sequence.split("=")[-1]
    sequence = sequence.split(";")[0]
    return sequence, number


if __name__ == "__main__":
    _check_arguments_number()
    archive = _unzip_archive()
    content_file = _find_content_file(archive)
    metadata = _get_metadata(content_file)
    for key, value in metadata.items():
        print(f"{key} - {value}")
