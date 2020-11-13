import requests
from bs4 import BeautifulSoup

url = "https://comic.naver.com/webtoon/list.nhn?titleId=675554"
res = requests.get(url)
res.raise_for_status()

soup = BeautifulSoup(res.text, "lxml")

# cartoons=soup.find_all("td", attrs={"class":"title"})
# title = cartoons[0].a.get_text()
# link=cartoons[0].a["href"]
# print(title)
# print("http://comic.naver.com"+link)

# 만화 제목 + 링크 구하기
# for cartoon in cartoons:
#     title = cartoon.a.get_text()
#     link="http://comic.naver.com"+cartoon.a["href"]
#     print(title, link)

# 평점 구하기
total_rates = 0
cartoons = soup.find_all("div", attrs={"class": "rating_type"})
for cartoon in cartoons:
    rate = cartoon.find("strong").get_text()
    print(rate)
    total_rates += float(rate)

print("전체 점수: ", total_rates)
print("평균 점수: ", total_rates/len(cartoons))

# 혼자하기 -> 등록일 구하기
cartoons_date = soup.find_all("td", attrs={"class": "num"})
for cartoon in cartoons_date:
    date = cartoon.get_text()
    print(date)
