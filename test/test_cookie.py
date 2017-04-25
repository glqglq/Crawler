import cookielib,os,json,time,urllib2,lxml.html

def load_ff_session(session_filename):
    cj = cookielib.CookieJar()
    if os._exists(session_filename):
        json_data = json.loads(open(session_filename,'rb').read())
        for window in json_data.get('windows',[]):
            for cookie in window.get('cookies',[]):
                c = cookielib.Cookie(0,
                                     cookie.get('name',''),
                                     cookie.get('value',''),
                                     None,False,
                                     cookie.get('host', ''),
                                     cookie.get('host','').startswith('.'),
                                     cookie.get('host','').startswith('.'),
                                     cookie.get('path',''),False,False,
                                     str(int(time.time()) + 3600 * 24 * 7),
                                     False,None,None,{})
                cj.set_cookie(c)
    else:
        print 'Session filename does not exsit:',session_filename
    return cj

if __name__ == '__main__':
    cj = load_ff_session(r'C:\Users\LuckyGong\AppData\Local\Google\Chrome\User Data\Default\Cookies')
    processor = urllib2.HTTPCookieProcessor(cj)
    opener = urllib2.build_opener(processor)
    url = 'http://example.webscraping.com'
    html = opener.open(url).read()

    tree = lxml.html.fromstring(html)
    tree.cssselect('ul#navbar li a')[0].text_content()