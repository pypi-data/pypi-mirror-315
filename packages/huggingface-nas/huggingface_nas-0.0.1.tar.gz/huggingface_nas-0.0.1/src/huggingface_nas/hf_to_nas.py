import os
import shutil

from datasets import load_dataset


def upload_dataset(
    webapi,
    dataset_name,
    base_folder,
    tmp_folder=".tmp_hf_to_nas",
    cache_tmp_folder=".cache_hf_to_nas",
    token=None
):
    hf_data = load_dataset(dataset_name, token=token, cache_dir=cache_tmp_folder)
    hf_data.save_to_disk(tmp_folder)

    try:
        webapi.login()
        webapi.upload_folder(local_folder_path=tmp_folder, remote_folder=os.path.join(base_folder, dataset_name))
    finally:
        webapi.logout()
        shutil.rmtree(tmp_folder)
        shutil.rmtree(cache_tmp_folder)

