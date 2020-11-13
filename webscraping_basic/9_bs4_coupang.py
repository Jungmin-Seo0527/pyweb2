import requests
import re
from bs4 import BeautifulSoup

url = "https://www.coupang.com/np/search?component=&q=%EB%85%B8%ED%8A%B8%EB%B6%81&channel=user"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36"}
res = requests.get(url, headers=headers)
res.raise_for_status()
soup = BeautifulSoup(res.text, "lxml")

# search-product 로 시작하는 모든 attrs를 가저온다
items = soup.find_all("li", attrs={"class": re.compile("^search-product")})
print(items[0].find("div", attrs={"class": "name"}).get_text())

# 여기까지 했을 때 나는 잘 되었지만 안되는 경우도 있는듯... (서버에서 거부??)
# 그때 해결방법...
# headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36"}
# res=requests.get(url, headers=headers)

# 처음 시도했을때는 정상적으로 제품의 이름이 출력되었으나 두번째
# 실행부터 안됨... header를 항상 추가하는것이 좋을 듯 하다
# User-Agent은 구글에 user agent string 검색후 WahtIsMyBrowser.com에 들가면 있음

for item in items:

    # 광고 제품은 제외
    ad_bedge = item.find("span", attrs={"class": "ad-badge-text"})
    if ad_bedge:
        print(" < 광고 상품 제외 >")
        continue

    name = item.find("div", attrs={"class": "name"}).get_text()

    #애플 제품 제외
    if "Apple" in name:
        print(" <Apple 상품 제외 >")
        continue

    price = item.find("strong", attrs={"class": "price-value"}).get_text()

    # 리뷰 100개 이상, 평점 4.5 이상 되는 것만 조회
    rate = item.find("em", attrs={"class": "rating"})
    if rate:
        rate = rate.get_text()
    else:
        print(" < 평점 없는 상품 제외 >")
        continue

    rate_cnt = item.find(
        "span", attrs={"class": "rating-total-count"})

    if rate_cnt:
        rate_cnt = rate_cnt.get_text()  # (34) -> 괄호 존재
        rate_cnt = rate_cnt[1:-1]  # 괄호 제거
    else:
        print(" < 평점 수 없는 상품 제외 >")
        continue

    if float(rate) >= 4.5 and int(rate_cnt) >= 100:
        print(name, price, rate, rate_cnt)
