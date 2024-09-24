import requests
from requests.packages.urllib3 import ssl

BASIC_PARAMS ={
        "MobileOS": "ETC",
        "MobileApp": "AppTest",
        "_type": "json",
        "serviceKey": "0JqgNdKPO9DWmAJhDNQSvhdt198m8i8rHC6T8TyzGsSr3tXfT/AELcsEBwdF9oaeSKAl4vQ1z1ZxMSK8P35OTw=="
    }
HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "User-Agent",
    # "cookie": "NCPVPCLB=53dc2963a8054bd57870a8b2355dc148919c5a02851f15d4ffafa945a766b4a1"
}
BASE_URL = "https://apis.data.go.kr/B551011/KorService1"
# ctx = ssl.create_default_context()
# ctx.set_ciphers('DEFAULT:!TLSv1.1')

class TLSAdapter(requests.adapters.HTTPAdapter):

    def init_poolmanager(self, *args, **kwargs):
        ctx = ssl.create_default_context()
        ctx.set_ciphers('DEFAULT@SECLEVEL=1')
        kwargs['ssl_context'] = ctx
        return super(TLSAdapter, self).init_poolmanager(*args, **kwargs)


def fetch_all_area_code():
    path = "/areaCode1"
    params = {
        "MobileOS": "ETC",
        "MobileApp": "AppTest",
        "_type": "json",
        "serviceKey": "0JqgNdKPO9DWmAJhDNQSvhdt198m8i8rHC6T8TyzGsSr3tXfT/AELcsEBwdF9oaeSKAl4vQ1z1ZxMSK8P35OTw=="
    }
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "User-Agent",
        "cookie": "NCPVPCLB=53dc2963a8054bd57870a8b2355dc148919c5a02851f15d4ffafa945a766b4a1"
    }
    url = BASE_URL + path
    session = requests.session()
    session.mount('https://', TLSAdapter())
    res = session.get(url, params=params)
    return res.json()["response"]["body"]["items"]["item"]

def fetch_area_by_location(map_x: float, map_y: float, redius: int, **kwargs):
    params = {
        "mapX": map_x,
        "mapY": map_y,
        "radius": redius,
        "numOfRows": 100,
        **kwargs,
        **BASIC_PARAMS
    }
    path = "/locationBasedList1"
    url = BASE_URL + path
    session = requests.session()
    session.mount('https://', TLSAdapter())
    res = session.get(url, params=params)
    return res.json()["response"]["body"]["items"]["item"]
    
