from pathlib import Path

from loguru import logger

from srcmlmal.config import PROCESSED_DATA_DIR

input_path: Path = (PROCESSED_DATA_DIR / "dataset.csv",)
output_path: Path = (PROCESSED_DATA_DIR / "features.csv",)
