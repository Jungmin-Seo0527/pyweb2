from flask import Flask, g, Response, make_response, request, render_template, session, Markup
from datetime import datetime, date
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import sqlite3
from selenium import webdriver
import time

app = Flask(__name__)
app.debug = True

# app.jinja_env.trim_blocks=True

#  subdomain
app.config['SERVER_NAME'] = "local.com:5000"


@app.route("/sd")
def helloworld_local():
    return "Hello Local.com!"


@app.route("/sd", subdomain="g")
def helloworld1():
    return "Hello G.Local.com!!!"


@app.before_request
def before_request():
    print("before_request!!!")
    g.str = "한글"


@app.route("/gg")
def helloworld2():
    return "Hello World!" + getattr(g, 'str', '111')


@app.route('/res1')
def res1():
    custom_res = Response("Custom Response", 201, {'test': 'ttt'})
    return make_response(custom_res)


# WSGI(WebServer Gateway Interface)
@app.route('/test_wsgi')
def wsgi_test():
    def application(environ, start_response):  # environ 환경변수
        # environ : Python dictionary로 HTTP 요청을 처리하는데 필요한 정보가 저장
        # HTTP 요청에 대한 정보는 물론, 운영체제나 WSGI서버의 설정 등도 정의되어 있다.

        # start_response : 일종의 콜백 start_sesponse(status, response_headers, exc_info=None)
        # 실제 서버에서 어플리케이션으로부터 응답(Response)의 상태(Status)와 헤더(Header), 그리고 예외(Exception)의
        # 유무를 확인받아 실행하게 되는데 status와 response_headers는 HTTP응답 명세에 근거하여 작성한다.
        body = 'The request method was %s' % environ['REQUEST_METHOD']
        headers = [('Content-Type', 'text/plain'),
                   ('Content-Length', str(len(body)))]
        start_response('200 OK', headers)
        return [body]

    return make_response(application)


# WSGI
# uwsgi는 일종의 어플리케이션 컨테이너(Application Container)로 동작하게 된다.
# 적재한 어플리케이션을 실행만 시켜주는 역활이라고 할수 있다.
# 이러한 uwsgi에 적재할 어플리케이션(스포카 서버)에는 일종의 규격이 존재하는데 이걸 WSGI라고 한다.
# 정확이는 WSGI에 의해 정의된 어플리케이션을 돌릴수 있게 설게된 컨테이너가 uwsgi라고 봐야 한다.
# WSGI는 파이썬 표준(PEP-333)으로 HTTP를 통해 요청을 받아 응답하는 어플리케이션에 대한 명세로
# 이러한 명세를 만족시키는 클래스나 함수,(__call__을 통해 부를 수 있는)객체를 WSGI어플리케이션이라고 한다.


# Request Event Handler
# @app.before_first_request # 사용자가 서버에 요청을 보낼때 첫번째 요청을 보낼때 함수 실행
# def...

# @app.before_request  # 매번 요청을 부를때 함수 실행(매번 요청을 할때마다 처리할 것들) -> web Filter(db connection)
# def...

# @app.after_request  # 요청을 하 수행한 후에 처리 후 응답이 나오기 직전에 수행(db close)
# def ...(response) return response

# @app.teardown_request # response 후에 처리
# def...(exception)

# @app.teardown_appcontext  # appcontext가 destroy될때
# def...(exception)


# Routing
# @app.route('/text') # defalut method get 지금 실습까지는 일반적으로 사용한것
# def ...

# @app.route('/test', methods=['POST', 'PUT']) # post, put일때만 실행 (get일때는 실행 안됨)
# def...

@app.route('/test/<tid>')  # tid는 일종의 변수가 된다.
def test3(tid):
    return "tid is %s" % tid


# @app.route('/test', defaluts={'page': 'index'}) #입력된 page가 없으면 디폴트
# @app.route('/test/<page>)
# def xxx(page):

# @app.route('/test', host='abc.com')
# @app.route('/test', redirect_to='/new_test')
# redirect a.html -> b.html (blog.naver.com -> blog.naver.com.asdfjas;dfkjaksl...)

# app.config['SERVER_NAME']='locasl.com:5000'

# @app.route("/")
# def helloworld_local():
#   return "Hello Local.com!"

# @app.route("/", subdomain="g")
# def helloworld():
#   return "Hello G.Local.com!!!"


# Request Parameter
# GET
@app.route('/rp')
def rp():
    q = request.args.get('q')
    return "q= %s" % str(q)


# POST
# request.form.get('p', 123) # 123-> default

# GET or POST
# request.values.get('v') # 이게 제일 편함 대신 느림

# Parameters
# request.args.getlist('qs')
@app.route('/rp2')
def rp2():
    q = request.args.getlist('q')
    return "q= %s" % str(q)


