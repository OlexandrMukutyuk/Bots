import os


def delete_tmp_media(media_ids):
    if not media_ids or not len(media_ids):
        return

    for media_id in media_ids:
        file_path = f"{os.getcwd()}/tmp/{media_id}"

        if os.path.isfile(file_path):
            try:
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
            except OSError as e:
                print(f"Error deleting file {file_path}: {e}")
        else:
            print(f"File not found: {file_path}")
