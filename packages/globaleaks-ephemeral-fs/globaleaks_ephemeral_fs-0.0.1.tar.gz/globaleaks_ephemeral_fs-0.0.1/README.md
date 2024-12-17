# globaleaks-ephemeral-fs
An ephemeral ChaCha20-encrypted filesystem implementation using fusepy and cryptography suitable for privacy-sensitive applications, such as whistleblowing platforms.

[![build workflow](https://github.com/globaleaks/globaleaks-ephemeral-fs/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/globaleaks/globaleaks-whistleblowing-ephemeral-fs/actions/workflows/test.yml?query=branch%3Amain) [![Codacy Badge](https://app.codacy.com/project/badge/Grade/a2baab179e2141648621eeed4665fdeb)](https://app.codacy.com/gh/globaleaks/globaleaks-ephemeral-fs/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade) [![Codacy Badge](https://app.codacy.com/project/badge/Coverage/a2baab179e2141648621eeed4665fdeb)](https://app.codacy.com/gh/globaleaks/globaleaks-ephemeral-fs/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_coverage) [![PyPI - Downloads](https://img.shields.io/pypi/dm/globaleaks-ephemeral-fs)](https://pypi.org/project/globaleaks-ephemeral-fs/)

## Overview
`globaleaks-ephemeral-fs` provides an ephemeral, ChaCha20-encrypted filesystem implementation using Python, FUSE, and Cryptography. This filesystem is designed for temporary, secure storage with strong encryption, making it ideal for privacy-sensitive applications like whistleblowing platforms.

## Installation

To install the package, use `pip`:

```bash
pip install globaleaks-ephemeral-fs
```

## Usage

### Command-Line Interface (CLI)

To mount the filesystem from the command line:

```bash
globaleaks-ephemeral-fs <mountpoint> [--storage_directory <directory>]
```

- `<mountpoint>`: The path where the filesystem will be mounted.
- `--storage_directory` (optional): The directory used for storage. If not provided, a temporary directory will be used.

### Python API

You can also use `globaleaks-ephemeral-fs` within your Python code. Here's an example:

```python
import argparse
from globaleaks_ephemeral_fs.ephemeral_fs import EphemeralFS

def main():
    parser = argparse.ArgumentParser(description="Globaleaks Ephemeral FS")
    parser.add_argument('mount_point', help="Path to mount the filesystem")
    parser.add_argument('--storage_directory', '-s', help="Optional storage directory. Defaults to a temporary directory.")
    args = parser.parse_args()

    # Mount the filesystem with the provided arguments
    EphemeralFS(args.mount_point, args.storage_directory, nothreads=True, foreground=True)

if __name__ == '__main__':
    main()
```

### Arguments

- `mount_point` (required): The directory where the encrypted filesystem will be mounted.
- `--storage_directory` (optional): Specify a custom storage directory for the filesystem. If not provided, a temporary directory will be used.

## Features

- **ChaCha20 Encryption**: All data stored in the filesystem is encrypted with ChaCha20.
- **FUSE Integration**: Mount the filesystem as a virtual disk using FUSE.
- **Temporary Storage**: The filesystem is ephemeral and can use a temporary directory for storage.

## Requirements

- Python 3.7+
- `fusepy` for FUSE support
- `cryptography` for encryption

## License

This project is licensed under the AGPLv3 License - see the [LICENSE](LICENSE) file for details.
