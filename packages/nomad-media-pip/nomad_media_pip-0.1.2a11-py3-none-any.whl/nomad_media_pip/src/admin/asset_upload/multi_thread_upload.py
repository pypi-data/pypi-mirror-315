"""
This module contains the implementation of the multi-threaded upload function.

Functions:
    _multi_thread_upload: Uploads parts of a file in multiple threads.
"""

import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

from nomad_media_pip.src.admin.asset_upload.upload_thread import _upload_thread

def _multi_thread_upload(self, file: str, start_upload_info: dict):
    """
    Upload file parts concurrently.
    Client can control concurrency through their ThreadPoolExecutor configuration.
    """
    parts = start_upload_info["parts"]
    failed_parts = []
    executor = None

    try:
        executor = ThreadPoolExecutor()  # Let client control pool size
        futures = [
            executor.submit(_upload_thread, self, file, part)
            for part in parts
        ]

        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                failed_parts.append(str(e))
                logging.error(f"Part upload failed: {e}")

    except Exception as e:
        logging.error(f"Error during multi-thread upload: {e}")
        raise
    finally:
        if executor:
            executor.shutdown(wait=True)

    if failed_parts:
        raise Exception(f"Upload failed for parts: {', '.join(failed_parts)}")