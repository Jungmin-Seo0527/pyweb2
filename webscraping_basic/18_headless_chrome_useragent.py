from selenium import webdriver

options = webdriver.ChromeOptions()
options.headless = True
options.add_argument("window-size=1920x1080")

# headless chrome 일때 useragent가 headless chrome으로 되는것을 막기 위해...
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    )

browser = webdriver.Chrome(options=options)
browser.maximize_window()

url = "https://www.whatismybrowser.com/detect/what-is-my-user-agent"
browser.get(url)

# Mozilla/5.0 (Windows NT 10.0; Win64; x64)
# AppleWebKit/537.36 (KHTML, like Gecko)
# Chrome/86.0.4240.198 Safari/537.36
detected_value = browser.find_element_by_id("detected_value")
print(detected_value.text)
browser.quit()
# headless chrome 으로 user agent 를 받으러 가면 원래 Chrome인 부분이 HeaadlessChrome으로 됨
# useragnet 에 headlesschrome이면 웹사이트에서 막아 버리는 경우가 있다.

# 걱정 -> 만약 프로그램을 교수님이 돌려보셨을때  user-agent는 당연히 다르기 때문에 에러가 자명함
# 아이디어: HandlessChrome 을 찾아서 Handle을 지워버리는건 어떨까...

