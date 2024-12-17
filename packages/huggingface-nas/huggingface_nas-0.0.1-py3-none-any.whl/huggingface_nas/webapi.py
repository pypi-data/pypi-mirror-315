import os
import logging

import requests
from tqdm.auto import tqdm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SynologyWebAPI:
    def __init__(self, url, username, password):
        self.url = url.rstrip("/")
        self.username = username
        self.password = password
        self.sid = None

    def login(self):
        """
        WebAPI를 이용해서 나스에 로그인을 진행합니다.
        """
        url = f"{self.url}/webapi/auth.cgi"
        params = {
            "api": "SYNO.API.Auth",
            "version": "6",
            "method": "login",
            "account": self.username,
            "passwd": self.password,
            "session": "FileStation",
            "format": "cookie"
        }
        res = requests.get(url, params=params)
        json_data = res.json()
        if json_data["success"]:
            self.sid = json_data["data"]["sid"]
            logger.info("로그인 성공")
        else:
            raise Exception("로그인 실패", json_data)

    def logout(self):
        """
        연결된 세션을 WebAPI를 이용해서 로그아웃을 진행합니다.
        """
        url = f"{self.url}/webapi/auth.cgi"
        params = {
            "api": "SYNO.API.Auth",
            "version": "6",
            "method": "logout",
            "session": "FileStation"
        }
        res = requests.get(url, params=params)
        json_data = res.json()
        if json_data["success"]:
            logger.info("로그아웃 성공.")
        else:
            raise Exception("로그아웃 실패:", json_data)

    def list_folder(self, folder_path):
        """
        {folder_path}에 있는 폴더 목록들을 가져옵니다.
        """
        url = f"{self.url}/webapi/entry.cgi"
        params = {
            "api": "SYNO.FileStation.List",
            "version": "2",
            "method": "list",
            "folder_path": folder_path,
            "additional": "size"
        }
        cookies = {"id": self.sid}
        res = requests.get(url, params=params, cookies=cookies)
        json_data = res.json()
        if json_data["success"]:
            return json_data["data"]["files"]
        else:
            raise Exception("폴더 목록 가져오기 실패:", json_data)

    def download_file(self, file_path, save_path):
        """
        {file_path} 파일을 {save_path}에 다운로드합니다.
        """
        url = f"{self.url}/webapi/entry.cgi"
        params = {
            "api": "SYNO.FileStation.Download",
            "version": "2",
            "method": "download",
            "path": file_path,
            "mode": "open"
        }
        cookies = {"id": self.sid}

        with requests.get(url, params=params, cookies=cookies, stream=True) as res:
            if res.status_code == 200:
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                with open(save_path, "wb") as f:
                    for chunk in tqdm(res.iter_content(chunk_size=8192), desc=os.path.basename(file_path)):
                        f.write(chunk)
                logger.info(f"다운로드 완료: {save_path}")
            else:
                raise Exception("파일 다운로드 실패:", res.status_code)

    def download_folder(self, folder_path, save_base_path):
        """
        {folder_path}에 있는 폴더와 파일들을 {save_base_path}에 다운합니다.
        """
        folders = self.list_folder(folder_path)
        for folder in folders:
            remote_path = folder["path"]
            local_path = os.path.join(save_base_path, folder["name"])
            if folder["isdir"]:
                logger.info(f"폴더 탐색 중: {remote_path}")
                self.download_folder(remote_path, local_path)
            else:
                logger.info(f"파일 다운로드 중: {remote_path}")
                self.download_file(remote_path, local_path)

    def upload_folder(self, local_folder_path, remote_folder, overwrite=False, timeout: int = 21600):
        """
        {local_folder_path}에 있는 폴더와 파일들을 {remote_folder}에 업로드 합니다.
        """
        url = f"{self.url}/webapi/entry.cgi"

        total_files = 0
        for root, dirs, files in os.walk(local_folder_path):
            total_files += len(files)

        logger.info(f"Found {total_files} files")
        pbar = tqdm(range(total_files), total=total_files, desc="Uploading")

        for root, dirs, files in os.walk(local_folder_path):
            for file_name in files:
                local_file_path = os.path.join(root, file_name)
                remote_file_path = os.path.join(remote_folder, os.path.relpath(local_file_path, local_folder_path))
                remote_file_path = os.path.dirname(remote_file_path)

                upload_data = {
                    "api": "SYNO.FileStation.Upload",
                    "version": "2",
                    "method": "upload",
                    "path": remote_file_path,
                    "create_parents": "true",  # 경로가 없으면 생성
                    "overwrite": "true" if overwrite else "false",  # 덮어쓰기 여부
                }
                upload_params = {
                    "_sid": self.sid
                }

                res = requests.post(
                    url, 
                    params=upload_params, 
                    data=upload_data, 
                    files={'file': (open(local_file_path, 'rb'))}, 
                    verify=False,
                    timeout=timeout,
                )

                if res.status_code == 200 and res.json().get("success"):
                    logger.info(f"\rUploaded: {local_file_path} to {remote_file_path}         \n", end='', flush=True)
                else:
                    logger.info(f"Failed to upload: {local_file_path}")

                pbar.update(1)
