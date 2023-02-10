import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry


def get_session(
    retries: int = 5,
    backoff_factor: float = 1,
    status_forcelist: list = [502, 503, 504],
) -> requests.Session:
    """Returns a requests session that retries on specific failures.
    also: https://stackoverflow.com/a/35636367/2469390
    https://www.coglib.com/~icordasc/blog/2014/12/retries-in-requests.html
    """
    session = requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session
