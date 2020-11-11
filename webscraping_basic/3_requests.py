import requests
#res=requests.get("http://naver.com")
res = requests.get("http://google.com")
print("응답코드: ", res.status_code)  # 200이면 정상

# ok = requests.codes.ok

# if res.status_code == ok:
#     print("정상입니다.")
# else:
#     print("문제가 생겼습니다.[에러코드 ", res.status_code, "]")

res.raise_for_status()  # 200이 아니면 오류

print(len(res.text))
print(res.text)

with open("mygoogle.html", "w", encoding="utf-8") as f:
    f.write(res.text)