# Request Parameter Custom Function Type
# request 처리 용 함수
def ymd(fmt):
    def trans(date_str):
        return datetime.strptime(date_str, fmt)

    return trans


@app.route('/dt')
def dt():
    datestr = request.values.get('date', date.today(), type=ymd('%Y-%m-%d'))
    return "우리나라 시간 형식: " + str(datestr)


# request.environ
@app.route('/reqenv')
def reqenv():
    return ('REQUEST_METHOD: %(REQUEST_METHOD) s <br>'
            'SCRIPT_NAME: %(SCRIPT_NAME) s <br>'
            'PATH_INFO: %(PATH_INFO) s <br>'
            'QUERY_STRING: %(QUERY_STRING) s <br>'
            'SERVER_NAME: %(SERVER_NAME) s <br>'
            'SERVER_PORT: %(SERVER_PORT) s <br>'
            'SERVER_PROTOCOL: %(SERVER_PROTOCOL) s <br>'
            'wsgi.version: %(wsgi.version) s <br>'
            'wsgi.url_scheme: %(wsgi.url_scheme) s <br>'
            'wsgi.input: %(wsgi.input) s <br>'
            'wsgi.errors: %(wsgi.errors) s <br>'
            'wsgi.multithread: %(wsgi.multithread) s <br>'
            'wsgi.multiprocess: %(wsgi.multiprocess) s <br>'
            'wsgi.run_once: %(wsgi.run_once) s') % request.environ


# Cookie
# from flask import Response
# Cookie __init__ Arguments
# key, value, max_age, expires, domian, path

# http://local.com:5000/wc?key=token&val=abc
@app.route('/wc')
def wc():
    key = request.args.get('key')
    val = request.args.get('val')
    res = Response("SET COOKIE")
    res.set_cookie(key, val)
    return make_response(res)


# http://local.com:5000/rc?key=token&val=abc
@app.route('/rc')
def rc():
    key = request.args.get('key')  # token
    val = request.cookies.get(key)
    return "cookie['" + key + "]" + val


# Templates(Jinja)_trim_block
@app.route('/tmpl/')
def t():
    tit = Markup("<strong>Title</Strong>")
    mu = Markup("<h1>iii=<i>%s</i></h1>")
    h = mu % "Italic"
    print("h=", h)
    print(">>>>>", type(tit))
    return render_template('index.html', title=tit, mu=h)


# excape
# quotation excape -> ""
# safe string & striptage
# {{ "<strong>String</string>"|safe}}
# {{ "<string>String</string>" | striptage}}


# Markup

# FOR loop
@app.route("/forLoop/")
def loop():
    lst = [("만남1", "김건모"), ("만남2", "노사연")]
    return render_template('index_loop.html', lst=lst)


# loop object
# for loop속에서 기본으로 제공되는 object : '현재 for loop의 self'
# loop.index : 1부터 시작하는 index값 (cf. loop.index0)
# loop.revindex: n-1내림차순 index값 (cf. loop.revindex0)
# loop.first: boolean(isThisFirstItem), loop의 첫번째인지의 여부
# loop.last: boolean(isThisLastItem), loop의 마지막인지의 여부
# loop.length: size
# loop.depth: loop 깊이
# loop.cycle: 짝, 홀수번째 구분

# for loop Filtering

# for recursion
@app.route("/tmpl2/")
def tmpl2():
    a = (1, "만남1", "김건모", False, [])
    b = (2, "만남2", "노사연", True, [a])
    c = (3, "만남3", "익명", False, [a, b])
    d = (4, "만남4", "익명", False, [a, b, c])
    return render_template("index_loop.html", lst2=[a, b, c, d])


# if condition
# {% if <condition> %}
# {% elseif <other condition> %}
# {% endif %}


# class, recursive for
class Nav:
    def __init__(self, title, url='#', children=[]):
        self.title = title
        self.url = url
        self.children = children


@app.route("/tmpl3/")
def tmpl3():
    py = Nav("파이썬", "http://serch.naver.com")
    java = Nav("자바", "http://search.naver.com")
    t_prg = Nav("프로그래밍 언어", "http://search.naver.com", [py, java])

    jinja = Nav("Jinja", "http://search.naver.com")
    gc = Nav("Genshi, Cheetah", "http://search.naver.com")
    flask = Nav("플라스크", "http://search.naver.com", [jinja, gc])

    spr = Nav("스프링", "http://search.naver.com")
    ndjs = Nav("노드js", "http://search.naver.com")
    t_webf = Nav("웹 프레임워크", "http://search.naver.com", [flask, spr, ndjs])

    my = Nav("나의 일상", "http://search.naver.com")
    issue = Nav("이슈 게시판", "http://search.naver.com")
    t_others = Nav("기타", "http://search.naver.com", [my, issue])

    return render_template("index_loop.html", navs=[t_prg, t_webf, t_others])


# parent's loop


