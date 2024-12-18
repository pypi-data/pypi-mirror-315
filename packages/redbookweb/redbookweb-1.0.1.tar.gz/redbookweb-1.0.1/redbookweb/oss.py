import os
import concurrent
import oss2
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from redbookweb.exception import DownloadError


class OSSManager:
    def __init__(
        self,
        access_key_id: str,
        access_key_secret: str,
        bucket_name: str,
        endpoint: str = "https://oss-accelerate.aliyuncs.com",
        max_workers: int = 5,
    ):
        # 初始化认证信息
        auth = oss2.Auth(access_key_id, access_key_secret)
        # 创建一个OSS Bucket实例
        self.bucket = oss2.Bucket(auth, endpoint, bucket_name)
        # 设置并发下载的最大线程数
        self.max_workers = max_workers

    def download_key(self, key: str, filename: str):
        try:
            result = self.bucket.get_object_to_file(key, filename)
            if result.resp.status != 200:
                raise DownloadError(
                    f"下载 {key} 时出错，HTTP状态码：{result.resp.status}"
                )
            return filename
        except oss2.exceptions.OssError as e:
            raise DownloadError(f"下载 {key} 时出错: {str(e)}")

    def download_url(self, url: str, file_path: str = ""):
        parsed_url = urlparse(url)
        key = parsed_url.path.lstrip("/")
        filename = os.path.basename(key)
        if file_path != "":
            if not os.path.exists(file_path):
                os.makedirs(file_path, exist_ok=True)
            filename = os.path.join(file_path, filename)
        return self.download_key(key, filename)

    def download_urls(self, urls: list, file_path: str = ""):
        download_func = partial(self.download_url, file_path=file_path)
        with ThreadPoolExecutor(self.max_workers) as executor:
            future_to_url = {executor.submit(download_func, url): url for url in urls}
            filename_list = []
            try:
                for future in concurrent.futures.as_completed(future_to_url):
                    filename = future.result()
                    filename_list.append(filename)
            except DownloadError as e:
                # 出现异常时尝试取消所有其他任务
                for future in future_to_url:
                    future.cancel()
                    raise DownloadError(
                        f"下载过程中出现错误，已尝试取消所有其他下载。错误详情：{str(e)}"
                    )
            return filename_list

    def delete_files(self, filename_list: list):
        for filename in filename_list:
            os.remove(filename)
