from urllib.parse import urlparse, parse_qs, urlencode
from http.cookies import SimpleCookie
import json

URL = "https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState=%7B%22usersSearchTerm%22%3A%22Miami%2C%20FL%22%2C%22mapBounds%22%3A%7B%22west%22%3A-80.51077731640623%2C%22east%22%3A-80.08780368359373%2C%22south%22%3A25.574566908910292%2C%22north%22%3A25.877672883428932%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A12700%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Afalse%2C%22filterState%22%3A%7B%22sortSelection%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C%22isAllHomes%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A11%7D&wants={%22cat1%22:[%22listResults%22],%22cat2%22:[%22total%22]}&requestId=1"


def cookie_parser():

    cookie_string = 'zguid=23|%24da15a053-8b8c-4228-9de7-d1158798f9f3; zgsession=1|051b5ceb-9ed8-458d-b8c6-6fb732be317f; zjs_user_id=null; _ga=GA1.2.1880371045.1623624510; _gid=GA1.2.1798703518.1623624510; zjs_anonymous_id=%22da15a053-8b8c-4228-9de7-d1158798f9f3%22; _gcl_au=1.1.416537519.1623624511; KruxPixel=true; DoubleClickSession=true; _pxvid=7a7e9167-cc99-11eb-bc65-0242ac12000a; __pdst=e9c55689ac704d27b00ee66b0914e0b8; _fbp=fb.1.1623624517339.553771425; _pin_unauth=dWlkPVpHTTNaR014TkdNdFpUa3dNeTAwT1dZMUxXRmlPRFl0TWpBNE1UWTBZVE00TmpabA; KruxAddition=true; g_state={"i_p":1623749094346,"i_l":2}; utag_main=v_id:017a078ffe730092c8e865a2dd3003072001706a0086e$_sn:2$_se:1$_ss:1$_st:1623669605342$dc_visit:1$ses_id:1623667805342%3Bexp-session$_pn:1%3Bexp-session; JSESSIONID=3737F893266D7CD9A1416811326F686A; _px3=7f4a8b3befd1d776a33015c159a5836f181d8c9a26a83d99b673fa6c06b25a48:uMu4GvZYq7nTrXyEFxpqAL6iUTRdfv0gF+pX2TwYF2s1JYwWS/KRWfwUlLvEB4cm13VcN33ODrLyWSwUFyz2CA==:1000:07Tp1PIqelEUonmMR5EXiXZLgNvZZqS6vNnMolWVMQMzFv8LVTpu1Qlt+CS6Jr0qNePYY37swMaUcLeZ3MD2ykE+ZrAQX1wa91WFmuHtFtmZcaeW2og003R08C4aJ2tf9IcGi6Ba8K3DSc46aULVE/KinkHg8VZllgceJwgS38rtbY5JpDbbWwux9VQjh0UPLbmG7FOFuEstVmxSg5uKdg==; _uetsid=7a548b40cc9911ebbe3e85689067764d; _uetvid=7a54dad0cc9911eb9ee7eb6c9ac9c733; __gads=ID=ddef253a7c7a0f19:T=1623676171:S=ALNI_MYgLk_vZKA6Wd0B5LG_CDvq_GHKeA; _gat=1; AWSALB=F6DsAhrOeBCI0xnQwhUUsjuH9g0jDTBoQb12Q6clji99mX5ks0YDYG7JFXwRiu5d5AyLmuCH1ufHW96z9g4wCd9GfBCymJ6SViwydLHSMqOy4ntzLJjt38cp4qxs; AWSALBCORS=F6DsAhrOeBCI0xnQwhUUsjuH9g0jDTBoQb12Q6clji99mX5ks0YDYG7JFXwRiu5d5AyLmuCH1ufHW96z9g4wCd9GfBCymJ6SViwydLHSMqOy4ntzLJjt38cp4qxs; search=6|1626270514606%7Crect%3D25.877672883428932%252C-80.08780368359373%252C25.574566908910292%252C-80.51077731640623%26rid%3D12700%26disp%3Dmap%26mdm%3Dauto%26p%3D2%26z%3D1%26pt%3Dpmf%252Cpf%26fs%3D1%26fr%3D0%26mmm%3D1%26rs%3D0%26ah%3D0%26singlestory%3D0%26housing-connector%3D0%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%26zillow-owned%3D0%263dhome%3D0%26featuredMultiFamilyBuilding%3D0%09%0912700%09%09%09%09%09%09'
    cookie = SimpleCookie()
    cookie.load(rawdata=cookie_string)

    cookies = {}
    for key, morsel in cookie.items():
        cookies[key] = morsel.value

    return cookies


def url_parser(link, page_number):

    parsed_url = urlparse(url=link)
    query_string = parse_qs(qs=parsed_url.query)
    query_string["requestId"] = [page_number]

    search_query = json.loads(query_string.get("searchQueryState")[0])
    search_query["pagination"] = {
        "currentPage": page_number
    }

    query_string.get("searchQueryState")[0] = search_query
    encoded_qs = urlencode(query=query_string, doseq=1)
    new_url = f"https://www.zillow.com/search/GetSearchPageState.htm?{encoded_qs}"

    return new_url
