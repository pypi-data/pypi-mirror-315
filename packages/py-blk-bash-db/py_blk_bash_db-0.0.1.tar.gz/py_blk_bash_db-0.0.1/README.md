# py_blk_hash_db

## Project Overview

`py_blk_hash_db` is a Python library for file chunking, hash computation, and database management. It allows users to split large files into fixed-size chunks and compute SHA-256 hash values for each chunk. These chunks and hash values are stored in a specified database directory for easier file management and recovery.

## Features

- **File Chunking**: Split files into specified size chunks.
- **Hash Computation**: Calculate SHA-256 hash values for each file chunk.
- **Data Storage**: Store file chunks and hash values in a specified database directory.
- **File Recovery**: Recover specified files from the database.

## Installation

```bash
pip install py-blk-hash-db
```

## Usage

### Load Files into the Database

```bash
python3 -m py_blk_bash_db -d database_path -i file_path
```

### Retrieve Files from the Database

```bash
python3 -m py_blk_bash_db -d database_path -s selected_json_filename -o output_file_path
```

### Delete Unused File Chunks

```bash
python3 -m py_blk_bash_db -d database_path -r
```

## Contribution

Contributions are welcome! Please submit Pull Requests on GitHub to contribute code or report issues.

## License

This project is licensed under the GPLv3 license. Please refer to the LICENSE file for details.