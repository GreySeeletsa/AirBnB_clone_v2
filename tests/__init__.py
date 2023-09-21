#!/usr/bin/python3
"""tests for AirBnbclone modules"""
import os
from typing import TextIO
from models.engine.file_storage import FileStorage


def clear_stream(stream: TextIO):
    """it will clear contents of given stream"""
    if stream.seekable():
        stream.seek(0)
        stream.truncate(0)


def delete_file(file_path: str):
    """deletes file if it exists"""
    if os.path.isfile(file_path):
        os.unlink(file_path)


def reset_store(store: FileStorage, file_path='file.json'):
    """resets items in given store"""
    with open(file_path, mode='w') as file:
        file.write('{}')
        if store is not None:
            store.reload()


def read_text_file(file_name):
    """reads contents of given file and returns the content inside"""
    lines = []
    if os.path.isfile(file_name):
        with open(file_name, mode='r') as file:
            for line in file.readlines():
                lines.append(line)
    return ''.join(lines)


def write_text_file(file_name, text):
    """writes text to given file
        file_name: name of the file to write to
        text: content of the file
    """
    with open(file_name, mode='w') as file:
        file.write(text)
