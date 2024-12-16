import os
from dataclasses import dataclass
from datetime import datetime
from tempfile import NamedTemporaryFile, gettempdir


@dataclass
class DiskCacheFile:
	path: str
	timestamp: datetime


def cache_data(original_data_hash: str, data: bytes) -> None:
	"""
	Cache data to disk.
	"""

	prefix = f"flask-squeeze-cache_{original_data_hash}"

	with NamedTemporaryFile(prefix=prefix, delete=False) as f:
		f.write(data)


def load_from_cache(original_data_hash: str) -> bytes | None:
	"""
	Load data from disk cache.
	"""

	# Get all files in the temp directory
	files = os.listdir(gettempdir())
	# Filter files that match the key
	files = [f for f in files if f.startswith(f"flask_squeeze_cache_{original_data_hash}")]
	# Get the latest file

	for f in files:
		_, f_hash = f.split("_")
		if f_hash == original_data_hash:
			with open(f, "rb") as f:
				return f.read()

	return None
