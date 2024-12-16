# GunfireAPI

A simple Python module to interact with the Gunfire API for uploading files and handling responses. This module allows easy file uploads to the Gunfire API and retrieval of the corresponding URL.

## Installation

You can install the package via pip:

```bash
pip install gunfireapi

## Example usage
```python

from gunfireapi import upload_file

file_path = "path/to/your/file.png"

file_url = upload_file(file_path)

if file_url:
    print("upload success")
    print("uploaded url:", file_url)
else:
    print("upload failed")