# block (template inheritance)
@app.route("/main/")
def main():
    return render_template('index2.html')


# 네이버 웹툰 만화 리스트 보여주기
@app.route("/bs/")
def bs():
    url = "https://comic.naver.com/webtoon/weekday.nhn"
    res = requests.get(url)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "lxml")

    # 네이버 웹툰 전체 목록 가져오기
    cartoons = soup.find_all("a", attrs={"class": "title"})
    # class 속성이 title인 모든 "a" element 를 반환

    cartoon_list = []
    for cartoon in cartoons:
        cartoon_list.append(cartoon.get_text())

    # create table, insert data
    filepath = "webtoon.db"
    conn = sqlite3.connect(filepath)
    cur = conn.cursor()
    conn.execute('CREATE TABLE IF NOT EXISTS webtoon(name TEXT, no int);')
    conn.commit()
    # sql="INSERT INTO webtoon VALUES (?)"
    # cur.execute(sql, cartoon_list[0])
    who = "tlqkf2"

    cur.execute("insert into webtoon values (?, ?)", (who, 12))
    # cur.executemany("insert into webtoon values (?, ?)", (cartoon_list, no))

    for i in cartoon_list:
        cur.execute("insert into webtoon values(?, ?)", (i, 1))

    conn.commit()
    conn.close()
    return render_template("bsIndex.html", list=cartoon_list)


@app.route("/about/")
def about():
    return "여기는 어바웃입니다"


# google movie list(title, price, rate, genre, url)
# google play 영화 인기차트는 스크롤을 내리기 전에는 그 밑에 있는 정보를 못보는것 주의!!
# chromedriver 필수
# 성공!!!
@app.route("/google_movie/")
def googleMovie():
    # 크롬창의 띄우지 않고 백그라운드로 실행해서 스크롤을 내려 아래에 있는 정보 로딩
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument("window-size=1920x1080")
    browser = webdriver.Chrome(options=options)
    # browser.maximize_window()

    # 페이지 이동
    url = "https://play.google.com/store/movies/top"
    browser.get(url)

    # 스크롤 내리기
    browser.execute_script("window.scrollTo(0, 1080)")
    interval = 2
    prev_height = browser.execute_script("return document.body.scrollHeight")
    while True:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(interval)  # 스크롤 내리고 로딩 시간 임의로 2초로 함
        cur_height = browser.execute_script("return document.body.scrollHeight")
        if cur_height == prev_height:
            break
        prev_height = cur_height
    print("done")
    browser.get_screenshot_as_file("google_movie_test.png")

    # db 만들기
    filepath = "google_movies.db"
    conn = sqlite3.connect(filepath)
    cur = conn.cursor()

    conn.executescript("""drop table if exists google_movies;
    create table google_movies(tite text, genre text, rate text, price text, url text);
    """)

    conn.commit()

    # 스크래핑
    soup = BeautifulSoup(browser.page_source, "lxml")

    movies = soup.find_all("div", attrs={"class": "Vpfmgd"})

    # title, price, rate, genre, url
    for movie in movies:
        title = movie.find("div", attrs={"class": "WsMG1c nnK0zc"}).get_text()
        genre = movie.find("div", attrs={"class": "KoLSrc"})
        # 장르가 표기되지 않은 것이 있음
        if genre:
            genre = genre.get_text()
        else:
            genre = "NULL"
        # rate 우선 보류
        rate = movie.find("div", attrs={"role": "img"})  # 별점 5개 만점에 4.4개를 받았습니다. -> 4.4만 추출...
        if rate:
            rate = rate["aria-label"]
        else:
            rate = "NULL"
        price = movie.find("span", attrs={"class": "VfPpfd ZdBevf i5DZme"}).get_text()
        link = movie.find("a", attrs={"class": "JC71ub"})["href"]

        conn.execute("insert into google_movies values (?, ?, ?, ?, ?)", (title, genre, rate, price, url))

    conn.commit()
    conn.close()
    return "google"


# naver movie list
# google과는 다르게 동적 페이지?(용어를 정확하게 모르겠다. -> 스크롤을 내려야지 로딩이 되면서 다음 정보가 화면에 출력되는 방식...)
# 가 아니고 페이지를 넘기면서 리스트를 스크랩 해야 함
# """drop table if exists naver_movies;
#     create table naver_movies(tite text, genre text, rate text, price text, url text);
#     """
# 문제.. 장르를 보려면 다시 크롤링 작업이 필요할것 같다...
@app.route("/naver_movies/")
def naverMovie():
    for page in range(1, 6):
        url = "https://serieson.naver.com/movie/top100List.nhn?page={}&rankingTypeCode=PC_D".format(page)
        res = requests.get(url)
        res.raise_for_status()

        soup = BeautifulSoup(res.text, "lxml")


@app.route("/")
def helloworld():
    return "Hello Flask World!!!!"
