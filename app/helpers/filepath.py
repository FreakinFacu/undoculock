import time

from app.models.files import Files


def gen_file_name(user_id, filename):
    new_name = "/%d/%d.%s" % (user_id, int(time.time()), filename)
    return new_name


def get_display_filename_from_db(file: Files):
    # format for the name is /{user_dir}/{timestamp}.{actual_name}
    path = file.filepath.split("/")[2].split(".")[1]

    return "%s - %s" % (file.type, path)


def get_display_type(file: Files):
    if file.filepath.endswith(".md") or file.filepath.endswith(".doc") or file.filepath.endswith(".txt"):
        return "insert_chart"
    return "image"
