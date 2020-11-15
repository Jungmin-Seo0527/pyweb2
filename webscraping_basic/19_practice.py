from selenium import webdriver
import time
import requests
from bs4 import BeautifulSoup

browser=webdriver.Chrome()

# 다음 이동
browser.get("https://www.daum.net/")

browser.find_element_by_id("q").send_keys("송파 헬리오시티")
# browser.find_element_by_class_name("ir_wa").click()
browser.find_element_by_xpath("//*[@id='daumSearch']/fieldset/div/div/button[2]").click()

# 동적 페이지를 크롤링 하여 스크랩할때는
# 항상 로딩 시간을 고려!!!!!!!!
time.sleep(2)
soup=BeautifulSoup(browser.page_source, "lxml")


infos=soup.find("table", attrs={"class":"tbl"}).find("tbody").find_all("tr")
# data_rows=soup.find("table", attrs={"class":"tbl"}).find("tbody").find_all("tr")
for info in infos:
    trading=info.find_all("td")

    print(trading[0].get_text())
    

# url="https://search.daum.net/search?w=tot&DA=YZR&t__nil_searchbox=btn&sug=&sugo=&sq=&o=&q=%EC%86%A1%ED%8C%8C+%ED%97%AC%EB%A6%AC%EC%98%A4%EC%8B%9C%ED%8B%B0"
# res=requests.get(url)
# res.raise_for_status()
# soup=BeautifulSoup(res.text, "lxml")

# data_rows=soup.find("table", attrs={"class":"tbl"}).find("tbody").find_all("tr")
# for index, row in enumerate(data_rows):
#     columns=row.find_all("td")
#     print("========== 매물{} ==========".format(index+1))
#     print("거래: ", columns[0].get_text().strip())
#     print("면적: ", columns[1].get_text().strip(), "(공급/전용)")
#     print("가격: ", columns[2].get_text().strip(), "(만원)")
#     print("동: ", columns[3].get_text().strip())
#     print("층: ", columns[4].get_text().strip())



