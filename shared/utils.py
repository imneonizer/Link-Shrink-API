
def build_http_url(url):
    if url.find("http://") != 0 and url.find("https://") != 0:
        url = "http://" + url
    return url