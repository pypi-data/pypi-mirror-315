import os
import logging
from typing import Optional
from pathlib import Path

from datasets import load_from_disk

from .webapi import SynologyWebAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_dataset_nas(
    path: str,
    cache_dir: str = ".cache/huggingface_nas",
    webapi: Optional[SynologyWebAPI] = None,
    dataset_base_path: Optional[str] = None,
):
    cache_dir = os.path.join(os.getenv("HOME", "./"), cache_dir)
    dataset_path = os.path.join(cache_dir, path)
    if not os.path.exists(dataset_path):
        if webapi is None or dataset_base_path is None:
            raise Exception("")

        logger.info(f"{path}을 다운로드합니다")
        try:
            webapi.login()
            remote_folder = os.path.join(dataset_base_path, path)
            save_base_path = os.path.join(cache_dir, path)
            webapi.download_folder(
                folder_path=remote_folder,
                save_base_path=save_base_path,
            )
        finally:
            webapi.logout()

    return load_from_disk(dataset_path)
