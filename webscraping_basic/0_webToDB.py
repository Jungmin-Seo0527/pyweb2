import requests
from bs4 import BeautifulSoup


# #google -> 스크래핑
# url = "https://play.google.com/store/movies/top"
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
#     "Accept-Language": "ko-KR, ko"
# } 
# res = requests.get(url, headers=headers)
# res.raise_for_status()
# soup = BeautifulSoup(res.text, "lxml")

# movies = soup.find_all("div", attrs={"class": "Vpfmgd"})

# # title, price, rate, genre, url
# for movie in movies:
#     title = movie.find("div", attrs={"class": "WsMG1c nnK0zc"}).get_text()
#     genre = movie.find("div", attrs={"class": "KoLSrc"}).get_text()
#     # rate 우선 보류
#     rate=movie.find("div", attrs={"role":"img"})["aria-label"] # 별점 5개 만점에 4.4개를 받았습니다. -> 4.4만 추출...
#     price = movie.find("span", attrs={"class": "VfPpfd ZdBevf i5DZme"}).get_text()
#     link = movie.find("a", attrs={"class": "JC71ub"})["href"]

#     print(f"제목:{title}")
#     print(f"장르:{genre}")
#     print(f"별점:{rate}")
#     print(f"금액 : {price}")
#     print("링크 : ", "http://play.google.com" + link)
#     print("-" * 120)

# naver 스크래핑
for page in range(1, 6):
    url="https://serieson.naver.com/movie/top100List.nhn?page={}&rankingTypeCode=PC_D".format(page)
    res=requests.get(url)
    res.raise_for_status()

    soup=BeautifulSoup(res.text, "lxml")
    movies=soup.find_all("li")
    # tite, price, rate, genre, url
    for movie in movies:
        title=movie.find("a", attrs={"class":"NPI=a:dcontent"})
        if title:
            title=title["title"]
        else:
            continue
        price=movie.find("p", attrs={"class":"price2 v2"}).find("span").get_text()
        rate=movie.find("em", attrs={"class":"score_num"}).get_text()
        
        
