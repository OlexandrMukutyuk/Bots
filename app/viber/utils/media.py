import os
from urllib.parse import urlparse, unquote


def delete_tmp_media(media_ids):
    if not media_ids or not len(media_ids):
        return

    for media_id in media_ids:
        file_path = f"{os.getcwd()}/media/{media_id}"

        if os.path.isfile(file_path):
            try:
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
            except OSError as e:
                print(f"Error deleting file {file_path}: {e}")
        else:
            print(f"File not found: {file_path}")


def get_filename_from_url(url):
    parsed_url = urlparse(url)
    filename = unquote(parsed_url.path.split("/")[-1])
    if "?" in filename:
        filename = filename[: filename.index("?")]
    return filename
