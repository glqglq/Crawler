import urllib,urllib2,lxml.html,cookielib
def parse_form(html):
    tree = lxml.html.fromstring(html)
    data = {}
    for e in tree.cssselect('form input'):
        if e.get('name'):
            data[e.get('name')] = e.get('value')
    return data
if __name__ == '__main__':
    LOGIN_URL = 'http://example.webscraping.com/user/login'

    # html = urllib2.urlopen(LOGIN_URL).read()
    # form = parse_form(html)
    # print form

    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    html = opener.open(LOGIN_URL).read()
    data = parse_form(html)
    data['email'] = '546751140@qq.com'
    data['password'] = '7758521'
    encoded_data = urllib.urlencode(data)
    request = urllib2.Request(LOGIN_URL,encoded_data)
    response = opener.open(request)
    print response.geturl()