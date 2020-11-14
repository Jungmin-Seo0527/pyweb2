import requests
from bs4 import BeautifulSoup

# google movie list
url = "https://play.google.com/store/movies/top"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
    "Accept-Language": "ko-KR, ko"
}  # user agent로 한국에서 접속함을 알려주고, 한국어로 정보를 받도록 함

res = requests.get(url, headers=headers)
res.raise_for_status()
soup = BeautifulSoup(res.text, "lxml")

movies = soup.find_all("div", attrs={"class": "ImZGtf mpg5gc"})
print(len(movies))  # 0이라고 뜸 (같은 class명이 분명 많이 있는데...)
# -> user agnet 를 사용하지 않아 디폴트로 미국에서 접속한 것으로 됨

# with open("movie.html", "w", encoding="utf-8") as f:
#     # f.write(res.text)
#     f.write(soup.prettify())  # html 문서를 예쁘게 출력
# 동적 페이징을 고려하지 않아 처음 나오는 10개의 영화 목록만 보여준다
# 실제 구글 무비 사이트에서 처음 10개의 보여주고 스크롤을 내리면 로딩후 다음 무비 리스트 들을 보여주는 형식으로 되어 있다.
# selenium을 이용해서 스크롤을 내리면서 스크랩을 함

for movie in movies:
    title=movie.find("div", attrs={"class":"WsMG1c nnK0zc"}).get_text()
    print(title)