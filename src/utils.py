def get_file_name_from_url(url):
    url_parts = url.split("/")
    return url_parts.pop().split(".")[0]