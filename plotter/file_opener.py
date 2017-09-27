import os
import datetime

# Parses: "Wed Sep 27 07:46:35 EET 2017"
_date_parse_expression = "%a %b %d %I:%M:%S EET %Y"


def get_log_files_with_date(log_dir, extension):
    files = os.listdir(log_dir)
    files = [x for x in files if x.endswith(extension)]
    return extract_date_info(files, log_dir)


def extract_date_info(files, parent_dir):
    result = {}
    for file_name in files:
        date = file_name.split('-')[0]
        date = datetime.datetime.strptime(date, "%a %b %d %I:%M:%S EET %Y")
        result[date] = os.path.join(parent_dir, file_name)

    return result


