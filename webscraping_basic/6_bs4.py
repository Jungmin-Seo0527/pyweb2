import requests
from bs4 import BeautifulSoup

url = "https://comic.naver.com/webtoon/weekday.nhn"
res = requests.get(url)
res.raise_for_status()

soup = BeautifulSoup(res.text, "lxml")
# print(soup.title)
# print(soup.title.get_text())
# print(soup.a) # soup 객체에서 처음 발견되는 a element 출력
# print(soup.a.attrs) # a element 의 속성 정보를 출력
# print(soup.a["href"]) # a element 의 href 속성 '값' 정보를 출력

# print(soup.find("a", attrs={"class":"Nbtn_upload"})) # class="Nbtn_upload"인 a element를 찾아줘
# print(soup.find(attrs={"class":"Nbtn_upload"})) # class="Nbtn_upload"인 어떤 element를 찾아줘
rank1 = soup.find("li", attrs={"class": "rank01"})
# print(rank1.a.get_text())
# rank2 = rank1.next_sibling.next_sibling # 개행으로 인해 2번씩 다음으로 감
# rank3 = rank2.next_sibling.next_sibling
# print(rank3.a.get_text())
# rank2=rank3.previous_sibling.previous_sibling # 이전
# print(rank2.a.get_text())

# rank2=rank1.find_next_sibling("li") # 개행을 고려 하지 않아도 됨
# print(rank2.a.get_text())
# rank3=rank2.find_next_sibling("li")
# print(rank3.a.get_text())

# rank1.find_next_siblings("li") # 모든 형제들을 가져온다

webtoon=soup.find("a", text="연애혁명-325. 할로우드 (Hollow wood) (1)")
print(webtoon)
