def parse_repo_name_from_url(url: str):
    return url.split("/")[-1].split(".git")[0]