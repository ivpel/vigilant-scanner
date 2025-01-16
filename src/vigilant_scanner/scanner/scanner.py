from pathlib import Path
import os
import hashlib
from .metadata_collector import FileMetadata


class Scanner:
    def __init__(self, directory):
        self.directory = directory

    def _compute_hash(self, file_path):
        """Compute the SHA-256 hash of a file."""
        sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()

    def _collect_metadata(self, file_path):
        """Collect metadata for a single file."""
        stats = file_path.stat()
        hash_value = self._compute_hash(file_path)
        return FileMetadata(
            path=str(file_path),
            generated_hash=hash_value,
            size=stats.st_size,
            permissions=oct(stats.st_mode),
            owner=stats.st_uid,
            modified_time=stats.st_mtime,
        )

    def scan_directory(self):
        """Scan the directory and return metadata for all files."""
        metadata_list = []
        for root, _, files in os.walk(self.directory):
            for file in files:
                full_path = Path(root) / file
                metadata = self._collect_metadata(full_path)
                metadata_list.append(metadata)
        return metadata_list
