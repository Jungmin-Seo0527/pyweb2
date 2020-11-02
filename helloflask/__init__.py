from flask import Flask, g, Response, make_response, request, session
from datetime import datetime, date

app = Flask(__name__)
app.debug = True

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
        headers = [('Content-Type', 'text/plain'), ('Content-Length', str(len(body)))]
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


@app.route("/")
def helloworld():
    return "Hello Flask World!!!!"
